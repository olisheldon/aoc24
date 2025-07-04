CXX = g++
CXXFLAGS = -std=c++23 -O2
BIN = bin
SOURCES = $(wildcard day*.cpp)
EXES = $(patsubst day%.cpp,$(BIN)/day%,$(SOURCES))

all: $(BIN) $(EXES)

$(BIN):
	mkdir -p $(BIN)

$(BIN)/day%: day%.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) -o $@ $<

.PHONY: clean
clean:
	rm -f $(BIN)/*