#include <stdio.h>

struct AVLNode{
	int elem;
	int is_null;
	int height;
	int left, right;
};

int root;

struct AVLNode nodes[10000];
int avai = 1;

int max(int a, int b){
	if(a > b) {
		return a;
	}
	return b;
}

void initTree(){
	int i;
	root = 0;
	for(i = 0; i < 100; i=i+1){
		nodes[i].is_null = 1;
		nodes[i].height = 0;
		nodes[i].left = 0;
		nodes[i].right = 0;
	}
	return;
}

int getHeight(int node){
	int ret;
	if (!nodes[node].is_null) {
		ret = nodes[node].height;
		return ret;
	}
	ret = -1;
	return ret;
}

int leftLeftRotation(int node){
	int temp = nodes[node].left, p1, p2;
	nodes[node].left = nodes[nodes[node].left].right;
	nodes[temp].right = node;

	p1 = getHeight(nodes[node].left);
	p2 = getHeight(nodes[node].right);
	nodes[node].height = max(p1, p2) + 1;
	p1 = getHeight(nodes[temp].left);
	p2 = getHeight(nodes[temp].right);
	nodes[temp].height = max(p1, p2) + 1;
	return temp;
}

int rightRightRotation(int node){
	int temp = nodes[node].right, p1, p2;
	nodes[node].right = nodes[nodes[node].right].left;
	nodes[temp].left = node;

	p1 = getHeight(nodes[node].left);
	p2 = getHeight(nodes[node].right);
	nodes[node].height = max(p1, p2) + 1;
	p1 = getHeight(nodes[temp].left);
	p2 = getHeight(nodes[temp].right);
	nodes[temp].height = max(p1, p2) + 1;
	return temp;
}

int leftRightRotation(int node){
	int ret;
	nodes[node].left = rightRightRotation(nodes[node].left);
	ret = leftLeftRotation(node);
	return ret;
}

int rightLeftRotation(int node){
	int ret;
	nodes[node].right = leftLeftRotation(nodes[node].right);
	ret = rightRightRotation(node);
	return ret;
}

int insert(int node, int elem){
	if(nodes[node].is_null){
		int i = avai;
		while(!nodes[i].is_null) {i = i + 1;}
		nodes[i].is_null = 0;
		nodes[i].elem = elem;
		avai = i + 1;
		return i;
	}else if(elem < nodes[node].elem){
		nodes[node].left = insert(nodes[node].left, elem);
		nodes[node].height = max(nodes[nodes[node].left].height, nodes[nodes[node].right].height) + 1;
		if (getHeight(nodes[node].left) - getHeight(nodes[node].right) == 2){
			if (elem < nodes[nodes[node].left].elem) {
				node = leftLeftRotation(node);
			}
			else {
				node = leftRightRotation(node);
			}
		}
		return node;
	}else if(elem > nodes[node].elem){
		nodes[node].right = insert(nodes[node].right, elem);
		nodes[node].height = max(nodes[nodes[node].left].height, nodes[nodes[node].right].height) + 1;
		if (getHeight(nodes[node].left) - getHeight(nodes[node].right) == -2){
			if (elem > nodes[nodes[node].right].elem) {
				node = rightRightRotation(node);
			}
			else {
				node = rightLeftRotation(node);
			}
		}
		return node;
	}
	return 0;
}

void addNode(int elem){
	root = insert(root, elem);
}

int search(int node, int elem){
	int ret;
	if(nodes[node].is_null) {
		return 0;
	}
	if(elem == nodes[node].elem) {
		return node;
	}
	else if(elem < nodes[node].elem) {
		ret = search(nodes[node].left, elem);
		return ret;
	}
	else {
		ret = search(nodes[node].right, elem);
		return ret;
	}
}

int searchNode(int elem){
	int ret;
	ret = search(root, elem);
	return ret;
}



void removeNode(int elem){
	return;
}

void printNode(int node){
	if(nodes[node].is_null){
		printf("NULL\n");
		return;
	}
	printf("%d left child is ", nodes[node].elem);
	if(nodes[nodes[node].left].is_null) {
		printf("NULL, right child is ");
	}
	else {
		printf("%d, right child is ", nodes[nodes[node].left].elem);
	}

	if(nodes[nodes[node].right].is_null) {
		printf("NULL\n");
	}
	else{
		printf("%d\n", nodes[nodes[node].right].elem);
	}
	return;
}

void printAVL(int node){
	if(nodes[node].is_null) {
		return;
	}
	printNode(node);
    printAVL(nodes[node].left);
    printAVL(nodes[node].right);
    return;
}

int main(){
	int n, i, elem, comm;
	initTree();

	while(1){
		scanf("%d %d", &comm, &elem);
		if(comm == 0){
			addNode(elem);
			printAVL(root);
		}
		else if(comm == 1){
			removeNode(elem);
			printAVL(root);
		}
		else if(comm == 2) {
			printNode(searchNode(elem));
		}
		
	}
	return 0;
}
