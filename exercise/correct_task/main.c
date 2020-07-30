#include <stdio.h>

int aplusb(int a, int b);

int main(void)
{
	if (aplusb(3, 1) != 4)
		printf("ERROR!\nEXECTED:4\nSTUDENTS:%d\n", aplusb(3, 1));
	else
		printf("TEST 1...OK:)");
	return (0);
}
