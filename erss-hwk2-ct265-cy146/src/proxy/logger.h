#ifndef MYLOGGER_H
#define MYLOGGER_H

#ifndef LOG_PATH
#define LOG_PATH "/var/log/erss/proxy.log"
//#define LOG_PATH "../../logs/log.txt"
#endif

#include <fstream>
#include <pthread.h>
#include <mutex>
#include "ProxyException.hpp"

class Mylogger
{
public:
   static Mylogger *instance(std::string path);
   virtual ~Mylogger();
   void log(const std::string content);
   std::string _toTimeString(const std::time_t *time);

   // Check if in Cache
   void logNotInCache(int id);
   void logInCacheButExpired(int id, const std::time_t *time);
   void logInCacheNeedRevalidation(int id);
   void logInCacheValid(int id);

   // Log Cached info
   void logNotCacheable(int id, std::string reason);
   void logCachedExpires(int id, const std::time_t *time);
   void logCachedNeedRevalidation(int id);

   // Log Request/Response
   void logNewRequestFromClient(int id, std::string request, std::string hostname, const std::time_t *time);
   void logMakeRequestToServer(int id, std::string request, std::string hostname);
   void logReciveResponseFromServer(int id, std::string response, std::string hostname);
   void logResponseToClient(int id, std::string response);

   // Tunnel
   void logTunnelClose(int id);

   // Three Catagory
   void Note(int id, std::string msg);
   void Warning(int id, std::string msg);
   void Error(int id, std::string msg);

private:
   Mylogger(std::string logFileName);
   static Mylogger *logger_;
   static std::mutex mutex_;
   std::ofstream mStream;
   pthread_mutex_t mLock;
};

#endif