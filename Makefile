CXX=nvcc
CXXFLAGS=-std=c++11 -O3
SRCS = a3.cpp a3.cu
OBJS = a3.o a3_cuda.o

TARGET = a3

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

a3.o: a3.cpp
	$(CXX) $(CXXFLAGS) -x cu -dc $< -o $@

a3_cuda.o: a3.cu
	$(CXX) $(CXXFLAGS) -dc $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)