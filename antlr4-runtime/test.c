#include <string.h>
#include <stdlib.h>

int main() {
	char s[1024];
	int len, i, flag = 0;
	gets(s);
	len = strlen(s);
	if (len < 0 || len > 1024) {
		printf("Error detected!\n");
	}
	else {
		i = 0;
		while (i + i < len && flag == 0) {
			if (s[i] != s[len - 1 - i]) {
                printf("False\n");
                flag = 1;
            }
            i = i+1;
		}
        if (flag == 0) {
        	printf("True\n");
        }
    }
	return 0;
}