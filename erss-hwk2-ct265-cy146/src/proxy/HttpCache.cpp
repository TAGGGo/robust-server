#include "HttpCache.hpp"
//Singleton
HttpCache &HttpCache::getInstance()
{
    static HttpCache instance;
    return instance;
}

void HttpCache::put(std::shared_ptr<HttpRequest> rqst, std::shared_ptr<HttpResponse> resp)
{
    std::lock_guard<std::mutex> lock(mutex_);
    str key = rqst->getKey();
    mp[key] = resp;
    que.push(key);
    if (que.size() > MAX_CACHE_SIZE)
    {
        auto front = que.front();
        Mylogger::instance(LOG_PATH)->Note(rqst->getId(), "POP KEY " + front + " from the cache");
        mp.erase(mp.find(front));
        que.pop();
    }
}

std::shared_ptr<HttpResponse> HttpCache::get(std::shared_ptr<HttpRequest> rqst)
{
    std::lock_guard<std::mutex> lock(mutex_);
    str key = rqst->getKey();
    if (mp.find(key) != mp.end())
    {
        return mp[key];
    }
    return std::shared_ptr<HttpResponse>(nullptr);
}

long HttpCache::getMaxAge(std::shared_ptr<HttpResponse> resp)
{
    time_t max_age = 0;
    str max_age_str = "";
    if (resp->hasHeaderField("Cache-Control"))
    {
        str feild = resp->getHeaderField("Cache-Control");
        max_age_str = feild.find("max-age=") != feild.npos ? feild.substr(feild.find("max-age=") + strlen("max-age=")) : max_age_str;
        max_age_str = feild.find("s-maxage=") != feild.npos ? feild.substr(feild.find("s-maxage=") + strlen("s-maxage=")) : max_age_str;
        max_age = max_age_str.size() != 0 ? stripNumber(max_age_str) : max_age;
        return max_age;
    }
    return -1;
}

time_t HttpCache::calculateExpireTime(std::shared_ptr<HttpResponse> resp)
{
    time_t current_age = resp->hasHeaderField("Age") ? std::stol(resp->getHeaderField("Age")) : 0;
    if (resp->hasHeaderField("Cache-Control"))
    {
        time_t max_age = getMaxAge(resp);
        return resp->getCreateTime() + max_age - current_age;
    }
    if (resp->hasHeaderField("Expires"))
    {
        return strToTime(resp->getHeaderField("Expires"));
    }
    time_t date, last_modified;
    date = resp->hasHeaderField("Date") ? strToTime(resp->getHeaderField("Date")) : 0;
    last_modified = resp->hasHeaderField("Last-Modified") ? strToTime(resp->getHeaderField("Last-Modified")) : date;
    return resp->getCreateTime() + (date - last_modified) / 10 - current_age;
}

bool HttpCache::isCacheable(std::shared_ptr<HttpResponse> resp)
{
    return !((resp->hasHeaderField("Cache-Control") && resp->getHeaderField("Cache-Control").find("no-store") != std::string::npos) || (resp->hasHeaderField("Cache-Control") && resp->getHeaderField("Cache-Control").find("private") != std::string::npos));
}

bool HttpCache::isInCache(std::shared_ptr<HttpRequest> rqst)
{
    
    return get(rqst) != std::shared_ptr<HttpResponse>(nullptr);
}

bool HttpCache::needValidation(std::shared_ptr<HttpRequest> rqst)
{
    if (!isInCache(rqst))
    {
        return false;
    }
    auto resp = get(rqst);
    time_t expire_time = calculateExpireTime(resp);
    if (resp->hasHeaderField("Cache-Control") && (resp->getHeaderField("Cache-Control").find("no-cache") != std::string::npos || resp->getHeaderField("Cache-Control").find("must-revalidate") != std::string::npos))
    {
        Mylogger::instance(LOG_PATH)->logInCacheNeedRevalidation(rqst->getId());
        return true;
    }
    if (difftime(time(nullptr), expire_time) > 0)
    {
        Mylogger::instance(LOG_PATH)->logInCacheButExpired(rqst->getId(), &expire_time);
        return true;
    }
    // Mylogger::instance(LOG_PATH)->logInCacheValid(rqst->getId());
    return false;
}

//Put pair<HttpRequest, HttpResponse> into Cache if exist
void HttpCache::putIntoCache(std::shared_ptr<HttpRequest> rqst, std::shared_ptr<HttpResponse> resp)
{
    if (!isCacheable(resp))
    {
        Mylogger::instance(LOG_PATH)->logNotCacheable(resp->getId(), "Cache-Control=" + resp->getHeaderField("Cache-Control"));
        return;
    }
    put(rqst, resp);
    time_t expire_time = calculateExpireTime(resp);
    if (resp->hasHeaderField("Cache-Control") && resp->getHeaderField("Cache-Control").find("no-cache") != std::string::npos)
    {
        Mylogger::instance(LOG_PATH)->logCachedNeedRevalidation(rqst->getId());
        return;
    }
    Mylogger::instance(LOG_PATH)->logCachedExpires(rqst->getId(), &expire_time);
}

//Return Cached Response if valid, else revalid and return new response
std::shared_ptr<HttpResponse> HttpCache::handleFindAndGetInCache(int fd, std::shared_ptr<HttpRequest> rqst)
{
    std::shared_ptr<HttpResponse> resp = nullptr;
    bool inCache = isInCache(rqst);
    bool needRevalid = needValidation(rqst);
    if (!inCache)
    {
        Mylogger::instance(LOG_PATH)->logNotInCache(rqst->getId());
    }
    if (inCache && !needRevalid)
    {
        Mylogger::instance(LOG_PATH)->logInCacheValid(rqst->getId());
        return get(rqst);
    }
    if (needRevalid)
    {
        resp = get(rqst);
        if (resp->hasHeaderField("ETag"))
        {
            rqst->insertHeader("If-None-Match", resp->getHeaderField("ETag"));
        }
        if (resp->hasHeaderField("Last-Modified"))
        {
            rqst->insertHeader("If-Modified-Since", resp->getHeaderField("Last-Modified"));
        }
    }
    int server_fd = connect_n_forward_to_server(fd, rqst);
    auto new_resp = receive_from_server_n_close(fd, server_fd, rqst);
    if (new_resp->getCode() == "304")
    {
        return resp;
    }
    if (new_resp->getCode() == "200")
    {
        putIntoCache(rqst, new_resp);
    }
    return new_resp;
}