PYTHON_VERSION=2.5
BOOST_VERSION=1_38
GCC_VERSION=43

BOOST_INCLUDE_PATH=/usr/local/include
PYTHON_INCLUDE_PATH=/usr/include
LINK_PATH=/usr/local/lib


CXX = g++
CXXFLAGS = -DDEBUG -g -I$(BOOST_INCLUDE_PATH)/boost-$(BOOST_VERSION) -I$(PYTHON_INCLUDE_PATH)/python$(PYTHON_VERSION)
OBJECTS = logger.o sockets.o cmd_router.o mud_python.o main.o
EXEC = a.out
SHARED_PYTHON_LIBS = cppTypes.so
SHARED_PYTHON_LIBS_FLAGS = -DBOOST_PYTHON_DYNAMIC_LIB
LINK = -L$(LINK_PATH) -lboost_system-gcc$(GCC_VERSION)-mt -lboost_python-gcc$(GCC_VERSION)-mt -lpython$(PYTHON_VERSION)

all: $(EXEC) $(SHARED_PYTHON_LIBS)

$(EXEC): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(LINK) $(OBJECTS) -o $@

logger.o : logger.hpp

sockets.o : sockets.hpp

mud_python.o : mud_python.hpp

cmd_router.o : cmd_router.hpp

cppTypes.so: mud_python.o
	$(CXX) $(LINK) $(SHARED_PYTHON_LIBS_FLAGS) -shared -o cppTypes.so mud_python.o

clean :
	rm -f $(EXEC) $(OBJECTS)
	rm -f *.pyc
	rm -f *.so
