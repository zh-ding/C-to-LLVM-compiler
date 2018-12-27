int main() {
	char s[1024];
	int len, i;
	gets(s);
	len = strlen(s);
	if (len < 0 || len > 1024) {
		printf("Error detected!\n");
		return 0;
	}
	for (i = 0; i+i < len; ++i)
	if (s[i] != s[len-1-i]) {
		printf("False\n");
		return 0;
	}
	printf("True\n");
	return 0;
}