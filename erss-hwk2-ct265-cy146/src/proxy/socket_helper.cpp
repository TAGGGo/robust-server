#include "socket_helper.hpp"

int init_server(const char *port)
{
  const char *hostname = NULL;
  int status;
  int socket_fd;
  struct addrinfo host_info;
  struct addrinfo *host_info_list;
  memset(&host_info, 0, sizeof(host_info));

  host_info.ai_family = AF_UNSPEC;
  host_info.ai_socktype = SOCK_STREAM;
  host_info.ai_flags = AI_PASSIVE;

  status = getaddrinfo(hostname, port, &host_info, &host_info_list);
  if (status != 0)
  {
    std::cerr << "Cannot get address info" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot create socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }

  socket_fd = socket(host_info_list->ai_family,
                     host_info_list->ai_socktype,
                     host_info_list->ai_protocol);
  if (socket_fd == -1)
  {
    std::cerr << "Error: cannot create socket" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot create socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }
  int yes = 1;
  status = setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
  status = bind(socket_fd, host_info_list->ai_addr, host_info_list->ai_addrlen);
  if (status == -1)
  {
    std::cerr << "Error: cannot bind socket" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot bind socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }

  status = listen(socket_fd, 100);
  if (status == -1)
  {
    std::cerr << "Error: cannot listen on socket" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot listen on socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }
  return socket_fd;
}

int init_client(const char *hostname, const char *port)
{
  int status;
  int socket_fd;
  struct addrinfo host_info;
  struct addrinfo *host_info_list;
  memset(&host_info, 0, sizeof(host_info));
  host_info.ai_family = AF_UNSPEC;
  host_info.ai_socktype = SOCK_STREAM;

  status = getaddrinfo(hostname, port, &host_info, &host_info_list);
  if (status != 0)
  {
    std::cerr << "Error: cannot get address info for host" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot get address info for host: " + std::string(hostname) + ", port: " + std::string(port));
  }

  socket_fd = socket(host_info_list->ai_family,
                     host_info_list->ai_socktype,
                     host_info_list->ai_protocol);
  if (socket_fd == -1)
  {
    std::cerr << "Error: cannot create socket" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot create socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }

  std::cout << "Connecting to " << hostname << " on port " << port << "..." << std::endl;
  if (connect(socket_fd, host_info_list->ai_addr, host_info_list->ai_addrlen) == -1)
  {
    std::cerr << "Error: cannot connect to socket" << std::endl;
    std::cerr << "  (" << hostname << "," << port << ")" << std::endl;
    throw SocketException("Cannot connect to socket for host: " + std::string(hostname) + ", port: " + std::string(port));
  }
  return socket_fd;
}

std::string get_ip_address(int fd)
{
  socklen_t size;
  struct sockaddr_storage addr_storage;
  char ip[INET_ADDRSTRLEN];
  size = sizeof(addr_storage);
  getpeername(fd, (struct sockaddr *)&addr_storage, &size);
  struct sockaddr_in * s = (struct sockaddr_in *)&addr_storage;
  inet_ntop(AF_INET, &s->sin_addr, ip, sizeof(ip));
  return ip;
}

ssize_t send_string(int fd, std::string msg)
{
  if (msg.size() == 0)
  {
    return 0;
  }
  size_t size = msg.size();
  ssize_t size_sent = write(fd, &msg.c_str()[0], size);
  if (size_sent <= 0)
  {
    close(fd);
    throw IOException("Send Failure To fd: " + std::to_string(fd));
  }
  return size_sent;
}

std::string read_string(int fd)
{
  char buffer[RECV_BUF_LENGTH];
  memset(buffer, 0, sizeof(buffer));
  size_t size = recv(fd, buffer, sizeof(buffer), 0);
  if (size <= 0)
  {
    close(fd);
    throw IOException("Read Failure From fd: " + std::to_string(fd));
  }
  str ans(size, 0);
  for (int i = 0; i < (int)size; ++i)
  {
    ans[i] = buffer[i];
  }
  return ans;
}

std::string read_until(int fd, str end)
{
  std::string ans;
  while (true)
  {
    ans += read_string(fd);
    if (ans.find(end) != std::string::npos)
    {
      break;
    }
  }
  return ans;
}

int connect_n_forward_to_server(int fd, std::shared_ptr<HttpRequest> rqst)
{
  try
  {
    str host = rqst->getHost();
    str port = rqst->getPort();
    int server_fd = init_client(host.c_str(), port.c_str());
    // Forward to server fd
    Mylogger::instance(LOG_PATH)->logMakeRequestToServer(rqst->getId(), rqst->getFirstLine(), rqst->getHost());
    send_string(server_fd, rqst->toStr());
    return server_fd;
  }
  catch (const std::exception &exception)
  {
    auto resp = std::make_shared<HttpResponse>(rqst->getId(), RSP_400BadRequest);
    send_string(fd, resp->toStr());
    Mylogger::instance(LOG_PATH)->logResponseToClient(rqst->getId(), resp->getFirstLine());
    throw exception;
  }
}

std::shared_ptr<HttpResponse> receive_from_server_n_close(int fd, int server_fd, std::shared_ptr<HttpRequest> rqst)
{
  try
  {
    // Receive response from server
    str recv_buffer = read_until(server_fd, "\r\n\r\n");
    std::shared_ptr<HttpResponse> response = std::make_shared<HttpResponse>(rqst->getId(), recv_buffer);
    Mylogger::instance(LOG_PATH)->logReciveResponseFromServer(rqst->getId(), response->getFirstLine(), rqst->getHost());
    if (response->hasHeaderField("Transfer-Encoding") && response->getHeaderField("Transfer-Encoding") == "chunked")
    {
      while (response->getBody().find("0\r\n\r\n") == std::string::npos)
      {
        str restbuffer = read_string(server_fd);
        response->appendBody(restbuffer);
      }
    }
    else if (response->hasHeaderField("Content-Length"))
    {
      auto total_len = std::stol(response->getHeaderField("Content-Length"));
      auto received_len = response->getBodySize();
      while (received_len < total_len)
      {
        str restbuffer = read_string(server_fd);
        received_len += restbuffer.size();
        response->appendBody(restbuffer);
      }
    }
    close(server_fd);
    return response;
  }
  catch (std::exception &exception)
  {
    auto resp = std::make_shared<HttpResponse>(fd, RSP_502BadGateway);
    send_string(fd, resp->toStr());
    Mylogger::instance(LOG_PATH)->logResponseToClient(rqst->getId(), resp->getFirstLine());
    close(server_fd);
    throw exception;
  }
}

void forward(int from_fd, int to_fd)
{
  str buffer = read_string(from_fd);
  send_string(to_fd, buffer);
}

void respond_to_client(int fd, std::shared_ptr<HttpResponse> resp)
{
  Mylogger::instance(LOG_PATH)->logResponseToClient(resp->getId(), resp->getFirstLine());
  send_string(fd, resp->toStr());
}

void build_tunnel(int fd, std::shared_ptr<HttpRequest> rqst)
{
  ssize_t send_size = send_string(fd, RSP_200OK);
  str host = rqst->getHost();
  str port = rqst->getPort();
  int server_fd = init_client(host.c_str(), port.c_str());
  fd_set fds, origin_fd;
  FD_ZERO(&fds);
  FD_ZERO(&origin_fd);
  FD_SET(fd, &fds);
  FD_SET(server_fd, &fds);
  int max_fd = std::max(fd, server_fd);
  struct timeval tv;
  tv.tv_sec = 3600;
  tv.tv_usec = 0;
  origin_fd = fds;
  while (true)
  {
    try
    {
      fds = origin_fd;
      int res = select(max_fd + 1, &fds, NULL, NULL, &tv);
      if (res <= 0)
      {
        break;
      }
      if (FD_ISSET(fd, &fds))
      {
        forward(fd, server_fd);
      }
      if (FD_ISSET(server_fd, &fds))
      {
        forward(server_fd, fd);
      }
    }
    catch (std::exception &e)
    {
      break;
    }
  }
}

void _handle_request(int fd, uid_t id)
{
  std::shared_ptr<HttpRequest> request;
  std::string buffer;
  try
  {
    buffer = read_string(fd);
    request = std::make_shared<HttpRequest>(id, buffer);
    time_t create_time = request->getCreateTime();
    Mylogger::instance(LOG_PATH)->logNewRequestFromClient(id, request->getFirstLine(),  get_ip_address(fd), &create_time);
  }
  catch (std::exception &exception)
  {
    auto resp = std::make_shared<HttpResponse>(id, RSP_400BadRequest);
    send_string(fd, resp->toStr());
    Mylogger::instance(LOG_PATH)->logResponseToClient(id, resp->getFirstLine());
    throw exception;
  }

  if (request->getMethod() == "GET")
  {
    auto resp = HttpCache::getInstance().handleFindAndGetInCache(fd, request);
    respond_to_client(fd, resp);
  }
  else if (request->getMethod() == "POST")
  {
    int server_fd = connect_n_forward_to_server(fd, request);
    auto resp = receive_from_server_n_close(fd, server_fd, request);
    respond_to_client(fd, resp);
  }
  else if (request->getMethod() == "CONNECT")
  {
    build_tunnel(fd, request);
  }
  else
  {
    auto resp = std::make_shared<HttpResponse>(id, RSP_501NotImplemented);
    send_string(fd, resp->toStr());
    Mylogger::instance(LOG_PATH)->logResponseToClient(id, resp->getFirstLine());
    throw HttpException("Not Implemented");
  }
  Mylogger::instance(LOG_PATH)->logTunnelClose(id);
  close(fd);
}

void handle_request(int fd, uid_t id)
{
  try
  {
    _handle_request(fd, id);
  }
  catch (const std::exception &e)
  {
    close(fd);
    Mylogger::instance(LOG_PATH)->logTunnelClose(id);
    return;
  }
}