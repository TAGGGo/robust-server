#ifndef _HELPER_FUNCTION
#define _HELPER_FUNCTION

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
#include "Http.h"
time_t strToTime(std::string field);
long stripNumber(std::string string);
#endif
