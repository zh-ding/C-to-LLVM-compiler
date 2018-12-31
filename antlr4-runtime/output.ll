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
  %".3" = sext i8 51 to i32
  store i32 %".3", i32* %"b"
  %"d" = alloca i32
  %"c" = alloca i32
  store i32 3, i32* %"c"
  %"arr" = alloca [10 x i32]
  %".6" = load i32, i32* %"c"
  %".7" = getelementptr inbounds [10 x i32], [10 x i32]* %"arr", i32 0, i32 0
  store i32 %".6", i32* %".7"
  br label %".9"
.9:
  %".12" = load i32, i32* %"a"
  %".13" = icmp eq i32 %".12", 1
  %".14" = load i32, i32* %"b"
  %".15" = sext i8 50 to i32
  %".16" = icmp eq i32 %".14", %".15"
  %".17" = and i1 %".13", %".16"
  br i1 %".17", label %".18", label %".19"
.10:
  ret i32 0
.18:
  br label %".21"
.19:
  %".38" = load i32, i32* %"b"
  %".39" = sext i8 52 to i32
  %".40" = icmp eq i32 %".38", %".39"
  br i1 %".40", label %".41", label %".42"
.21:
  %".24" = load i32, i32* %"c"
  %".25" = icmp eq i32 %".24", 2
  br i1 %".25", label %".26", label %".27"
.22:
  br label %".10"
.26:
  %".29" = getelementptr inbounds [11 x i8], [11 x i8]* @".str0", i32 0, i32 0
  %".30" = load i32, i32* %"a"
  %".31" = call i32 (i8*, ...) @"printf"(i8* %".29", i32 %".30")
  br label %".22"
.27:
  %".33" = getelementptr inbounds [11 x i8], [11 x i8]* @".str1", i32 0, i32 0
  %".34" = load i32, i32* %"a"
  %".35" = call i32 (i8*, ...) @"printf"(i8* %".33", i32 %".34")
  br label %".22"
.41:
  %".44" = getelementptr inbounds [6 x i8], [6 x i8]* @".str2", i32 0, i32 0
  %".45" = load i32, i32* %"b"
  %".46" = call i32 (i8*, ...) @"printf"(i8* %".44", i32 %".45")
  br label %".10"
.42:
  %".48" = getelementptr inbounds [17 x i8], [17 x i8]* @".str3", i32 0, i32 0
  %".49" = getelementptr inbounds [10 x i32], [10 x i32]* %"arr", i32 0, i32 0
  %".50" = load i32, i32* %".49"
  %".51" = call i32 (i8*, ...) @"printf"(i8* %".48", i32 %".50")
  br label %".10"
}

declare i32 @"printf"(i8* %".1", ...) 

@".str0" = constant [11 x i8] c"a=%d c==2\0a\00"
@".str1" = constant [11 x i8] c"a=%d c!=2\0a\00"
@".str2" = constant [6 x i8] c"b=%c\0a\00"
@".str3" = constant [17 x i8] c"hello arr[0]=%d\0a\00"
