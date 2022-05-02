#include "helper_function.h"
#include <cctype>
#include <algorithm>

time_t strToTime(std::string field)
{
    time_t time_needed;
    if (field.find("\r\n") != field.npos)
    {
        field = field.substr(0, field.find("\r\n"));
    }
    std::tm t;
    strptime(field.c_str(), "%a, %d %b %Y %H:%M:%S %Z", &t);
    time_needed = std::mktime(&t);
    return time_needed;
}

long stripNumber(std::string string)
{
    long ans = 0;
    for (int i = 0; i < string.size(); ++i)
    {
        if (string[i] >= '0' && string[i] <= '9')
        {
            ans += ans * 10 + (string[i] - '0');
        }
        else
        {
            break;
        }
    }
    return ans;
}