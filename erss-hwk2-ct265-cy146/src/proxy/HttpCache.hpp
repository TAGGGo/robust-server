#ifndef _HTTP_CACHE_HPP
#define _HTTP_CACHE_HPP
#define MAX_CACHE_SIZE 100

#include <string>
#include <unordered_map>
#include <queue>
#include <memory>
#include "logger.h"
#include "Http.h"
#include "helper_function.h"

using umap=std::unordered_map<std::string, std::shared_ptr<HttpResponse> >;
using queue=std::queue<std::string>;

/*Use First in First Out Stretegy*/
class HttpCache {
    private:
    umap mp;
    queue que;
    std::mutex mutex_;
    HttpCache() {}
    ~HttpCache() {}

    void put(std::shared_ptr<HttpRequest> rqst, std::shared_ptr<HttpResponse> resp);
    std::shared_ptr<HttpResponse> get(std::shared_ptr<HttpRequest> rqst);

    long getMaxAge(std::shared_ptr<HttpResponse> resp);
    time_t calculateExpireTime(std::shared_ptr<HttpResponse> resp);
    bool isCacheable(std::shared_ptr<HttpResponse> resp);
    bool needValidation(std::shared_ptr<HttpRequest> rqst);
    void putIntoCache(std::shared_ptr<HttpRequest> rqst, std::shared_ptr<HttpResponse> resp);
    bool isInCache(std::shared_ptr<HttpRequest> rqst);
    public:
    std::shared_ptr<HttpResponse> handleFindAndGetInCache(int fd, std::shared_ptr<HttpRequest> rqst);
    static HttpCache & getInstance();
};
#include "socket_helper.hpp"
#endif