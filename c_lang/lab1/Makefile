NAME = lab1
CFLAGS = -Wall -Wextra


all:
	gcc -c main_lab1.c gitdir/average_between_negatives.c
	gcc $(CFLAGS) main_lab1.o average_between_negatives.o -o lab1

leak:
	valgrind lab1 && grep total

clean:
	/bin/rm -rf main_lab1.o average_between_negatives.o
fclean: clean
	/bin/rm -rf lab1

re: fclean all
