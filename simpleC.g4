grammar simpleC;

prog :(include)* (function)*;
//prog : (whileBlock)*;

//-------------语法规则----------------------------------------------
include : '#include' '<' mLIB '>';

//函数
function : mType mID '(' params ')' '{' funcBody '}';

//函数参数
params : param (','param)* |;
param : mType mID;

//函数体
funcBody : body returnBlock;

//语句块/函数快
body : (block | func)*;

//语句块
block : initialBlock | arrayInitBlock | arrayNoInitBlock | assignBlock | ifBlocks | whileBlock;

//初始化语句
initialBlock : mType mID '=' expr ';';
arrayInitBlock : mType mID '[' mINT ']'';';
arrayNoInitBlock : mType mID '[' ']' ';';


//赋值语句
assignBlock : arrayItem '=' expr ';' |mID '=' expr ';' ;


//if 语句
ifBlocks : ifBlock (elifBlock)* (elseBlock)?;
ifBlock : 'if' '('condition')' '{' body '}';
elifBlock : 'else' 'if' '(' condition ')' '{' body '}';
elseBlock : 'else' '{' body '}';

condition :  expr (Conjunction expr)*;

//while 语句
whileBlock : 'while' '(' condition ')' '{' body '}';

//for 语句
forBlock : 'for' '(' initialBlock| assignBlock|mID| ',' condition ',' body| ')' '{' body '}';

//return 语句
returnBlock : 'return' + (mINT|mID) + ';';

expr
    : '(' expr ')'               #parens
    | op='!' expr                   #Neg
    | expr op=('*' | '/' | '%') expr   #MulDiv 
    | expr op=('+' | '-') expr   #AddSub
    | expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr #Judge
    | arrayItem                  #arrayietm
    | mINT                        #int                          
    | mDOUBLE                     #double
    | mCHAR                       #char
    | mSTRING                     #strig             
    | mID                         #mIDentifier                                        
    ;

mType : 'int'| 'double'| 'char'| 'string';

arrayItem : mID '[' expr ']';


//函数
func : strlenFunc | atoiFunc | printfFunc | scanfFunc ;

//strlen
strlenFunc : 'strlen' '(' mID ')'';';

//atoi
atoiFunc : 'atoi' '(' mID ')' ';';

//printf
printfFunc 
    : 'printf' '(' (mSTRING | mID) (','mID)* ')'';';

//scanf
scanfFunc : 'scanf' '(' (('&')?mID)(','('&')?mID)* ')'';';

//gets
getsFunc : 'gets' '(' mID ')';

//Selfdefined
selfDefinedFunc : mID '('((argument|mID)(','argument|mID)*)? ')';

argument : mINT | mDOUBLE | mCHAR | mSTRING;

//mID
mID : ID;

// mINT
mINT: INT;

// mCHAR
mCHAR: CHAR;

// mDOUBLE
mDOUBLE: DOUBLE;

// mSTRING
mSTRING: STRING;

// mLIB
mLIB: LIB;

//-------------词法规则----------------------------------------------
ID : [a-zA-Z_][0-9A-Za-z_]*;

INT : [0-9]+;

DOUBLE : [0-9]+'.'[0-9]+;

CHAR : '\''.'\'';

STRING : '"'.*?'"';

LIB : [a-zA-Z]+'.h'?;

Conjunction : '&&' | '||';

Operator : '!' | '+' | '-' | '*' | '/' | '==' | '!=' | '<' | '<=' | '>' | '>=';

//UnaryOperator :  '&' | '*' | '+' | '-' | '~' | '!';

LineComment: '//'.*?'\r'?'\n'   -> skip;

BlockComment:  '/*'.*?'*/'  -> skip;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

