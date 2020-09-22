FLAGS=-Wall -Wextra
STU_DIR=$(DIR)
NAME_STUDENT=task_$(STU_DIR)
OBJ_STUDENT_DIR=$(DIR)/obj_student/

NOINPUT=0
ARG=1
STDINP=2



OK='\033[0;32m'
FAIL='\033[0;31m'
NC='\033[0m'

STDRD=$(STD)
ifeq ($(LANG), 1)
	CC=clang
	EXT=.c
else
	CC=g++
	EXT=.cpp
endif

FILES_STUDENT=$(addprefix $(STU_DIR), $(CFILES))
OBJ_STUDENT=$(addprefix $(OBJ_STUDENT_DIR), $(CFILES:$(EXT)=.o))

all: random copy_main $(NAME_STUDENT) 
ifeq ($(CHECKTYPE), NOINPUT)
	./task > $(STU_DIR)/outputs/output
	diff $(STU_DIR)/outputs/output correct_outputs/output > $(STU_DIR)/diffs/difference &&
	echo "TEST $(OK)OK :)$(NC)" && echo "OK" > $(STU_DIR)/result\ 
	|| echo "$(FAIL)TEST FAILED :($(NC)" && echo "TEST FAILED: see the in diffs for more info" > $(STU_DIR)/result
ifeq ($(CHECKTYPE), ARG)
	python3 arg_test.py $(NAME_STUDENT) $(LEAK)
ifeq ($(CHECKTYPE), STDINP)
	python3 stdin_test.py $(NAME_STUDENT) $(LEAK)
endif

$(OBJ_STUDENT): $(OBJ_STUDENT_DIR)%.o: $(STU_DIR)%$(EXT)
	$(CC) -std=$(STDRD) -c $(FLAGS) $< -o $@

$(NAME_STUDENT): $(OBJ_STUDENT)
	$(CC) -std=$(SRDRD) $(FLAGS) $(OBJ_STUDENT) -o $(NAME_STUDENT)

clean:
	/bin/rm -rf $(OBJ_STUDENT_DIR)  obj_utils

fclean: clean
	/bin/rm -rf $(NAME_STUDENT)

re: fclean finish all

leakcheck:
ifeq ($(COMMAND_ARGS), 0)
	valgrind ./student
	/bin/rm -rf student.dSYM	
endif

finish: fclean
	/bin/rm -rf $(STU_DIR)* $(STU_DIR).git correct_answer student_answer difference diffs outputs leakchecks student.dSYM

.PHONY: all clean fclean re random move_main
