from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleCParser import simpleCParser
else:
    from simpleCParser import simpleCParser

from simpleCVisitor import simpleCVisitor

class Visitor(simpleCVisitor):

    def __init__(self):
        super(simpleCVisitor, self).__init__()
        self.constants = []
        self.functions = dict()
        self.var_cnt = 0
        self.label_cnt = 0
        

    def visitChildren(self, ctx, filling = '\n'):
        ret = { 'prepare': '', 'content': '' }
        total = ctx.getChildCount()
        # print(total)
        for index in range(total):
            res = self.visit(ctx.getChild(index))
            # print(res)
            ret['prepare'] += res['prepare']
            ret['content'] += res['content']
            if index < total-1:
                ret['content'] += filling
        return ret
    
    # Visit a parse tree produced by simpleCParser#prog.
    def visitProg(self, ctx:simpleCParser.ProgContext):
        ret = self.visitChildren(ctx)
        for value in self.constants:
            ret['content'] += value
        for value in self.functions.values():
            ret['content'] += value
        return ret


    # Visit a parse tree produced by simpleCParser#include.
    def visitInclude(self, ctx:simpleCParser.IncludeContext):
        # return self.visitChildren(ctx)
        return {'prepare': '', 'content': ''}


    # Visit a parse tree produced by simpleCParser#mFunction.
    def visitMFunction(self, ctx:simpleCParser.FunctionContext):
        # return self.visitChildren(ctx)
        ret = { 'prepare': '', 'content': 'define ' }
        res = self.visit(ctx.getChild(0))  # return type
        ret['content'] += res['content']
        ret['content'] += ' @'
        res = self.visit(ctx.getChild(1))  # function name
        ret['content'] += res['content']
        ret['content'] += '('
        res = self.visit(ctx.getChild(3))  # parmas
        ret['content'] += res['content']
        ret['content'] += ') {\n'
        res = self.visit(ctx.getChild(6))  # body
        ret['content'] += res['content']
        ret['content'] += '}\n'
        return ret


    # Visit a parse tree produced by simpleCParser#params.
    def visitParams(self, ctx:simpleCParser.ParamsContext):
        print('params')
        ret = { 'prepare': '', 'content': '' }
        total = ctx.getChildCount()
        if total == 0:
            return ret
        ret = self.visit(ctx.getChild(0))
        for index in range(2, total, 2):
            res = self.visit(ctx.getChild(index))
            ret['content'] += ', ' + res['content']
        return ret


    # Visit a parse tree produced by simpleCParser#param.
    def visitParam(self, ctx:simpleCParser.ParamContext):
        print('param')
        ret = { 'prepare': '', 'content': '' }
        res = self.visit(ctx.getChild(0)) # param type
        ret['content'] += res['content']
        res = self.visit(ctx.getChild(1)) # param name
        ret['content'] += ' %' + res['content']
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#funcBody.
    def visitFuncBody(self, ctx:simpleCParser.FuncBodyContext):
        print(ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#body.
    def visitBody(self, ctx:simpleCParser.BodyContext):
        print('visitBody')
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#block.
    def visitBlock(self, ctx:simpleCParser.BlockContext):
        print('visitBlock')
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
        print('ifBlocks')
        ret = {'prepare': '', 'content': ''}
        endif_label = self.label_cnt
        self.label_cnt += 1
        total = ctx.getChildCount()
        for index in range(total):
            res = self.visit(ctx.getChild(index))
            # ret['prepare'] += res['prepare']
            ret['content'] += res['content']
            ret['content'] += 'br label %%"label%d"\n' % endif_label
        ret['content'] += 'label%d:\n' % endif_label
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#ifBlock.
    def visitIfBlock(self, ctx:simpleCParser.IfBlockContext):
        print('ifBlock')
        ret = {'prepare': '', 'content': ''}
        labelIF = self.label_cnt
        labelELSE = self.label_cnt+1
        self.label_cnt += 2

        res = self.visit(ctx.getChild(2)) # condition
        ret['content'] = res['prepare'] + ret['content']
        ret['content'] += 'br i1 %s, label %%"label%d", label %%"label%d"\n' %\
                            (res['content'], labelIF, labelELSE)
        ret['content'] += 'label%d:\n' % labelIF

        res = self.visit(ctx.getChild(5)) # body
        ret['content'] += res['content']
        ret['content'] += 'label%d:\n' % labelELSE

        return ret


    # Visit a parse tree produced by simpleCParser#elifBlock.
    def visitElifBlock(self, ctx:simpleCParser.ElifBlockContext):
        print('elifBlock')
        ret = {'prepare': '', 'content': ''}
        labelIF = self.label_cnt
        labelELSE = self.label_cnt+1
        self.label_cnt += 2

        res = self.visit(ctx.getChild(3)) # condition
        ret['content'] = res['prepare'] + ret['content']
        ret['content'] += 'br i1 %s, label %%"label%d", label %%"label%d"\n' %\
                            (res['content'], labelIF, labelELSE)
        ret['content'] += 'label%d:\n' % labelIF

        res = self.visit(ctx.getChild(6)) # body
        ret['content'] += res['content']
        ret['content'] += 'label%d:\n' % labelELSE
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#elseBlock.
    def visitElseBlock(self, ctx:simpleCParser.ElseBlockContext):
        print('elseBlock')
        ret = {'prepare': '', 'content': ''}
        res = self.visit(ctx.getChild(2)) # body
        ret['content'] += res['content']
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#condition.
    def visitCondition(self, ctx:simpleCParser.ConditionContext):
        print('condition')
        ret = self.visit(ctx.getChild(0))
        total = ctx/getChildCount()
        for index in range(1, total, 2):
            res = self.visit(ctx.getChild(index+1))
            ret['prepare'] += res['prepare']
            if ctx.getChild(index).getText() == '&&':
                ret['prepare'] += '%%".%d" = and i1 %s, %s\n' % \
                                    (self.var_cnt, ret['content'], res['content'])
                ret['content'] = '%%".%d"' % self.var_cnt
                self.var_cnt += 1
            elif if ctx.getChild(index).getText() == '||':
                ret['prepare'] += '%%".%d" = or i1 %s, %s\n' % \
                                    (self.var_cnt, ret['content'], res['content'])
                ret['content'] = '%%".%d"' % self.var_cnt
                self.var_cnt += 1

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
        print('returnBlock')
        ret = { 'prepare': '', 'content': 'ret '}
        res = self.visit(ctx.getChild(1))
        ret['content'] = res['prepare'] + ret['content'] + res['content'] + '\n'
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
        print('Identifier' + ctx.getText())
        return ctx.getText()
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#parens.
    def visitParens(self, ctx:simpleCParser.ParensContext):
        # ret = self.visit(ctx.getChild(1)) + '\n'
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
        cont = self.visitChildren()
        return {
                'type': 'i32',
                'content': cont
                }


    # Visit a parse tree produced by simpleCParser#Judge.
    def visitJudge(self, ctx:simpleCParser.JudgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mType.
    def visitMType(self, ctx:simpleCParser.MTypeContext):
        # return self.visitChildren(ctx)
        # print(ctx.getText())
        print('mtype')
        _type = ctx.getText()
        if _type == 'int':
            return {'prepare': '', 'content': 'i32'}
        elif _type == 'char':
            return {'prepare': '', 'content': 'i8'}
        elif _type == 'double':
            return {'prepare': '', 'content': 'double'}
        return {'prepare': '', 'content': 'void'}


    # Visit a parse tree produced by simpleCParser#arrayItem.
    def visitArrayItem(self, ctx:simpleCParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#func.
    def visitFunc(self, ctx:simpleCParser.FuncContext):
        print("func")
        # ret = self.visitChildren(ctx)
        ret = self.visit(ctx.getChild(0))
        return ret


    # Visit a parse tree produced by simpleCParser#strlenFunc.
    def visitStrlenFunc(self, ctx:simpleCParser.StrlenFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#atoiFunc.
    def visitAtoiFunc(self, ctx:simpleCParser.AtoiFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#printfFunc.
    def visitPrintfFunc(self, ctx:simpleCParser.PrintfFuncContext):
        self.functions['printf'] = 'declare i32 @"printf"(i8* %".1", ...)'
        idx = len(self.constants)
        ret = { 'prepare': '', 'content': '' }
        if ctx.getChildCount() == 4:
            res = self.visit(ctx.getChild(2))
            # ret['prepare'] += res['prepare']
            ret['content'] += ('call i32 (i8*, ...) @"printf"(i8* %s)' % res['content'])
            ret['content'] = res['prepare'] + ret['content']
        else:
            pass
        return ret


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


    # Visit a parse tree produced by simpleCParser#mID.
    def visitMID(self, ctx:simpleCParser.MIDContext):
        ret =   {
                    'prepare': '',
                    'content': '"' + ctx.getText() + '"'
                }
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mINT.
    def visitMINT(self, ctx:simpleCParser.MINTContext):
        ret =   {
                    'prepare': '',
                    'content': "i32 " + ctx.getText()
                }
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mDOUBLE.
    def visitMDOUBLE(self, ctx:simpleCParser.MDOUBLEContext):
        ret =   {
                    'prepare': '',
                    'content': "double " + ctx.getText()
                }
        return ret


    # Visit a parse tree produced by simpleCParser#mCHAR.
    def visitMCHAR(self, ctx:simpleCParser.MCHARContext):
        ret =   {
                    'prepare': '',
                    'content': "i8 %d" % chr(ctx.getChild(1).getText()[0])
                }
        return ret

    def calc_len(self, st):
        Len = 0
        for index in range(len(st)):
            if index == 0 or st[index] == '\\' and st[index-1] != '\\':
                continue
            Len += 1
        return Len

    # Visit a parse tree produced by simpleCParser#mSTRING.
    def visitMSTRING(self, ctx:simpleCParser.MSTRINGContext):
        idx = len(self.constants)
        cont = ctx.getText().replace('\\n', '\\0A')
        Len = self.calc_len(cont)-2
        # print(ctx.getText())
        s = '@"str.%d" = constant [%d x i8] c%s\n' % (idx, Len, cont)
        # print(s)
        self.constants.append(s)
        # %".58" = getelementptr inbounds [6 x i8], [6 x i8]* @".str5", i32 0, i32 0
        prep = '%%".%d" = getelementptr inbounds [%d x i8], [%d x i8]* @"str.%d", i32 0, i32 0\n' % \
                (self.var_cnt, Len, Len, idx)
        self.var_cnt += 1
        return {
                'prepare': prep,
                'content': '%%".%d"' % (self.var_cnt-1)
                }


    # Visit a parse tree produced by simpleCParser#mLIB.
    def visitMLIB(self, ctx:simpleCParser.MLIBContext):
        return self.visitChildren(ctx)

del simpleCParser