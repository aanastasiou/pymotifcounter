# 
CC=gcc
# 
CFLAGS=-c -Wall -O3 -DUNIX=1 -fcommon

LDFLAGS= -lm -O3

FILES=main clustering  grassberger  hash  list mat  metropolis  motif_ids  output  permutation  prob  random  results  role  stubs  switches
SOURCES=$(FILES:=.c)
OBJECTS=$(FILES:=.o)
EXECUTABLES=mfinder

all: $(SOURCES) $(EXECUTABLES)
	
$(EXECUTABLES): $(OBJECTS) 
	$(CC) $(OBJECTS) $(LDFLAGS) -o $(EXECUTABLES)

$(FILES):
	$(CC) $(CFLAGS) $@.c -o $@.o

clean:
	rm -rf *o mfinder
