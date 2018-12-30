int foo(int a, int b) {
	int c = b-a;
	return c;
}

int main() {
	int a = 1, b = '2', d;
	int c = 3;
	if (a == 1) {
		if (c == 2) {
			printf("a=%d c==2\n", a);
		}
		else
		{
			printf("a=%d c!=2\n", a);
		}
	}
	else if (b == '2') {
		printf("b=%c\n", b);
	} else
	{
		printf("hello\n");
	}
	return 0;
}
