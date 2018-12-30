import sys

from antlr4 import *
from simpleCParser import simpleCParser
from simpleCLexer import simpleCLexer
from simpleCListener import simpleCListener
from simpleCVisitor import simpleCVisitor
from visitor import Visitor

def main(argv):
    input = FileStream(argv[1])
    lexer = simpleCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = simpleCParser(stream)
    tree = parser.prog()
    # v = simpleCVisitor()
    v = Visitor()
    v.visit(tree)
    if (len(argv) >= 3):
    	open(argv[2], 'w').write(v.module)
    else:
    	print(v.module)

if __name__ == '__main__':
    main(sys.argv)