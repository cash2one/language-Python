main:libtest.so main.cpp
	g++ main.cpp -o $(@) -I./ -L./ -ltest

libtest.so:testLib.cpp
	g++ -shared -o libtest.so testLib.cpp -I./

clean:
	rm main *~ *pyc

