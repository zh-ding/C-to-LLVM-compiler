# Generated from simpleC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleCParser import simpleCParser
else:
    from simpleCParser import simpleCParser

from simpleCVisitor import simpleCVisitor
from llvmlite import ir

double = ir.DoubleType()
int32 = ir.IntType(32)
int8 = ir.IntType(8)
void = ir.VoidType()

# This class defines a complete generic visitor for a parse tree produced by simpleCParser.

class Visitor(simpleCVisitor):

    def __init__(self):
        super(simpleCVisitor, self).__init__()
        self.module = ir.Module()
        self.blocks = []
        self.builders = []
        self.local_vars = []
        self.global_vars = dict()
        self.functions = dict()
        self.constants = 0
        # self.var_cnt = 0
        # self.label_cnt = 0

    # Visit a parse tree produced by simpleCParser#prog.
    def visitProg(self, ctx:simpleCParser.ProgContext):
        total = ctx.getChildCount()
        for index in range(total):
            self.visit(ctx.getChild(index))
        return
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#include.
    def visitInclude(self, ctx:simpleCParser.IncludeContext):
        return


    # Visit a parse tree produced by simpleCParser#mFunction.
    def visitMFunction(self, ctx:simpleCParser.MFunctionContext):
        return_type = self.visit(ctx.getChild(0)) # mtype
        func_name = ctx.getChild(1).getText() # func name
        params = self.visit(ctx.getChild(3)) # func params

        params_type = []
        for index in range(len(params)):
            params_type.append(params[index]['type'])
        funcProto = ir.FunctionType(return_type, params_type)
        func = ir.Function(self.module, funcProto, name=func_name)
        for index in range(len(params)):
            func.args[index].name = params[index]['IDname']
        block = func.append_basic_block(name=func_name+'.entry')
        builder = ir.IRBuilder(block)
        self.blocks.append(block)
        self.builders.append(builder)
        varList = {}
        for index in range(len(params)):
            varList[params[index]['IDname']] = {
                'type': params[index]['type'],
                'name': func.args[index]
            }
        self.local_vars.append(varList)

        self.visit(ctx.getChild(6)) # func body

        self.blocks.pop()
        self.builders.pop()
        self.local_vars.pop()
        return


    # Visit a parse tree produced by simpleCParser#params.
    def visitParams(self, ctx:simpleCParser.ParamsContext):
        total = ctx.getChildCount()
        if (total == 0):
            return []
        ret = [self.visit(ctx.getChild(0))]
        for index in range(2, total, 2):
            ret.append(self.visit(ctx.getChild(index)))
        return ret


    # Visit a parse tree produced by simpleCParser#param.
    def visitParam(self, ctx:simpleCParser.ParamContext):
        type_ = ctx.visit(ctx.getChild(0))
        IDname = ctx.getChild(1).getText()
        return {
                'type': type_,
                'IDname': IDname
        }


    # Visit a parse tree produced by simpleCParser#funcBody.
    def visitFuncBody(self, ctx:simpleCParser.FuncBodyContext):
        total = ctx.getChildCount()
        for index in range(total):
            self.visit(ctx.getChild(index))
        return
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#body.
    def visitBody(self, ctx:simpleCParser.BodyContext):
        total = ctx.getChildCount()
        for index in range(total):
            self.visit(ctx.getChild(index))
        return
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#block.
    def visitBlock(self, ctx:simpleCParser.BlockContext):
        total = ctx.getChildCount()
        for index in range(total):
            self.visit(ctx.getChild(index))
        return
        # return self.visitChildren(ctx)


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
        print('returnBlock')
        builder = self.builders[-1]
        res = self.visit(ctx.getChild(1))
        ret = builder.ret(res['name'])
        return {
                'type': void,
                'const': False,
                'name': ret
        }


    # Visit a parse tree produced by simpleCParser#Neg.
    def visitNeg(self, ctx:simpleCParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#identifier.
    def visitIdentifier(self, ctx:simpleCParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#parens.
    def visitParens(self, ctx:simpleCParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#arrayietm.
    def visitArrayietm(self, ctx:simpleCParser.ArrayietmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#string.
    def visitString(self, ctx:simpleCParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#MulDiv.
    def visitMulDiv(self, ctx:simpleCParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#AddSub.
    def visitAddSub(self, ctx:simpleCParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#double.
    def visitDouble(self, ctx:simpleCParser.DoubleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#function.
    def visitFunction(self, ctx:simpleCParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#char.
    def visitChar(self, ctx:simpleCParser.CharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#int.
    def visitInt(self, ctx:simpleCParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#Judge.
    def visitJudge(self, ctx:simpleCParser.JudgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#mType.
    def visitMType(self, ctx:simpleCParser.MTypeContext):
        if ctx.getText() == 'int':
            return int32
        if ctx.getText() == 'char':
            return int8
        if ctx.getText() == 'double':
            return double
        return void


    # Visit a parse tree produced by simpleCParser#arrayItem.
    def visitArrayItem(self, ctx:simpleCParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#func.
    def visitFunc(self, ctx:simpleCParser.FuncContext):
        self.visit(ctx.getChild(0))
        return
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#strlenFunc.
    def visitStrlenFunc(self, ctx:simpleCParser.StrlenFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#atoiFunc.
    def visitAtoiFunc(self, ctx:simpleCParser.AtoiFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#printfFunc.
    def visitPrintfFunc(self, ctx:simpleCParser.PrintfFuncContext):
        print('printfFunc')
        if 'printf' in self.functions:
            printf = self.functions['printf']
        else:
            printfty = ir.FunctionType(int32, [ir.PointerType(int8)], var_arg=True)
            printf = ir.Function(self.module, printfty, name="printf")
            self.functions['printf'] = printf

        builder = self.builders[-1]
        zero = ir.Constant(int32, 0)
        index = ir.Constant(int32, 0)
        if ctx.getChildCount() == 4:
            res = self.visit(ctx.getChild(2))
            arg = builder.gep(res['name'], [zero, index], inbounds=True)
            ret = builder.call(printf, [arg])
        else:
            pass
        return {
                'type': int32,
                'const': False,
                'name': ret
        }
        # return self.visitChildren(ctx)


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
        IDname = ctx.getText()
        builder = self.builders[-1]
        total = len(self.local_vars)
        for index in range(total):
            varList = self.local_vars[total-1-index]
            if IDname in varList:
                var = builder.load(varList[IDname]['name'])
                return {
                        'type': varList[IDname]['type'],
                        'const': False,
                        'name': var
                }
        if IDname in self.global_vars:
            var = builder.load(self.global_vars[IDname]['name'])
            return {
                    'type': self.global_vars[IDname]['type'],
                    'const': False,
                    'name': var
            }
        return {
                'type': void,
                'const': False,
                'name': ir.Constant(void, None)
        }


    # Visit a parse tree produced by simpleCParser#mINT.
    def visitMINT(self, ctx:simpleCParser.MINTContext):
        # idx = len(self.constants)
        # cont = ctx.getText().replace('\\n', '\\0A')
        # Len = self.calc_len(cont)-2

        # const = ir.GlobalVariable(module, ir.IntType(32), ".int%d"%idx)
        # const.initializer = ir.Constant(ir.IntType(32), int(ctx.getText()))
        # const.global_constant = True
        return {
                'type': 'i32',
                'const': True,
                'name': ir.Constant(int32, int(ctx.getText()))
        }


    # Visit a parse tree produced by simpleCParser#mDOUBLE.
    def visitMDOUBLE(self, ctx:simpleCParser.MDOUBLEContext):
        # return self.visitChildren(ctx)
        return {
                'type': double,
                'const': True,
                'name': ir.Constant(double, float(ctx.getText()))
        }


    # Visit a parse tree produced by simpleCParser#mCHAR.
    def visitMCHAR(self, ctx:simpleCParser.MCHARContext):
        return {
                'type': int8,
                'const': True,
                'name': ir.Constant(int8, ord(ctx.getChild(1).getText()[0]))
        }


    # Visit a parse tree produced by simpleCParser#mSTRING.
    def visitMSTRING(self, ctx:simpleCParser.MSTRINGContext):
        idx = self.constants
        self.constants += 1
        cont = ctx.getText().replace('\\n', '\n')
        cont = cont[1:-1]
        print(cont)
        # Len = self.calc_len(cont)
        Len = len(bytearray(cont, 'utf-8'))

        const = ir.GlobalVariable(self.module, ir.ArrayType(int8, Len), ".str%d"%idx)
        const.global_constant = True
        const.initializer = ir.Constant(ir.ArrayType(int8, Len), bytearray(cont, 'utf-8'))
        return {
                'type': ir.ArrayType(int8, Len),
                'const': False,
                'name': const
        }


    # Visit a parse tree produced by simpleCParser#mLIB.
    def visitMLIB(self, ctx:simpleCParser.MLIBContext):
        # return self.visitChildren(ctx)
        return


    def calc_len(self, st):
        Len = 0
        for index in range(len(st)):
            if index == 0 or st[index] == '\\' and st[index-1] != '\\':
                continue
            Len += 1
        return Len



del simpleCParser