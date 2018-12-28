from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleCParser import simpleCParser
else:
    from simpleCParser import simpleCParser

from simpleCVisitor import simpleCVisitor

class Visitor(simpleCVisitor):

    def __init__(self):
        super(simpleCVisitor, self).__init__()
        self.result_code = ''

    def visitChildren(self, ctx, filling = '\n'):
        ret = ''
        total = ctx.getChildCount()
        for index in range(total):
            ret += self.visit(ctx.getChild(index))
            if index < total-1:
                ret += filling
        return ret
    
    # Visit a parse tree produced by simpleCParser#prog.
    def visitProg(self, ctx:simpleCParser.ProgContext):
        ret = self.visitChildren(ctx)
        print(ret)
        return ret


    # Visit a parse tree produced by simpleCParser#include.
    def visitInclude(self, ctx:simpleCParser.IncludeContext):
        # return self.visitChildren(ctx)
        return


    # Visit a parse tree produced by simpleCParser#mFunction.
    def visitFunction(self, ctx:simpleCParser.FunctionContext):
        # return self.visitChildren(ctx)
        ret = 'define '
        ret += self.visit(ctx.getChild(0))
        ret += '@'
        ret += self.visit(ctx.getChild(1))
        ret += '('
        ret += self.visit(ctx.getChild(3))
        ret += ') {\n'
        ret += self.visit(ctx.getChild(6))
        ret += '}'
        return ret


    # Visit a parse tree produced by simpleCParser#params.
    def visitParams(self, ctx:simpleCParser.ParamsContext):
        return self.visitChildren(ctx, ', ')


    # Visit a parse tree produced by simpleCParser#param.
    def visitParam(self, ctx:simpleCParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#funcBody.
    def visitFuncBody(self, ctx:simpleCParser.FuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#body.
    def visitBody(self, ctx:simpleCParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#block.
    def visitBlock(self, ctx:simpleCParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#initialBlock.
    def visitInitialBlock(self, ctx:simpleCParser.InitialBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#arrayInitBlock.
    def visitArrayInitBlock(self, ctx:simpleCParser.ArrayInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#assignBlock.
    def visitAssignBlock(self, ctx:simpleCParser.AssignBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#ifBlocks.
    def visitIfBlocks(self, ctx:simpleCParser.IfBlocksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#ifBlock.
    def visitIfBlock(self, ctx:simpleCParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#elifBlock.
    def visitElifBlock(self, ctx:simpleCParser.ElifBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#elseBlock.
    def visitElseBlock(self, ctx:simpleCParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#condition.
    def visitCondition(self, ctx:simpleCParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#whileBlock.
    def visitWhileBlock(self, ctx:simpleCParser.WhileBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#forBlock.
    def visitForBlock(self, ctx:simpleCParser.ForBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#for1Block.
    def visitFor1Block(self, ctx:simpleCParser.For1BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#for3Block.
    def visitFor3Block(self, ctx:simpleCParser.For3BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#returnBlock.
    def visitReturnBlock(self, ctx:simpleCParser.ReturnBlockContext):
        ret = 'ret '
        res = self.visit(ctx.getChild(1))
        print(res)
        # if isinstance(res, dict):
        #     ret += res['type'] + ' '
        #     ret += res['content'] + '\n'
        # else:
        #     ret += res + '\n'
        return ret


    # Visit a parse tree produced by simpleCParser#Neg.
    def visitNeg(self, ctx:simpleCParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#identifier.
    def visitIdentifier(self, ctx:simpleCParser.IdentifierContext):
        print(ctx.getText())
        return ctx.getText()
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#parens.
    def visitParens(self, ctx:simpleCParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#arrayietm.
    def visitArrayietm(self, ctx:simpleCParser.ArrayietmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#string.
    def visitString(self, ctx:simpleCParser.StringContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'string',
                'content': ctx.STRING().getText()
                }


    # Visit a parse tree produced by simpleCParser#MulDiv.
    def visitMulDiv(self, ctx:simpleCParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#AddSub.
    def visitAddSub(self, ctx:simpleCParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#double.
    def visitDouble(self, ctx:simpleCParser.DoubleContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'double',
                'content': ctx.DOUBLE().getText()
                }


    # Visit a parse tree produced by simpleCParser#function.
    def visitFunction(self, ctx:simpleCParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#char.
    def visitChar(self, ctx:simpleCParser.CharContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'char',
                'content': ctx.CHAR().getText()
                }


    # Visit a parse tree produced by simpleCParser#int.
    def visitInt(self, ctx:simpleCParser.IntContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'i32',
                'content': ctx.CHAR().getText()
                }


    # Visit a parse tree produced by simpleCParser#Judge.
    def visitJudge(self, ctx:simpleCParser.JudgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mType.
    def visitMType(self, ctx:simpleCParser.MTypeContext):
        # return self.visitChildren(ctx)
        # print(ctx.getText())
        return ctx.getText()


    # Visit a parse tree produced by simpleCParser#arrayItem.
    def visitArrayItem(self, ctx:simpleCParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#func.
    def visitFunc(self, ctx:simpleCParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#strlenFunc.
    def visitStrlenFunc(self, ctx:simpleCParser.StrlenFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#atoiFunc.
    def visitAtoiFunc(self, ctx:simpleCParser.AtoiFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#printfFunc.
    def visitPrintfFunc(self, ctx:simpleCParser.PrintfFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#scanfFunc.
    def visitScanfFunc(self, ctx:simpleCParser.ScanfFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#getsFunc.
    def visitGetsFunc(self, ctx:simpleCParser.GetsFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#selfDefinedFunc.
    def visitSelfDefinedFunc(self, ctx:simpleCParser.SelfDefinedFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#argument.
    def visitArgument(self, ctx:simpleCParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mINT.
    def visitMINT(self, ctx:simpleCParser.MINTContext):
        return "i32 " + ctx.getText()
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mCHAR.
    def visitMCHAR(self, ctx:simpleCParser.MCHARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mDOUBLE.
    def visitMDOUBLE(self, ctx:simpleCParser.MDOUBLEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mSTRING.
    def visitMSTRING(self, ctx:simpleCParser.MSTRINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mLIB.
    def visitMLIB(self, ctx:simpleCParser.MLIBContext):
        return self.visitChildren(ctx)

del simpleCParser