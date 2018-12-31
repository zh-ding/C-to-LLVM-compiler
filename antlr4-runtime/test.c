int foo(int a, int b) {
	int c = b-a;
	return c;
}

int main() {
	int a = 1, b = '3', d;
	int c = 3;
	int arr[10];
	arr[0] = c;
	if (a == 1 && b == '2') {
		if (c == 2) {
			printf("a=%d c==2\n", a);
		}
		else
		{
			printf("a=%d c!=2\n", a);
		}
	}
	else if (b == '4') {
		printf("b=%c\n", b);
	} else
	{
		printf("hello arr[0]=%d\n", arr[0]);
	}
	return 0;
}
