#include "Http.h"
#include <cctype>
#include <algorithm>

std::string toLower(std::string data)
{
    std::transform(data.begin(), data.end(), data.begin(),
                   [](unsigned char c)
                   { return std::tolower(c); });
    return data;
}
bool checkMethod(std::string method)
{
    if (method.size() == 0)
    {
        return false;
    }
    else
    {
        for (auto &c : method)
        {
            if (c < 'A' || c > 'Z')
            {
                return false;
            }
        }
    }
    return true;
}

bool checkVersion(std::string version)
{
    return version.find("HTTP/") != version.npos;
}

bool checkUrl(std::string url)
{
    return url.size() != 0;
}

str Http::getLine()
{
    return line;
}
str Http::getResHeader()
{
    return resHeader;
}

size_t Http::getId()
{
    return id;
}

std::unordered_map<str, str> Http::getHeaderInfo()
{
    return headerInfo;
}

time_t Http::getCreateTime()
{
    return create_time;
}

void Http::insertHeader(str key, str value)
{
    key = toLower(key);
    headerInfo[key] = value;
}

Http::Http(size_t Id, std::string buff) : create_time(time(NULL))
{
    try
    {
        id = Id;
        ssize_t pos = buff.find("\r\n\r\n");
        resHeader = buff.substr(pos + 4, buff.size() - (pos + 4));
        std::stringstream ss(buff.substr(0, pos));
        std::getline(ss, line, '\n');
        if (line.back() == '\r')
        {
            line.pop_back();
        }
        std::string tmp;
        while (std::getline(ss, tmp, '\n'))
        {
            if (tmp.size() != 0)
            {
                if (tmp.back() == '\r')
                {
                    tmp.pop_back();
                }
                ssize_t div_pos = tmp.find(": ");
                insertHeader(tmp.substr(0, div_pos), tmp.substr(div_pos + 2, tmp.size() - (div_pos + 2)));
            }
        }
    }
    catch (std::exception &e)
    {
        throw HttpException("Request Error: " + std::string(e.what()));
    }
}

bool Http::hasHeaderField(str field)
{
    field = toLower(field);
    return headerInfo.find(field) != headerInfo.end();
}

str Http::getHeaderField(str field)
{
    field = toLower(field);
    if (headerInfo.find(field) == headerInfo.end())
    {
        throw HttpException("header does not contain field: " + field);
    }
    return headerInfo[field];
}

str Http::toStr()
{
    str ans = line + "\r\n";
    for (auto &p : headerInfo)
    {
        ans += (p.first + ": " + p.second + "\r\n");
    }
    ans += ("\r\n" + resHeader);
    return ans;
}

str Http::getFirstLine() { return line; }

Http::~Http() {}
HttpRequest ::HttpRequest(size_t Id, std::string buff) : Http(Id, buff)
{
    try
    {
        std::stringstream ss(line);
        std::getline(ss, method, ' ');
        std::getline(ss, url, ' ');
        std::getline(ss, version, ' ');
        if (!checkMethod(method) || !checkUrl(url) || !checkVersion(version))
        {
            throw HttpException("Malformed firstline");
        }

        // std::cout << method << " " << url << " " << version << std::endl;
        if (hasHeaderField("Host"))
        {
            std::string host_line = getHeaderField("Host");
            ssize_t host_line_divpos = host_line.find(':');
            if (host_line_divpos == std::string::npos)
            {
                host = host_line;
            }
            else
            {
                host = host_line.substr(0, host_line_divpos);
                port = host_line.substr(host_line_divpos + 1, host_line.size() - (host_line_divpos + 1));
            }
        }
        // Truncate url if its Absolute Path
        if (url.find("http://") != url.npos)
        {
            url = url.substr(url.find("http://") + strlen("http://"));
            url = url.substr(url.find("/"));
            line = method + " " + url + " " + version;
        }
    }
    catch (std::exception &e)
    {
        throw HttpException("Request Error: " + std::string(e.what()));
    }
}
str HttpRequest::getMethod() { return method; }
str HttpRequest::getPort() { return port; }
str HttpRequest::getHost() { return host; }
str HttpRequest::getUrl() { return url; }
str HttpRequest::getKey()
{
    if (url.find("http") != url.npos)
    {
        return url;
    }
    if (url.find(host) != url.npos)
    {
        return "http://" + url;
    }
    return "http://" + host + url;
}
HttpRequest::~HttpRequest() {}

HttpResponse::HttpResponse(size_t Id, std::string buff) : Http(Id, buff)
{
    std::stringstream ss(line);
    std::getline(ss, version, ' ');
    std::getline(ss, code, ' ');
    std::getline(ss, status, ' ');
}
str HttpResponse::getBody() { return resHeader; }
void HttpResponse::appendBody(str string) { resHeader += string; }
long HttpResponse::getBodySize() { return resHeader.size(); }
str HttpResponse::getCode() { return code; }

// int main(){
//     std::ifstream t("req.txt");
//     std::stringstream buffer;
//     buffer << t.rdbuf();
//     str s = buffer.str();
//     //s = "GET http://vcm-24073.vm.duke.edu:15213/ HTTP/1.1\nHost: vcm-24073.vm.duke.edu:15213\r\n\r\n";
//     s = "GET http://vcm-24073.vm.duke.edu:15213/ HTTP/1.1";
//     //std::cout << s << std::endl;
//     std::size_t i = 1;
//     // Http *p =  new Http(i, v);
//     HttpRequest * p =  new HttpRequest(i, s);
//     //std::cout << "body:"<< p->getBody()<<std::endl;
//     std::cout << "host:" << p->getHost() <<std::endl;
//     std::cout << "port:" << p->getPort()<<std::endl;
//     std::cout << "url:" << p->getUrl()<<std::endl;
//     for(auto i : p->headerInfo){
//         std::cout << i.first << "----" << i.second<<std::endl;
//     }
// }
