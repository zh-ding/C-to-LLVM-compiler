import sys

from antlr4 import *
from simpleCParser import simpleCParser
from simpleCLexer import simpleCLexer
from simpleCListener import simpleCListener
from simpleCVisitor import simpleCVisitor

def main(argv):
    input = FileStream(argv[1])
    lexer = simpleCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = simpleCParser(stream)
    tree = parser.prog()
    v = simpleCVisitor()
    print(v.visit(tree))

if __name__ == '__main__':
    main(sys.argv)