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
        ret = { 'prepare': '', 'content': '', 'type': 'void' }
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
        return {'prepare': '', 'content': '', 'type': 'void'}


    # Visit a parse tree produced by simpleCParser#mFunction.
    def visitMFunction(self, ctx:simpleCParser.FunctionContext):
        # return self.visitChildren(ctx)
        ret = { 'prepare': '', 'content': 'define ', 'type': 'void' }
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
        ret = { 'prepare': '', 'content': '', 'type': 'void' }
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
        ret = { 'prepare': '', 'content': '', 'type': 'void' }
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
        print('initialBlock')
        ret = {'prepare': '', 'content': '', 'type': 'void'}
        total = ctx.getChildCount()
        _type = self.visit(ctx.getChild(0))
        index = 1
        while index < total:
            res = self.visit(ctx.getChild(index))
            var_name = res['content']
            ret['content'] += '%%%s = alloca %s\n' % (var_name, _type['content'])
            if ctx.getChild(index+1).getText() != '=':
                index += 2
            else:
                res = self.visit(ctx.getChild(index+2))
                ret['content'] += res['prepare']
                ret['content'] += 'store i32 %%%s, %s* %s\n' %(res['content'], _type['content'], var_name)
                index += 4
        return ret

    # Visit a parse tree produced by simpleCParser#arrayInitBlock.
    def visitArrayInitBlock(self, ctx:simpleCParser.ArrayInitBlockContext):
        print('arrayInitBlock')
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#assignBlock.
    def visitAssignBlock(self, ctx:simpleCParser.AssignBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#ifBlocks.
    def visitIfBlocks(self, ctx:simpleCParser.IfBlocksContext):
        print('ifBlocks')
        ret = {'prepare': '', 'content': '', 'type': 'void'}
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
        ret = {'prepare': '', 'content': '', 'type': 'void'}
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
        ret = {'prepare': '', 'content': '', 'type': 'void'}
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
        ret = {'prepare': '', 'content': '', 'type': 'void'}
        res = self.visit(ctx.getChild(2)) # body
        ret['content'] += res['content']
        return ret
        # return self.visitChildren(ctx)

    def toBoolean(self, result):
        if (result['type'] != 'i1'):
            result['prepare'] += '%%".%d" = icmp ne %s %s, 0\n' % (self.var_cnt, ret['type'], ret['content'])
            result['type'] = 'i1'
            result['content'] = '%%".%d"' % self.var_cnt
            self.var_cnt += 1
        return result

    # Visit a parse tree produced by simpleCParser#condition.
    def visitCondition(self, ctx:simpleCParser.ConditionContext):
        print('condition')
        ret = self.visit(ctx.getChild(0))
        ret = self.toBoolean(ret)

        total = ctx/getChildCount()
        for index in range(1, total, 2):
            res = self.visit(ctx.getChild(index+1))
            res = self.toBoolean(res)
            ret['prepare'] += res['prepare']
            if ctx.getChild(index).getText() == '&&':
                ret['prepare'] += '%%".%d" = and i1 %s, %s\n' % \
                                    (self.var_cnt, ret['content'], res['content'])
                ret['content'] = '%%".%d"' % self.var_cnt
                self.var_cnt += 1
            elif ctx.getChild(index).getText() == '||':
                ret['prepare'] += '%%".%d" = or i1 %s, %s\n' % \
                                    (self.var_cnt, ret['content'], res['content'])
                ret['content'] = '%%".%d"' % self.var_cnt
                self.var_cnt += 1

        return ret


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
        ret = { 'prepare': '', 'content': 'ret ', 'type': 'void'}
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
        ret = { 'prepare': '', 'content': '', 'type': 'i1' }
        res = self.visit(ctx.getChild(1))
        res = self.toBoolean(res)
        ret['prepare'] += res['prepare']
        ret['prepare'] += '%%".%d" = xor i1 %s, true\n' % (self.var_cnt, res['content'])
        ret['content'] += '%%".%d"' % self.var_cnt
        self.var_cnt += 1
        return ret


    # Visit a parse tree produced by simpleCParser#identifier.
    def visitIdentifier(self, ctx:simpleCParser.IdentifierContext):
        print('Identifier' + ctx.getText())
        return ctx.getText()
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#parens.
    def visitParens(self, ctx:simpleCParser.ParensContext):
        return self.visit(ctx.getChild(1))


    # Visit a parse tree produced by simpleCParser#arrayietm.
    def visitArrayietm(self, ctx:simpleCParser.ArrayietmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#string.
    def visitString(self, ctx:simpleCParser.StringContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'i8*',
                'prepare': '',
                'content': ctx.STRING().getText()
                }

    def convertIIZ(self, a, dtype):
        a['prepare'] += '%%".%d" = zext %s %s to %s\n' % \
                        (self.var_cnt, a['type'], a['content'], dtype)
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = dtype
        self.var_cnt += 1
        return a

    def convertIIS(self, a, dtype):
        a['prepare'] += '%%".%d" = sext %s %s to %s\n' % \
                        (self.var_cnt, a['type'], a['content'], dtype)
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = dtype
        self.var_cnt += 1
        return a

    def convertIDS(self, a):
        a['prepare'] += '%%".%d" = sitofp %s %s to double\n' % \
                        (self.var_cnt, a['type'], a['content'])
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = 'double'
        self.var_cnt += 1
        return a

    def convertIDU(self, a):
        a['prepare'] += '%%".%d" = uitofp %s %s to double\n' % \
                        (self.var_cnt, a['type'], a['content'])
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = 'double'
        self.var_cnt += 1
        return a

    def convertDIS(self, a, dtype):
        a['prepare'] += '%%".%d" = fptosi double %s to %s\n' % \
                        (self.var_cnt, a['content'], dtype)
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = dtype
        self.var_cnt += 1
        return a

    def convertDIU(self, a, dtype):
        a['prepare'] += '%%".%d" = fptoui double %s to %s\n' % \
                        (self.var_cnt, a['content'], dtype)
        a['content'] = '%%".%d"' self.var_cnt
        a['type'] = dtype
        self.var_cnt += 1
        return a

    def isInteger(self, tp):
        return tp.startswith('i') and tp[1:].isdigit()

    def exprConvert(self, a, b):
        if a['type'] == b['type']:
            return a, b
        if self.isInteger(a['type']) and self.isInteger(b['type']):
            bita = int(a['type'][1:])
            bitb = int(b['type'][1:])
            if bita > bitb:
                if (bitb == 1):
                    b = self.convertIIZ(b, a['type'])
                else:
                    b = self.convertIIS(b, a['type'])
            else:
                if (bita == 1):
                    a = self.convertIIZ(a, b['type'])
                else:
                    a = self.convertIIS(a, b['type'])
            return a, b
        elif a['type'] == 'double' and self.isInteger(b['type']):
            if (b['type'] == 'i1'):
                b = self.convertIDU(b)
            else:
                b = self.convertIDS(b)
            return a, b
        elif b['type'] == 'double' and self.isInteger(a['type']):
            if (a['type'] == 'i1'):
                a = self.convertIDU(a)
            else:
                a = self.convertIDS(a)
            return a, b
        return a, b


    # Visit a parse tree produced by simpleCParser#MulDiv.
    def visitMulDiv(self, ctx:simpleCParser.MulDivContext):
        ret = { 'prepare': '', 'content': '', 'type': 'void' }
        res1 = self.visit(ctx.getChild(0))
        res2 = self.visit(ctx.getChild(2))
        res1, res2 = self.exprConvert(res1, res2)
        ret['type'] = res1['type']
        ret['prepare'] = res1['prepare'] + res2['prepare']
        if (ctx.getChild(1).getText() == '*'):
            ret['prepare'] = '%%".%d" = mul %s %s, %s' % (self.var_cnt, res1['type'], res1['content'], res2['content'])
            ret['content'] = '%%".%d"' % self.var_cnt
            self.var_cnt += 1
        elif (ctx.getChild(1).getText() == '/'):
            if res1['type'] == 'double':
                op = 'fdiv'
            else:
                op = 'sdiv'
            ret['prepare'] = '%%".%d" = %s %s %s, %s' % (self.var_cnt, op, res1['type'], res1['content'], res2['content'])
            ret['content'] = '%%".%d"' % self.var_cnt
            self.var_cnt += 1
        elif (ctx.getChild(1).getText() == '%'):
            if res1['type'] == 'double':
                op = 'frem'
            else:
                op = 'srem'
            ret['prepare'] = '%%".%d" = %s %s %s, %s' % (self.var_cnt, op, res1['type'], res1['content'], res2['content'])
            ret['content'] = '%%".%d"' % self.var_cnt
            self.var_cnt += 1
        return ret


    # Visit a parse tree produced by simpleCParser#AddSub.
    def visitAddSub(self, ctx:simpleCParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#double.
    def visitDouble(self, ctx:simpleCParser.DoubleContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'double',
                'prepare': '',
                'content': ctx.DOUBLE().getText()
                }


    # Visit a parse tree produced by simpleCParser#function.
    def visitFunction(self, ctx:simpleCParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#char.
    def visitChar(self, ctx:simpleCParser.CharContext):
        # return self.visitChildren(ctx)
        return {
                'type': 'i8',
                'prepare': '',
                'content': ctx.CHAR().getText()
                }


    # Visit a parse tree produced by simpleCParser#int.
    def visitInt(self, ctx:simpleCParser.IntContext):
        # return self.visitChildren(ctx)
        cont = self.visitChildren()
        return {
                'type': 'i32',
                'prepare': '',
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
            return {'prepare': '', 'content': 'i32', 'type': 'void'}
        elif _type == 'char':
            return {'prepare': '', 'content': 'i8', 'type': 'void'}
        elif _type == 'double':
            return {'prepare': '', 'content': 'double', 'type': 'void'}
        return {'prepare': '', 'content': 'void', 'type': 'void'}


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
        ret = { 'prepare': '', 'content': '', 'type': 'i32'}
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
                    'type': 'void',
                    'prepare': '',
                    'content': '"' + ctx.getText() + '"'
                }
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mINT.
    def visitMINT(self, ctx:simpleCParser.MINTContext):
        ret =   {
                    'type': 'i32',
                    'prepare': '',
                    'content': "i32 " + ctx.getText()
                }
        return ret
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mDOUBLE.
    def visitMDOUBLE(self, ctx:simpleCParser.MDOUBLEContext):
        ret =   {
                    'type': 'double',
                    'prepare': '',
                    'content': "double " + ctx.getText()
                }
        return ret


    # Visit a parse tree produced by simpleCParser#mCHAR.
    def visitMCHAR(self, ctx:simpleCParser.MCHARContext):
        ret =   {
                    'type': 'i8',
                    'prepare': '',
                    'content': "i8 %d" % ord(ctx.getChild(1).getText()[0])
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
                'type': 'i8*',
                'prepare': prep,
                'content': '%%".%d"' % (self.var_cnt-1)
                }


    # Visit a parse tree produced by simpleCParser#mLIB.
    def visitMLIB(self, ctx:simpleCParser.MLIBContext):
        return self.visitChildren(ctx)

del simpleCParser