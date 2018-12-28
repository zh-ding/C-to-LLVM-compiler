grammar simpleC;

prog :(include)* (mFunction)*;
//prog : (forBlock)*;

//-------------语法规则----------------------------------------------
include : '#include' '<' LIB '>';

//函数
mFunction : mType ID '(' params ')' '{' funcBody '}';

//函数参数
params : param (','param)* |;
param : mType ID;

//函数体
funcBody : body returnBlock;

//语句块/函数快
body : (block | func';')*;

//语句块
block : initialBlock | arrayInitBlock |  assignBlock | ifBlocks | whileBlock | forBlock | returnBlock;

//初始化语句
initialBlock : mType (ID ('=' expr)? (',' ID ('=' expr)?)*)? ';';
arrayInitBlock : mType ID '[' INT ']'';';
//arrayNoInitBlock : mType ID '[' ']' ';';


//赋值语句
assignBlock : ((arrayItem|ID) '=')+  expr ';';


//if 语句
ifBlocks : ifBlock (elifBlock)* (elseBlock)?;
ifBlock : 'if' '('condition')' '{' body '}';
elifBlock : 'else' 'if' '(' condition ')' '{' body '}';
elseBlock : 'else' '{' body '}';

condition :  expr (Conjunction expr)*;

//while 语句
whileBlock : 'while' '(' condition ')' '{' body '}';

//for 语句
forBlock : 'for' '(' for1Block  ';' condition ';' for3Block ')' ('{' body '}'|';');
for1Block :  ID ('=' expr)? (',' for1Block)?|;
for3Block : ID ('=' expr)? (',' for3Block)?|;

//return 语句
returnBlock : 'return' + (INT|ID) + ';';

expr
    : '(' expr ')'               #parens
    | op='!' expr                   #Neg
    | expr op=('*' | '/' | '%') expr   #MulDiv 
    | expr op=('+' | '-') expr   #AddSub
    | expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr #Judge
    | arrayItem                  #arrayietm
    | (op='-')? INT                        #int                          
    | (op='-')? DOUBLE                     #double
    | CHAR                       #char
    | STRING                     #string             
    | ID                         #identifier   
    | func                       #function                                     
    ;

mType : 'int'| 'double'| 'char'| 'string';

arrayItem : ID '[' expr ']';


//函数
func : strlenFunc | atoiFunc | printfFunc | scanfFunc | getsFunc | selfDefinedFunc ;

//strlen
strlenFunc : 'strlen' '(' ID ')';

//atoi
atoiFunc : 'atoi' '(' ID ')' ;

//printf
printfFunc 
    : 'printf' '(' (STRING | ID) (','expr)* ')';

//scanf
scanfFunc : 'scanf' '(' (('&')?ID)(','('&')?ID)* ')';

//gets
getsFunc : 'gets' '(' ID ')';
//Selfdefined

selfDefinedFunc : ID '('((argument|ID)(','argument|ID)*)? ')';

argument : INT | DOUBLE | CHAR | STRING;

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

