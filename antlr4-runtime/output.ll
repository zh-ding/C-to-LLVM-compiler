; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

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
  %"a" = alloca i32
  %"b" = alloca i32
  %"c" = alloca [10 x i32]
  %".2" = getelementptr inbounds [5 x i8], [5 x i8]* @".str0", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"scanf"(i8* %".2", i32* %"a", i32* %"b")
  %".4" = getelementptr inbounds [5 x i8], [5 x i8]* @".str1", i32 0, i32 0
  %".5" = getelementptr inbounds [10 x i32], [10 x i32]* %"c", i32 0, i32 0
  %".6" = getelementptr inbounds [10 x i32], [10 x i32]* %"c", i32 0, i32 1
  %".7" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* %".5", i32* %".6")
  %".8" = getelementptr inbounds [8 x i8], [8 x i8]* @".str2", i32 0, i32 0
  %".9" = load i32, i32* %"a"
  %".10" = load i32, i32* %"b"
  %".11" = add i32 %".9", %".10"
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".11")
  %".13" = getelementptr inbounds [9 x i8], [9 x i8]* @".str3", i32 0, i32 0
  %".14" = getelementptr inbounds [10 x i32], [10 x i32]* %"c", i32 0, i32 0
  %".15" = load i32, i32* %".14"
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".13", i32 %".15")
  %".17" = getelementptr inbounds [9 x i8], [9 x i8]* @".str4", i32 0, i32 0
  %".18" = getelementptr inbounds [10 x i32], [10 x i32]* %"c", i32 0, i32 1
  %".19" = load i32, i32* %".18"
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".17", i32 %".19")
  ret i32 0
}

declare i32 @"scanf"(i8* %".1", ...) 

@".str0" = constant [5 x i8] c"%d%d\00"
@".str1" = constant [5 x i8] c"%d%d\00"
declare i32 @"printf"(i8* %".1", ...) 

@".str2" = constant [8 x i8] c"a+b=%d\0a\00"
@".str3" = constant [9 x i8] c"c[0]=%d\0a\00"
@".str4" = constant [9 x i8] c"c[1]=%d\0a\00"
