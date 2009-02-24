CXX = g++
CXXFLAGS = -DDEBUG -g -I/home/rberckmans/lib/boost_1_36_0 -I/usr/include/python2.5
OBJECTS = logger.o sockets.o cmd_router.o mud_python.o main.o
EXEC = a.out
LINK = -L/usr/local/lib -lboost_system-gcc41-mt -lboost_python-gcc41-mt -lpython2.5


$(EXEC): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(LINK) $(OBJECTS) -o $@

logger.o : logger.hpp

sockets.o : sockets.hpp

mud_python.o : mud_python.hpp

cmd_router.o : cmd_router.hpp

clean :
	rm -f $(EXEC) $(OBJECTS)
	rm -f *.pyc