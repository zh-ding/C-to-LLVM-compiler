# C-to-LLVM-compiler

## 环境

* 系统：Ubuntu18.04
* 语言：Python3.6

## 安装

安装[antlr4](https://www.antlr.org/)。

安装antlr4-python3-runtime

```
pip install antlr4-python3-runtime
```

安装llvmlite

```
pip install llvmlite
```

## 使用

生成LLVM IR代码

```
python antlr4-runtime/parse.py source.c [output.ll]
```

运行LLVM IR代码

```
lli output.ll
```

## 测试用例

1、`testcases/palindrome.c`回文检测

2、`testcases/KMP.c`字符串搜索

3、`testcases/calc.c`四则运算计算器

4、`testcases/AVLtree.c`平衡树