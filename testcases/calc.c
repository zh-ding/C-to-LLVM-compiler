// to DingZheng
// I'm so Cai

// Zeyu Wang is the BEST. --By Xun Lu

#include <stdio.h>
#include <string.h>

char expr[1000];
int st_num[1000];
char st_op[1000];

int main(){

    int st_num_pt = -1;
    int st_op_pt = -1;

    scanf("%s", expr + 1);
    expr[0] = '(';
    int len = strlen(expr);
    expr[len++] = ')';

    int i = len - 1;
    int num = 0;
    int k = 1;
    while(i >= 0){
        if(expr[i] == '+'){
            while(st_op_pt >= 0 && (st_op[st_op_pt] == '*' || st_op[st_op_pt] == '/')){
                if(st_op[st_op_pt--] == '*')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] * st_num[st_num_pt - 1];
                else
                    st_num[st_num_pt - 1] = st_num[st_num_pt] / st_num[st_num_pt - 1];
                --st_num_pt;
            }
            st_op[++st_op_pt] = '+';
            --i;
        }else if(expr[i] == '-'){
            while(st_op_pt >= 0 && (st_op[st_op_pt] == '*' || st_op[st_op_pt] == '/')){
                if(st_op[st_op_pt--] == '*')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] * st_num[st_num_pt - 1];
                else
                    st_num[st_num_pt - 1] = st_num[st_num_pt] / st_num[st_num_pt - 1];
                --st_num_pt;
            }
            st_op[++st_op_pt] = '-';
            --i;
        }else if(expr[i] == '*'){
            st_op[++st_op_pt] = '*';
            --i;
        }else if(expr[i] == '/'){
            st_op[++st_op_pt] = '/';
            --i;
        }else if(expr[i] == ')'){
            st_op[++st_op_pt] = ')';
            --i;
        }else if(expr[i] == '('){
            while(st_op[st_op_pt] != ')'){
                char ch = st_op[st_op_pt--];
                if(ch == '+')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] + st_num[st_num_pt - 1];
                else if(ch == '-')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] - st_num[st_num_pt - 1];
                else if(ch == '*')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] * st_num[st_num_pt - 1];
                else if(ch == '/')
                    st_num[st_num_pt - 1] = st_num[st_num_pt] / st_num[st_num_pt - 1];
                --st_num_pt;
            }
            --st_op_pt;
            --i;
        }else{
            num = 0;
            k = 1;
            while(i >= 0 && expr[i] >= '0' && expr[i] <= '9'){
                num = num + (expr[i] - '0') * k;
                k = k * 10;
                --i;
            }
            st_num[++st_num_pt] = num;
        }
    }
    printf("%d\n", st_num[0]);
    return 0;
}
