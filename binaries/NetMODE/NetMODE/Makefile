
FLAGS = -Wall -O3
#FLAGS = -g
LDFLAGS = -lpthread

NetMODE: obj/main.o\
	obj/kavoshSearch345.o\
	obj/kavoshSearch6.o\
	obj/common.o\
	obj/preProcess.o\
	obj/genRandomGraph.o\
	obj/searchRandGraph6.o\
	obj/searchRandGraph345.o\
	obj/TM.o 
	g++ obj/*.o -o NetMODE $(FLAGS) $(LDFLAGS)
	

obj/main.o:main.cpp
	g++ -c main.cpp -o obj/main.o $(FLAGS)

obj/common.o:common.cpp common.h
	g++ -c common.cpp -o obj/common.o $(FLAGS)

obj/kavoshSearch345.o:kavoshSearch345.cpp
	g++ -c kavoshSearch345.cpp -o obj/kavoshSearch345.o $(FLAGS)

obj/kavoshSearch6.o:kavoshSearch6.cpp
	g++ -c kavoshSearch6.cpp -o obj/kavoshSearch6.o $(FLAGS)

obj/preProcess.o:preProcess.cpp
	g++ -c preProcess.cpp -o obj/preProcess.o $(FLAGS)

obj/genRandomGraph.o: genRandomGraph.cpp
	g++ -c genRandomGraph.cpp -o obj/genRandomGraph.o $(FLAGS)

obj/searchRandGraph345.o: searchRandGraph6.cpp
	g++ -c searchRandGraph345.cpp -o obj/searchRandGraph345.o $(FLAGS)

obj/searchRandGraph6.o: searchRandGraph6.cpp
	g++ -c searchRandGraph6.cpp -o obj/searchRandGraph6.o $(FLAGS)

obj/TM.o: TM.cpp TM.h
	g++ -c TM.cpp -o obj/TM.o $(FLAGS)

clean:
	rm NetMODE obj/*.o

ar:
	tar cvzf ../baks/"`date`".tar.gz *.cpp *.h Makefile tags 
