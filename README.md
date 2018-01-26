# rubbish_interpreter
* * *

这个是编译原理的课设的一个解释器。

首先先进行词法分析，这个是参考了[c4.c](https://github.com/rswier/c4)的词法分析的过程。（class lex）

语法分析阶段我是自己参考将中缀式转化为后缀式这种方法，然后在将后缀式转化为前缀式，这样就得到了类似lisp的ast了。（class Parse）

然后就开始解释运行了（function eval）

内部放置的函数有printf,input,setmap,getmap,maplen。内置了hash map这个数据结构。
***

### 语法
| 作用 |  语法 |
| - | :-: |
|定义函数|`function function_name([params]){fucntion_body}`|
|条件|`if(condition){true_body}[else{false_body}]`|
|循环|`while(condition){true_body}`|
|函数返回|`return exp`|

### 内置函数
| 函数名 |  用法 |返回值|
| - | :-: |-:|
|printf|`printf(format,...)`|无|
|input|`变量=input()`|输入的整型数|
|setmap|`setmap(map变量，位置，值)`|无|
|getmap|`getmap(map变量，位置)`|map这个位置的值|
|maplen|`maplen(map变量)`|map的长度|

# 注意：
1. 变量请先定义在使用
2. map是关键字，不可以作为变量使用
3. 内置函数再定义是不起效果的
