int a, b;
int d[10];

struct mstruct{
    int a;
    double b[10];
};

// struct mstruct x;
struct mstruct x[10];

void void_foo(){
    printf("void_foo\n");
    return;
}

int foo(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

int main() {
    int i;
    int c[10];
    for (i = 0; i < 10; i = i+1) {
        scanf("%d", &x[i].a);
    }
    for (i = 0; i < 10; i = i+1) {
        printf("x[%d].a=%d\n", i, x[i].a);
    }
    return 0;
}