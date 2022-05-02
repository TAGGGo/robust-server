#include "logger.h"
Mylogger::Mylogger(std::string logFilename)
{
    pthread_mutex_init(&mLock, NULL);
    mStream.open(logFilename, std::fstream::app);
}

Mylogger::~Mylogger()
{
    mStream.close();
    pthread_mutex_destroy(&mLock);
}

Mylogger *Mylogger::instance(std::string path)
{
    std::lock_guard<std::mutex> lock(mutex_);
    if (logger_ == nullptr)
    {
        logger_ = new Mylogger(path);
    }
    return logger_;
}

void Mylogger::log(const std::string content)
{
    pthread_mutex_lock(&mLock);
    mStream << content << std::endl;
    pthread_mutex_unlock(&mLock);
}

std::string Mylogger::_toTimeString(const std::time_t *time)
{
    auto *ptr = std::gmtime(time);
    if (ptr == nullptr)
    {
        throw SystemException("Time data is not correct!");
    }

    std::string stime = std::asctime(ptr);
    // pop \n in the end
    stime.pop_back();
    return stime + " UTC";
}

// Check if in Cache
void Mylogger::logNotInCache(int id)
{
    log(std::to_string(id) + ": not in cache");
}
void Mylogger::logInCacheButExpired(int id, const std::time_t *time)
{
    log(std::to_string(id) + ": in cache, but expired at " + _toTimeString(time));
}
void Mylogger::logInCacheNeedRevalidation(int id)
{
    log(std::to_string(id) + ": in cache, requires validation");
}
void Mylogger::logInCacheValid(int id)
{
    log(std::to_string(id) + ": in cache, valid");
}

// Log Cached info
void Mylogger::logNotCacheable(int id, std::string reason)
{
    log(std::to_string(id) + ": not cacheable because " + reason);
}
void Mylogger::logCachedExpires(int id, const std::time_t *time)
{
    log(std::to_string(id) + ": cached, expires at " + _toTimeString(time));
}
void Mylogger::logCachedNeedRevalidation(int id)
{
    log(std::to_string(id) + ": cached, but requires re-validation");
}

// Log Request/Response
void Mylogger::logNewRequestFromClient(int id, std::string request, std::string hostname, const std::time_t *time)
{
    log(std::to_string(id) + ": \"" + request + "\" from " + hostname + " @ " + _toTimeString(time));
}
void Mylogger::logMakeRequestToServer(int id, std::string request, std::string hostname)
{
    log(std::to_string(id) + ": Requesting \"" + request + "\" from " + hostname);
}
void Mylogger::logReciveResponseFromServer(int id, std::string response, std::string hostname)
{
    log(std::to_string(id) + ": Received \"" + response + "\" from " + hostname);
}
void Mylogger::logResponseToClient(int id, std::string response)
{
    log(std::to_string(id) + ": Responding \"" + response + "\"");
}

// Tunnel
void Mylogger::logTunnelClose(int id)
{
    log(std::to_string(id) + ": Tunnel Closed");
}

// Three Catagory
void Mylogger::Note(int id, std::string msg)
{
    log(std::to_string(id) + ": NOTE: " + msg);
}
void Mylogger::Warning(int id, std::string msg)
{
    log(std::to_string(id) + ": WARNING: " + msg);
}
void Mylogger::Error(int id, std::string msg)
{
    log(std::to_string(id) + ": ERROR: " + msg);
}