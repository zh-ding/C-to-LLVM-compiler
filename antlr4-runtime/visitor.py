# Generated from simpleC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleCParser import simpleCParser
else:
    from simpleCParser import simpleCParser

from simpleCVisitor import simpleCVisitor
from llvmlite import ir

double = ir.DoubleType()
int1 = ir.IntType(1)
int32 = ir.IntType(32)
int8 = ir.IntType(8)
void = ir.VoidType()

# This class defines a complete generic visitor for a parse tree produced by simpleCParser.

class Visitor(simpleCVisitor):

    def __init__(self):
        super(simpleCVisitor, self).__init__()
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu" # llvm.Target.from_default_triple()
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128" # llvm.create_mcjit_compiler(backing_mod, target_machine)
        self.blocks = []
        self.builders = []
        self.local_vars = []
        self.global_vars = dict()
        self.functions = dict()
        self.cur_func = ''
        self.constants = 0
        self.need_load = True
        self.endifBlock = None
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
        self.functions[func_name] = func
        builder = ir.IRBuilder(block)
        self.blocks.append(block)
        self.builders.append(builder)
        varList = {}
        for index in range(len(params)):
            new_var = builder.alloca(params[index]['type'])
            builder.store(func.args[index], new_var)
            varList[params[index]['IDname']] = {
                'type': params[index]['type'],
                'name': new_var
            }
        self.local_vars.append(varList)
        self.cur_func = func_name

        self.visit(ctx.getChild(6)) # func body

        self.cur_func = ''
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
        type_ = self.visit(ctx.getChild(0))
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


    def assignConvert(self, a, dtype):
        if (a['type'] == dtype):
            return a
        if self.isInteger(a['type']) and self.isInteger(dtype):
            if (a['type'] == int1):
                a = self.convertIIZ(a, dtype)
            else:
                a = self.convertIIS(a, dtype)
        elif self.isInteger(a['type']) and dtype == double:
            a = self.convertIDS(a)
        elif self.isInteger(dtype) and a['type'] == double:
            a = self.convertDIS(a)
        return a

    # Visit a parse tree produced by simpleCParser#initialBlock.
    def visitInitialBlock(self, ctx:simpleCParser.InitialBlockContext):
        print('initialBlock')
        builder = self.builders[-1]
        varList = self.local_vars[-1]

        type_ = self.visit(ctx.getChild(0))
        total = ctx.getChildCount()
        index = 1
        while (index < total):
            IDname = ctx.getChild(index).getText()
            if IDname in varList:   # error!
                pass
            new_var = builder.alloca(type_, name=IDname)
            varList[IDname] = {
                'type': type_,
                'name': new_var
            }
            if ctx.getChild(index+1).getText() != '=':
                index += 2
            else:
                res = self.visit(ctx.getChild(index+2))
                res = self.assignConvert(res, type_)
                builder.store(res['name'], new_var)
                index += 4
        return
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#arrayInitBlock.
    def visitArrayInitBlock(self, ctx:simpleCParser.ArrayInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#assignBlock.
    def visitAssignBlock(self, ctx:simpleCParser.AssignBlockContext):
        print('assignBlock')
        builder = self.builders[-1]
        total = ctx.getChildCount()
        # print(total)
        res = self.visit(ctx.getChild(total-2))

        rng = [i for i in range(0, total-2, 2)]
        rng = rng[::-1]
        # print(rng)
        for i in range(len(rng)):
            index = rng[i]
            self.need_load = False
            res1 = self.visit(ctx.getChild(index))
            self.need_load = True
            res = self.assignConvert(res, res1['type'])
            builder.store(res['name'], res1['name'])
            if index > 0:
                new_var = builder.load(res1['name'])
                res = {
                    'type': res1['type'],
                    'const': False,
                    'name': new_var
                }
        return res


    # Visit a parse tree produced by simpleCParser#ifBlocks.
    def visitIfBlocks(self, ctx:simpleCParser.IfBlocksContext):
        builder = self.builders[-1]
        total = ctx.getChildCount()
        ifblocks = builder.append_basic_block()
        endif = builder.append_basic_block()
        builder.branch(ifblocks)

        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(ifblocks)
        builder = ir.IRBuilder(ifblocks)
        self.builders.append(builder)

        tmp = self.endifBlock
        self.endifBlock = endif
        for index in range(total):
            self.visit(ctx.getChild(index))

        self.endifBlock = tmp

        bl = self.blocks.pop()
        bu = self.builders.pop()
        if not bl.is_terminated:
            bu.branch(endif)

        self.blocks.append(endif)
        self.builders.append(ir.IRBuilder(endif))
        return


    # Visit a parse tree produced by simpleCParser#ifBlock.
    def visitIfBlock(self, ctx:simpleCParser.IfBlockContext):
        res = self.visit(ctx.getChild(2))
        builder = self.builders[-1]
        new_block_true = builder.append_basic_block()
        new_block_false = builder.append_basic_block()
        builder.cbranch(res['name'], new_block_true, new_block_false)

        self.blocks.pop()
        self.builders.pop()

        self.blocks.append(new_block_true)
        self.builders.append(ir.IRBuilder(new_block_true))
        self.local_vars.append({})

        self.visit(ctx.getChild(5))

        builder = self.builders[-1]
        builder.branch(self.endifBlock)

        self.blocks.pop()
        self.builders.pop()
        self.local_vars.pop()

        self.blocks.append(new_block_false)
        self.builders.append(ir.IRBuilder(new_block_false))
        return


    # Visit a parse tree produced by simpleCParser#elifBlock.
    def visitElifBlock(self, ctx:simpleCParser.ElifBlockContext):
        res = self.visit(ctx.getChild(3))
        builder = self.builders[-1]
        new_block_true = builder.append_basic_block()
        new_block_false = builder.append_basic_block()
        builder.cbranch(res['name'], new_block_true, new_block_false)

        self.blocks.pop()
        self.builders.pop()

        self.blocks.append(new_block_true)
        self.builders.append(ir.IRBuilder(new_block_true))
        self.local_vars.append({})

        self.visit(ctx.getChild(6))

        builder = self.builders[-1]
        builder.branch(self.endifBlock)

        self.blocks.pop()
        self.builders.pop()
        self.local_vars.pop()

        self.blocks.append(new_block_false)
        self.builders.append(ir.IRBuilder(new_block_false))
        return


    # Visit a parse tree produced by simpleCParser#elseBlock.
    def visitElseBlock(self, ctx:simpleCParser.ElseBlockContext):
        self.local_vars.append({})

        self.visit(ctx.getChild(2))

        self.local_vars.pop()
        return


    # Visit a parse tree produced by simpleCParser#condition.
    def visitCondition(self, ctx:simpleCParser.ConditionContext):
        builder = self.builders[-1]
        ret = self.visit(ctx.getChild(0))
        ret = self.toBoolean(ret, notFlag=False)
        total = ctx.getChildCount()
        for index in range(1, total, 2):
            res = self.visit(ctx.getChild(index+1))
            res = self.toBoolean(res, notFlag=False)
            new_var = builder.and_(ret['name'], res['name'])
            ret  = {
                    'type': ret['type'],
                    'const': False,
                    'name': new_var
            }
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
        builder = self.builders[-1]
        res = self.visit(ctx.getChild(1))
        ret = builder.ret(res['name'])
        return {
                'type': void,
                'const': False,
                'name': ret
        }

    def convertIIZ(self, a, dtype):
        builder = self.builders[-1]
        new_var = builder.zext(a['name'], dtype)
        return {
                'type': dtype,
                'const': False,
                'name': new_var
        }

    def convertIIS(self, a, dtype):
        builder = self.builders[-1]
        new_var = builder.sext(a['name'], dtype)
        return {
                'type': dtype,
                'const': False,
                'name': new_var
        }

    def convertDIS(self, a, dtype):
        builder = self.builders[-1]
        new_var = builder.fptosi(a['name'], dtype)
        return {
                'type': dtype,
                'const': False,
                'name': new_var
        }

    def convertDIU(self, a, dtype):
        builder = self.builders[-1]
        new_var = builder.fptoui(a['name'], dtype)
        return {
                'type': dtype,
                'const': False,
                'name': new_var
        }

    def convertIDS(self, a):
        builder = self.builders[-1]
        new_var = builder.sitofp(a['name'], double)
        return {
                'type': double,
                'const': False,
                'name': new_var
        }

    def convertIDU(self, a):
        builder = self.builders[-1]
        new_var = builder.uitofp(a['name'], double)
        return {
                'type': double,
                'const': False,
                'name': new_var
        }

    def toBoolean(self, result, notFlag = True):
        if notFlag:
            op = '=='
        else:
            op = '!='
        builder = self.builders[-1]
        if result['type'] == int8 or result['type'] == int32:
            new_var = builder.icmp_signed(op, a['name'], ir.Constant(result['type'], 0))
            return {
                    'tpye': int1,
                    'const': False,
                    'name': new_var
            }
        elif result['type'] == double:
            new_var = builder.fcmp_ordered(op, a['name'], ir.Constant(double, 0))
            return {
                    'tpye': int1,
                    'const': False,
                    'name': new_var
            }
        return result

    # Visit a parse tree produced by simpleCParser#Neg.
    def visitNeg(self, ctx:simpleCParser.NegContext):
        res = self.visit(ctx.getChild(0))
        res = self.toBoolean(res, notFlag = True)
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#identifier.
    def visitIdentifier(self, ctx:simpleCParser.IdentifierContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#parens.
    def visitParens(self, ctx:simpleCParser.ParensContext):
        return self.visit(ctx.getChild(1))


    # Visit a parse tree produced by simpleCParser#arrayietm.
    def visitArrayietm(self, ctx:simpleCParser.ArrayietmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#string.
    def visitString(self, ctx:simpleCParser.StringContext):
        return self.visit(ctx.getChild(0))


    def isInteger(self, typ):
        return hasattr(typ, 'width')


    def exprConvert(self, a, b):
        if a['type'] == b['type']:
            return a, b
        if self.isInteger(a['type']) and self.isInteger(b['type']):
            if a['type'].width < b['type'].width:
                if a['type'].width == 1:
                    a = self.convertIIZ(a, b['type'])
                else:
                    a = self.convertIIS(a, b['type'])
            else:
                if b['type'].width == 1:
                    b = self.convertIIZ(b, a['type'])
                else:
                    b = self.convertIIS(b, a['type'])
        elif self.isInteger(a['type']) and b['type'] == double:
            a = convertIDS(a, b['type'])
        elif self.isInteger(b['type']) and a['type'] == double:
            b = convertIDS(b, a['type'])
        else:
            pass
        return a, b


    # Visit a parse tree produced by simpleCParser#MulDiv.
    def visitMulDiv(self, ctx:simpleCParser.MulDivContext):
        builder = self.builders[-1]
        res1 = self.visit(ctx.getChild(0))
        res2 = self.visit(ctx.getChild(2))
        res1, res2 = self.exprConvert(res1, res2)
        if ctx.getChild(1).getText() == '*':
            new_var = builder.mul(res1['name'], res2['name'])
        elif ctx.getChild(1).getText() == '/':
            new_var = builder.sdiv(res1['name'], res2['name'])
        elif ctx.getChild(1).getText() == '%':
            new_var = builder.srem(res1['name'], res2['name'])
        return {
                'type': res1['type'],
                'const': False,
                'name': new_var
        }


    # Visit a parse tree produced by simpleCParser#AddSub.
    def visitAddSub(self, ctx:simpleCParser.AddSubContext):
        builder = self.builders[-1]
        res1 = self.visit(ctx.getChild(0))
        res2 = self.visit(ctx.getChild(2))
        res1, res2 = self.exprConvert(res1, res2)
        if ctx.getChild(1).getText() == '+':
            new_var = builder.add(res1['name'], res2['name'])
        elif ctx.getChild(1).getText() == '-':
            new_var = builder.sub(res1['name'], res2['name'])
        return {
                'type': res1['type'],
                'const': False,
                'name': new_var
        }


    # Visit a parse tree produced by simpleCParser#double.
    def visitDouble(self, ctx:simpleCParser.DoubleContext):
        if ctx.getChild(0).getText() == '-':
            res = self.visit(ctx.getChild(1))
            new_var = builder.neg(res['name'])
            return {
                    'type': res['type'],
                    'name': new_var
            }
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#function.
    def visitFunction(self, ctx:simpleCParser.FunctionContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#char.
    def visitChar(self, ctx:simpleCParser.CharContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#int.
    def visitInt(self, ctx:simpleCParser.IntContext):
        if ctx.getChild(0).getText() == '-':
            res = self.visit(ctx.getChild(1))
            new_var = builder.neg(res['name'])
            return {
                    'type': res['type'],
                    'name': new_var
            }
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#Judge.
    def visitJudge(self, ctx:simpleCParser.JudgeContext):
        builder = self.builders[-1]
        res1 = self.visit(ctx.getChild(0))
        res2 = self.visit(ctx.getChild(2))
        res1, res2 = self.exprConvert(res1, res2)
        op = ctx.getChild(1).getText()
        if res1['type'] == double:
            new_var = builder.fcmp_ordered(op, res1['name'], res2['name'])
        elif self.isInteger(res1['type']):
            new_var = builder.icmp_signed(op, res1['name'], res2['name'])
        return {
                'type': int1,
                'const': False,
                'name': new_var
        }


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
        return self.visit(ctx.getChild(0))
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
        # print(ctx.getChildCount())
        # print(ctx.getText())
        if ctx.getChildCount() == 4:
            res = self.visit(ctx.getChild(2))
            arg = builder.gep(res['name'], [zero, index], inbounds=True)
            ret = builder.call(printf, [arg])
        else:
            res = self.visit(ctx.getChild(2))
            args = [builder.gep(res['name'], [zero, index], inbounds=True)]

            total = ctx.getChildCount()
            for index in range(4, total-1, 2):
                res = self.visit(ctx.getChild(index))
                # print(res)
                args.append(res['name'])
            ret = builder.call(printf, args)
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
        print('selfDefinedFunc')
        # print(ctx.getText())
        builder = self.builders[-1]
        func_name = ctx.getChild(0).getText() # func name
        if func_name in self.functions:
            func = self.functions[func_name]
            # ret_type = self.functions[functions]

            total = ctx.getChildCount()
            # print(total-1)
            params = []
            for index in range(2, total-1, 2):
                res = self.visit(ctx.getChild(index))
                res = self.assignConvert(res, func.args[index//2-1].type)
                params.append(res['name'])
            new_var = builder.call(func, params)
            return {
                    'type': func.function_type.return_type,
                    'const': False,
                    'name': new_var
            }
        else:
            pass
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleCParser#argument.
    def visitArgument(self, ctx:simpleCParser.ArgumentContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by simpleCParser#mID.
    def visitMID(self, ctx:simpleCParser.MIDContext):
        IDname = ctx.getText()
        builder = self.builders[-1]
        total = len(self.local_vars)
        for index in range(total):
            varList = self.local_vars[total-1-index]
            if IDname in varList:
                if self.need_load:
                    var = builder.load(varList[IDname]['name'])
                    return {
                            'type': varList[IDname]['type'],
                            'const': False,
                            'name': var
                    }
                else:
                    return {
                            'type': varList[IDname]['type'],
                            'const': False,
                            'name': varList[IDname]['name']
                    }
        if IDname in self.global_vars:
            if self.need_load:
                var = builder.load(self.global_vars[IDname]['name'])
                return {
                        'type': self.global_vars[IDname]['type'],
                        'const': False,
                        'name': var
                }
            else:
                return {
                        'type': self.global_vars[IDname]['type'],
                        'const': False,
                        'name': self.global_vars[IDname]['name']
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
                'type': int32,
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
        # print(ctx.getChild(1).getText())
        return {
                'type': int8,
                'const': True,
                'name': ir.Constant(int8, ord(ctx.getText()[1]))
        }


    # Visit a parse tree produced by simpleCParser#mSTRING.
    def visitMSTRING(self, ctx:simpleCParser.MSTRINGContext):
        idx = self.constants
        self.constants += 1
        cont = ctx.getText().replace('\\n', '\n')
        cont = cont[1:-1]
        cont += '\0'
        # print(cont)
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



del simpleCParser