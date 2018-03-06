# rubbish_interpreter

这个是编译原理的课设的一个解释器。

首先先进行词法分析，这个是参考了[c4.c](https://github.com/rswier/c4)的词法分析的过程。（class lex）

语法分析阶段我是自己参考将中缀式转化为后缀式这种方法，然后在将后缀式转化为前缀式，这样就得到了类似lisp的ast了。（class Parse）

然后就开始解释运行了（function cal）

内部放置的函数有printf,input,setmap,getmap,maplen,inmap,func,strappend,strindex,strlen,ord,chr,str,num,type。内置了hash map这个数据结构。
***
### 类型
| 类型名 |  具体类型作用 |
| - | :-: |
|RSStr|RubbishScript的字符类型|
|number|RubbishScript的数字类型|
|RSFunc|RubbishScript的函数类型|


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
|input|`变量=input(类型字符串)`|输入的类型字符串相等的类型|
|setmap|`setmap(map变量，位置，值)`|无|
|getmap|`getmap(map变量，位置)`|map这个位置的值|
|maplen|`maplen(map变量)`|map的长度|
|inmap|`inmap(map变量，位置)`|0为不在，1为在|
|func|`func(函数名称的字符串,...（函数参数）)`|调用名为这个字符串的函数，参数为字符后面的参数|
|strappend|`strappend(目标字符串，想要添加的字符串)`|两个字符连接RSStr对象|
|strindex|`strindex(目标字符串，位置)`|返回这个位置的字符|
|strlen|`strlen(目标字符串)`|返回这个字符的长度|
|ord|`ord(目标字符)`|返回这个字符的ASCII码的数|
|chr|`chr(ASCII位置)`|返回这个ASCII码的数的字符|
|str|`str(数字)`|将这个字符转为str类型|
|num|`num(目标字符)`|将这个字符转为num类型|
|type|`type(想要type的变量)`|返回这个想要type变量的类型|

# 注意：
1. 变量请先定义在使用
2. map是关键字，不可以作为变量使用
3. 内置函数再定义是不起效果的
4. 只能用Python3执行

