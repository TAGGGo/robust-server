#ifndef _HTTP_HPP
#define _HTTP_HPP

#include <ctime>
#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <fstream>  
#include <iostream> 
#include <stdio.h>
#include <string.h>
#include "ProxyException.hpp"
using str=std::string;
class Http{
    public:
        size_t id;
        str line; // first line
        str resHeader;
        std::unordered_map<str, str> headerInfo;
        time_t create_time;
    public:
        Http(size_t Id, std::string buff);
        ~Http();
        
        size_t getId();
        str getFirstLine();
        str getHeader();
        str getHeaderInfo(str buff);
        str getLine();
        str getResHeader();
        str toStr();
        time_t getCreateTime();
        void insertHeader(str key, str value);

        bool hasHeaderField(str field);
        str getHeaderField(str field);
        std::unordered_map<str, str> getHeaderInfo();

};

class HttpRequest : public Http{
    protected:
        str method;
        str version;
        str host;
        str url;
        // HTTP
        // str type;
        str port = "80";
    
    public:
        HttpRequest(size_t Id, std::string buff);
        ~HttpRequest();
        str getMethod();
        str getHost();
        str getPort();
        str getKey();
        str getUrl();
};

class HttpResponse : public Http{
    private:
        str responseCode;
        str status;
        str code;
        str version;

    public:
        HttpResponse(size_t Id, std::string buff);
        str getBody();
        long getBodySize();
        str getCode();
        void appendBody(str string);

};

#endif