#ifndef __PROXY_EXCEPTION_HPP_
#define __PROXY_EXCEPTION_HPP_

#include <exception>
#include <string>

class SystemException : public std::exception
{
    std::string message;

public:
    SystemException(std::string msg) : message(msg) {}

    const char *what() const throw() { return message.c_str(); }
};

class SocketException : public std::exception
{
    std::string message;

public:
    SocketException(std::string msg) : message(msg) {}

    const char *what() const throw() { return message.c_str(); }
};

class IOException : public std::exception
{
    std::string message;

public:
    IOException(std::string msg) : message(msg) {}

    const char *what() const throw() { return message.c_str(); }
};

class HttpException : public std::exception
{
    std::string message;

public:
    HttpException(std::string msg) : message(msg) {}

    const char *what() const throw() { return message.c_str(); }
};

#endif
