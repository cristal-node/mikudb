cleanup: test
	@echo "cleaning up"
	@rm ./main

test: compile
	@echo "running"
	./main

compile: main.c
	@echo "starting compile"
	gcc -g -Wall -o main main.c -lm -lcurl