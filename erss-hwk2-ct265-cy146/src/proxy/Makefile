CXX = g++ -std=c++11 -g
objects = launch.o logger.o Http.o HttpCache.o helper_function.o socket_helper.o

all: deamon

deamon: $(objects)
	$(CXX) -pthread -ggdb3 -o deamon $(objects)
	rm -rf *.o
clean:
	rm -rf *.o deamon
