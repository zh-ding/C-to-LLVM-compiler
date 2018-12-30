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
  %"c" = alloca i32
  %".8" = load i32, i32* %".6"
  %".9" = load i32, i32* %".4"
  %".10" = sub i32 %".8", %".9"
  store i32 %".10", i32* %"c"
  %".12" = load i32, i32* %"c"
  ret i32 %".12"
}

define i32 @"main"() 
{
main.entry:
  %"a" = alloca i32
  store i32 1, i32* %"a"
  %"b" = alloca i32
  %".3" = sext i8 50 to i32
  store i32 %".3", i32* %"b"
  %"d" = alloca i32
  %"c" = alloca i32
  store i32 3, i32* %"c"
  br label %".6"
.6:
  %".9" = load i32, i32* %"a"
  %".10" = icmp eq i32 %".9", 1
  br i1 %".10", label %".11", label %".12"
.7:
  ret i32 0
.11:
  br label %".14"
.12:
  %".31" = load i32, i32* %"b"
  %".32" = sext i8 50 to i32
  %".33" = icmp eq i32 %".31", %".32"
  br i1 %".33", label %".34", label %".35"
.14:
  %".17" = load i32, i32* %"c"
  %".18" = icmp eq i32 %".17", 2
  br i1 %".18", label %".19", label %".20"
.15:
  br label %".7"
.19:
  %".22" = getelementptr inbounds [11 x i8], [11 x i8]* @".str0", i32 0, i32 0
  %".23" = load i32, i32* %"a"
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".22", i32 %".23")
  br label %".15"
.20:
  %".26" = getelementptr inbounds [11 x i8], [11 x i8]* @".str1", i32 0, i32 0
  %".27" = load i32, i32* %"a"
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".26", i32 %".27")
  br label %".15"
.34:
  %".37" = getelementptr inbounds [6 x i8], [6 x i8]* @".str2", i32 0, i32 0
  %".38" = load i32, i32* %"b"
  %".39" = call i32 (i8*, ...) @"printf"(i8* %".37", i32 %".38")
  br label %".7"
.35:
  %".41" = getelementptr inbounds [7 x i8], [7 x i8]* @".str3", i32 0, i32 0
  %".42" = call i32 (i8*, ...) @"printf"(i8* %".41")
  br label %".7"
}

declare i32 @"printf"(i8* %".1", ...) 

@".str0" = constant [11 x i8] c"a=%d c==2\0a\00"
@".str1" = constant [11 x i8] c"a=%d c!=2\0a\00"
@".str2" = constant [6 x i8] c"b=%c\0a\00"
@".str3" = constant [7 x i8] c"hello\0a\00"
