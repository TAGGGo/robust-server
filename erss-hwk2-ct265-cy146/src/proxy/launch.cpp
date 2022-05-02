#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <thread>
#include <fcntl.h>
#include "socket_helper.hpp"
extern HttpCache &cache;
Mylogger *Mylogger::logger_ = nullptr;
std::mutex Mylogger::mutex_;
static void skeleton_daemon()
{
    pid_t pid;
    pid = fork();

    //Fork to create a child process
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    //Dessociate from controlling tty
    if (setsid() < 0) exit(EXIT_FAILURE);

    //Point stdin/stdout/stderr at /dev/null
    int null_fd = open( "/dev/null", O_WRONLY );
    if(null_fd < 0 || dup2(null_fd, 0) < 0 || dup2(null_fd, 1) < 0 || dup2(null_fd, 2) < 0) {
        exit(EXIT_FAILURE);
    }
    //Chdir to "/"
    chdir("/");

    //Set umast to 0
    umask(0);

    //Use fork( ) again to make the process not a session leader
    pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    //Close signals
    struct sigaction action = {SIG_IGN};
    sigaction(SIGPIPE, &action, NULL);
}

int main()
{
    // Become a deamon
    skeleton_daemon();

    // "PORT:12345"
    int listen_fd = 0;
    try
    {
        listen_fd = init_server("12345");
    }
    catch (SocketException &e)
    {
        close(listen_fd);
        return EXIT_FAILURE;
    }
    uid_t id = 0;
    while (true)
    {
        try
        {
            struct sockaddr_storage socket_addr;
            socklen_t socket_addr_len = sizeof(socket_addr);
            int client_connection_fd = accept(listen_fd, (struct sockaddr *)&socket_addr, &socket_addr_len);
            std::thread Thread(handle_request, client_connection_fd, ++id);
            Thread.detach();
        }
        catch (SocketException &e)
        {
            continue;
        }
    }
    close(listen_fd);
    exit(EXIT_SUCCESS);
}
