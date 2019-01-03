int a, b;
int d[10];

int foo(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

int main() {
    int c[10];
    scanf("%d%d", &a, &b);
    scanf("%d%d", &c[0], &c[1]);
    scanf("%d%d", &d[0], &d[1]);
    printf("a+b=%d\n", a+b);
    printf("c[0]=%d\n", c[0]);
    printf("c[1]=%d\n", c[1]);
    printf("d[0]=%d\n", d[0]);
    printf("d[1]=%d\n", d[1]);
    return 0;
}