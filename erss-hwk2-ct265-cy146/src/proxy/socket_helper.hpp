#ifndef __SOCKET_HELPER_HPP
#define __SOCKET_HELPER_HPP

#include <sys/socket.h>
#include <sys/select.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <iostream>
#include <memory>
#include <functional>
#include <unistd.h>
#include "HttpCache.hpp"
#define RECV_BUF_LENGTH 20480
#define BUF_LENGTH 4096
static str RSP_200OK = "HTTP/1.1 200 OK\r\n\r\n";
static str RSP_400BadRequest = "HTTP/1.1 400 Bad Request\r\n\r\n";
static str RSP_502BadGateway = "HTTP/1.1 502 Bad Gateway\r\n\r\n";
static str RSP_501NotImplemented = "HTTP/1.1 501 Not Implemented\r\n\r\n";

int init_server(const char *port);

int init_client(const char *hostname, const char *port);

std::string get_ip_address(int fd);

ssize_t send_string(int fd, std::string msg);

std::string read_string(int fd);

std::string read_until(int fd, str end);

void forward(int from_fd, int to_fd);

int connect_n_forward_to_server(int fd, std::shared_ptr<HttpRequest> rqst);

std::shared_ptr<HttpResponse> receive_from_server_n_close(int fd, int server_fd, std::shared_ptr<HttpRequest> rqst);

void respond_to_client(int fd, std::shared_ptr<HttpResponse> resp);

void build_tunnel(int fd, std::shared_ptr<HttpRequest> rqst);

void handle_request(int fd, uid_t id);

#endif
