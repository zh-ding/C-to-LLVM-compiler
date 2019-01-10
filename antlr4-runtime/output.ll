; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"a" = common global i32 undef
@"b" = common global i32 undef
@"d" = common global [10 x i32] undef
@"x" = common global [10 x {i32, [10 x double]}] zeroinitializer
define void @"void_foo"() 
{
void_foo.entry:
  %".2" = getelementptr inbounds [10 x i8], [10 x i8]* @".str0", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@".str0" = constant [10 x i8] c"void_foo\0a\00"
define i32 @"foo"(i32 %"a", i32 %"b") 
{
foo.entry:
  %".4" = alloca i32
  store i32 %"a", i32* %".4"
  %".6" = alloca i32
  store i32 %"b", i32* %".6"
  br label %".8"
.8:
  %".11" = load i32, i32* %".4"
  %".12" = load i32, i32* %".6"
  %".13" = icmp sgt i32 %".11", %".12"
  br i1 %".13", label %".14", label %".15"
.9:
  %".20" = load i32, i32* %".6"
  ret i32 %".20"
.14:
  %".17" = load i32, i32* %".4"
  ret i32 %".17"
.15:
  br label %".9"
}

define i32 @"main"() 
{
main.entry:
  %"i" = alloca i32
  %"c" = alloca [10 x i32]
  store i32 0, i32* %"i"
  br label %".3"
.3:
  %".7" = load i32, i32* %"i"
  %".8" = icmp slt i32 %".7", 10
  br i1 %".8", label %".4", label %".5"
.4:
  %".10" = getelementptr inbounds [3 x i8], [3 x i8]* @".str1", i32 0, i32 0
  %".11" = load i32, i32* %"i"
  %".12" = getelementptr inbounds [10 x {i32, [10 x double]}], [10 x {i32, [10 x double]}]* @"x", i32 0, i32 %".11"
  %".13" = getelementptr inbounds {i32, [10 x double]}, {i32, [10 x double]}* %".12", i32 0, i32 0
  %".14" = call i32 (i8*, ...) @"scanf"(i8* %".10", i32* %".13")
  %".15" = load i32, i32* %"i"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %"i"
  br label %".3"
.5:
  store i32 0, i32* %"i"
  br label %".20"
.20:
  %".24" = load i32, i32* %"i"
  %".25" = icmp slt i32 %".24", 10
  br i1 %".25", label %".21", label %".22"
.21:
  %".27" = getelementptr inbounds [12 x i8], [12 x i8]* @".str2", i32 0, i32 0
  %".28" = load i32, i32* %"i"
  %".29" = load i32, i32* %"i"
  %".30" = getelementptr inbounds [10 x {i32, [10 x double]}], [10 x {i32, [10 x double]}]* @"x", i32 0, i32 %".29"
  %".31" = getelementptr inbounds {i32, [10 x double]}, {i32, [10 x double]}* %".30", i32 0, i32 0
  %".32" = load i32, i32* %".31"
  %".33" = call i32 (i8*, ...) @"printf"(i8* %".27", i32 %".28", i32 %".32")
  %".34" = load i32, i32* %"i"
  %".35" = add i32 %".34", 1
  store i32 %".35", i32* %"i"
  br label %".20"
.22:
  ret i32 0
}

declare i32 @"scanf"(i8* %".1", ...) 

@".str1" = constant [3 x i8] c"%d\00"
@".str2" = constant [12 x i8] c"x[%d].a=%d\0a\00"
