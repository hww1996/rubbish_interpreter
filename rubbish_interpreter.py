__author__ = 'Administrator'

from copy import deepcopy
import sys
import json

class lex_type:
    '''
    1:id
    2:num
    3:string
    4:div
    5:equal
    6:assign
    7:add
    8:sub
    9:ne
    10:le
    11:shl
    12:lt
    13:ge
    14:shr
    15:gt
    16:lor
    17:or
    18:land
    19:and
    20:xor
    21:mod
    22:mul
    23:other
    '''
    def __init__(self,token,type):
        self.token=token
        self.type=type

    def __str__(self):
        return self.token
    def __repr__(self):
        return self.__str__()

class lex():
    def __init__(self,s):
        self.tokens=[]
        self.s=s
        self.pos=0
    def scanf(self):
        token=''
        while self.pos<len(self.s):
            token=self.s[self.pos]
            self.pos+=1
            if ord(token)>=ord('a') and ord(token)<=ord('z') or \
                ord(token)>=ord('A') and ord(token)<=ord('Z') or \
                ord(token)==ord('_'):
                id_token=token

                while \
                self.pos<len(self.s) and \
                (ord(self.s[self.pos])>=ord('a') and ord(self.s[self.pos])<=ord('z') or \
                ord(self.s[self.pos])>=ord('A') and ord(self.s[self.pos])<=ord('Z') or \
                ord(self.s[self.pos])>=ord('0') and ord(self.s[self.pos])<=ord('9') or \
                ord(self.s[self.pos])==ord('_')):
                    id_token+=self.s[self.pos]
                    self.pos+=1
                self.tokens.append(lex_type(id_token,1))

            elif ord(token)>=ord('0') and ord(token)<=ord('9'):
                num_token=token

                while self.pos<len(self.s) and ord(self.s[self.pos])>=ord('0') and ord(self.s[self.pos])<=ord('9'):
                    num_token+=self.s[self.pos]
                    self.pos+=1
                self.tokens.append(lex_type(num_token,2))

            elif token=='\'' or token=='"':
                last_token=token
                string_token=token
                while self.pos<len(self.s) and self.s[self.pos]!=last_token:
                    string_token+=self.s[self.pos]
                    self.pos+=1
                string_token+=last_token
                self.pos+=1
                self.tokens.append(lex_type(string_token,3))

            elif token=='/':
                if self.s[self.pos]=='/':
                    while self.pos<len(self.s) and self.s[self.pos]!='\n':
                        self.pos+=1
                else:
                    self.tokens.append(lex_type(token,4))

            elif token=='=':
                if self.s[self.pos]=='=':
                    self.pos+=1
                    self.tokens.append(lex_type("==",5))
                else:
                    self.tokens.append(lex_type("=",6))
            elif token=='+':
                self.tokens.append(lex_type("+",7))

            elif token=='-':
                self.tokens.append(lex_type("-",8))

            elif token=='!':
                if self.s[self.pos]=='=':
                    self.pos+=1
                    self.tokens.append(lex_type("!=",9))
                else:
                    print("unknown token.")
                    exit(-1)

            elif token=='<':
                if self.s[self.pos]=='=':
                    self.pos+=1
                    self.tokens.append(lex_type("<=",10))
                elif self.s[self.pos]=='<':
                    self.pos+=1
                    self.tokens.append(lex_type("<<",11))
                else:
                    self.tokens.append(lex_type("<",12))

            elif token=='>':
                if self.s[self.pos]=='=':
                    self.pos+=1
                    self.tokens.append(lex_type(">=",13))
                elif self.s[self.pos]=='>':
                    self.pos+=1
                    self.tokens.append(lex_type(">>",14))
                else:
                    self.tokens.append(lex_type(">",15))
            elif token=='|':
                if self.s[self.pos]=='|':
                    self.pos+=1
                    self.tokens.append(lex_type("||",16))
                else:
                    self.tokens.append(lex_type("|",17))
            elif token=='&':
                if self.s[self.pos]=='&':
                    self.pos+=1
                    self.tokens.append(lex_type("&&",18))
                else:
                    self.tokens.append(lex_type("&",19))
            elif token=='^':
                self.tokens.append(lex_type("^",20))

            elif token=='%':
                self.tokens.append(lex_type("%",21))

            elif token=='*':
                self.tokens.append(lex_type("*",22))

            elif token==';' or token=='{' or token=='}' or token=='(' or token==')' or token==',':
                self.tokens.append(lex_type(token,23))
        return self.tokens


class Function():
    def __init__(self,name,pos):
        self.var=[]
        self.function_name=name
        self.pos=pos
    def __str__(self):
        ss="function_name:%s,pos:%d,var:%s"
        return  ss %(self.function_name,self.pos,str(self.var))
    def __repr__(self):
        return self.__str__()
    def add_var(self,var):
        if var in self.var:
            print("dup use the id")
            exit(-1)
        self.var.append(var)
class RSFunc():
    def __init__(self,code,name,var):
        self.code=code
        self.name=name
        self.var=var
    def __str__(self):
        return str(self.code)
    def __repr__(self):
        return self.__str__()
class RSStr():
    def __init__(self,val):
        self.val=val
    def __str__(self):
        return "RSStr(%s)" %(self.val)
    def __repr__(self):
        return self.__str__()

class Parse():
    def __init__(self,s):
        self.s=s
        self.tokens=[]
        self.token_map={}
        self.func_map={}
        self.pos=0
        self.statement=[]
    def analysis(self):
        self.tokens=lex(self.s).scanf()
        self.templateFunctions()
        self.inner_function()
        ans={}
        for func in self.func_map:
            if self.func_map[func].pos>0:#judge if is inner_fucntion
                ans[func]=RSFunc(self.parse(self.func_map[func].pos,self.tokens),func,deepcopy(self.func_map[func].var))
        return ans

    def inner_function(self):
        self.func_map["printf"]=Function("printf",-1)

        self.func_map["input"]=Function("input",-1)

        self.func_map["setmap"]=Function("setmap",-1)

        self.func_map["getmap"]=Function("getmap",-1)

        self.func_map["maplen"]=Function("maplen",-1)

        self.func_map["inmap"]=Function("inmap",-1)

        self.func_map["mapremove"]=Function("mapremove",-1)

        self.func_map["func"]=Function("func",-1)

        self.func_map["strappend"]=Function("strappend",-1)

        self.func_map["strindex"]=Function("strindex",-1)

        self.func_map["strlen"]=Function("strlen",-1)

        self.func_map["ord"]=Function("ord",-1)

        self.func_map["chr"]=Function("chr",-1)

        self.func_map["str"]=Function("str",-1)

        self.func_map["num"]=Function("num",-1)

        self.func_map["type"]=Function("type",-1)

        return
    def templateFunctions(self):
        i=0
        while i<len(self.tokens):
            if self.tokens[i].token=="function":
                i+=1
                f=Function(self.tokens[i].token,-1)
                i+=2
                while self.tokens[i].token!=")":
                    if self.tokens[i].type==1:
                        f.add_var(self.tokens[i].token)
                    elif self.tokens[i].token==",":
                        pass
                    else:
                        print("define token is not an id.")
                        exit(-1)
                    i+=1
                f.pos=i+1
                self.func_map[f.function_name]=f
            i+=1
        return
    def parse(self,pos,tokens):
        if tokens[pos].token!="{":
            print("error")
            exit(-1)
        ans=[]
        ans.append("begin")
        pos+=1
        while tokens[pos].token!="}":
            temp=[]
            if tokens[pos].token=="if":
                temp.append("if")
                pos+=1
                if_cond=[]
                if tokens[pos].token!="(":
                    print("error.if don't match the (")
                    exit(-1)
                pos+=1
                brak_count=0
                while True:
                    if tokens[pos].token==")":
                        if brak_count==0:
                            break
                    if tokens[pos].token=="(":
                        brak_count+=1
                    if tokens[pos].token==")":
                        brak_count-=1
                    if_cond.append(tokens[pos])
                    pos+=1
                pos+=1
                if len(if_cond)==0:
                    print("error.not condition.")
                    exit(-1)
                temp.append(self.deal_statance(if_cond))

                if_body=[]
                if tokens[pos].token!="{":
                    print("error.after if condition withou token {")
                    exit(-1)
                if_body.append(tokens[pos])
                pos+=1
                brak_count=0
                while True:
                    if tokens[pos].token=="}":
                        if brak_count==0:
                            break
                    if tokens[pos].token=="{":
                        brak_count+=1
                    if tokens[pos].token=="}":
                        brak_count-=1
                    if_body.append(tokens[pos])
                    pos+=1
                if_body.append(tokens[pos])
                pos+=1
                temp.append(self.parse(0,if_body))

                if tokens[pos].token=="else":
                    pos+=1
                    if tokens[pos].token!="{":
                        print("error.after if condition withou token {")
                        exit(-1)
                    else_body=[]
                    else_body.append(tokens[pos])
                    pos+=1
                    brak_count=0
                    while True:
                        if tokens[pos].token=="}":
                            if brak_count==0:
                                break
                        if tokens[pos].token=="{":
                            brak_count+=1
                        if tokens[pos].token=="}":
                            brak_count-=1
                        else_body.append(tokens[pos])
                        pos+=1
                    else_body.append(tokens[pos])
                    pos+=1
                    temp.append(self.parse(0,else_body))
####################################################################################
            elif tokens[pos].token=="while":
                temp.append("while")
                pos+=1
                while_cond=[]
                if tokens[pos].token!="(":
                    print("error.while don't match the (")
                    exit(-1)
                pos+=1
                brak_count=0
                while True:
                    if tokens[pos].token==")":
                        if brak_count==0:
                            break
                    if tokens[pos].token=="(":
                        brak_count+=1
                    if tokens[pos].token==")":
                        brak_count-=1
                    while_cond.append(tokens[pos])
                    pos+=1
                pos+=1
                if len(while_cond)==0:
                    print("error.not condition.")
                    exit(-1)
                temp.append(self.deal_statance(while_cond))

                while_body=[]
                if tokens[pos].token!="{":
                    print("error.after while condition withou token {")
                    exit(-1)
                while_body.append(tokens[pos])
                pos+=1
                brak_count=0
                while True:
                    if tokens[pos].token=="}":
                        if brak_count==0:
                            break
                    if tokens[pos].token=="{":
                        brak_count+=1
                    if tokens[pos].token=="}":
                        brak_count-=1
                    while_body.append(tokens[pos])
                    pos+=1
                while_body.append(tokens[pos])
                pos+=1
                temp.append(self.parse(0,while_body))
####################################################################################
            else:
                while tokens[pos].token!=";":
                    temp.append(tokens[pos])
                    pos+=1
                pos+=1
                ans.append(self.deal_statance(temp))
                continue
            ans.append(deepcopy(temp))
        return ans
    def deal_statance(self,statence):
        if len(statence)==0:
            return None
        if len(statence)==1:
            if statence[0].type==2:
                return int(statence[0].token)
            elif statence[0].type==3:
                return RSStr(json.loads(statence[0].token))
        pos=0
        ans=[]
        while pos<len(statence):
            if statence[pos].type==1:
                if self.func_map.get(statence[pos].token)!=None:
                    func_list=[]
                    func_list.append(statence[pos].token)
                    pos+=1
                    if statence[pos].token!="(":
                        print("error! not match the (")
                        exit(-1)
                    brak_count=0
                    pos+=1
                    while statence[pos].token!=")":
                        function_temp=[]
                        while True:
                            if statence[pos].token==")" or statence[pos].token==",":
                                if brak_count==0:
                                    break
                            if statence[pos].token=="(":
                                brak_count+=1
                            if statence[pos].token==")":
                                brak_count-=1
                            function_temp.append(statence[pos])
                            pos+=1
                        function_param_temp_result=self.deal_statance(function_temp)
                        if function_param_temp_result!=None:
                            func_list.append(deepcopy(function_param_temp_result))
                        if statence[pos].token==",":
                            pos+=1
                    ans.append(deepcopy(func_list))
                else:
                    ans.append(statence[pos].token)
            elif statence[pos].type==2:
                ans.append(int(statence[pos].token))
            elif statence[pos].type==3:
                ans.append(RSStr(json.loads(statence[pos].token)))
            else:
                ans.append(statence[pos].token)
            pos+=1
        return self.make_to_lisp(ans)
    def make_to_lisp(self,statence_list):
        if len(statence_list)==0:
            return None
        if len(statence_list)==1:
            return statence_list[0]
        priority={
            '*':10,'/':10,'%':10,
            '+':9,'-':9,
            '<<':8,'>>':8,
            '<':7,'>':7,'<=':7,'>=':7,
            '==':6,'!=':6,
            '&':5,
            '^':4,
            '|':3,
            '&&':2,
            '||':1,
            '=':0
        }
        temp_output=[]
        temp_output_symbol=[]
        for i in range(len(statence_list)):
            if isinstance(statence_list[i],str):
                if priority.get(statence_list[i])!=None:
                    if len(temp_output_symbol)==0:
                        temp_output_symbol.append(statence_list[i])
                    else:
                        j=len(temp_output_symbol)-1
                        if  temp_output_symbol[j]=="(" or \
                            priority[temp_output_symbol[j]]<=priority[statence_list[i]]:

                            temp_output_symbol.append(statence_list[i])
                        else:
                            while j>=0:
                                if temp_output_symbol[j]=="(":
                                    break
                                if priority[temp_output_symbol[j]]<priority[statence_list[i]]:
                                    break
                                temp_output.append(temp_output_symbol.pop())
                                j-=1
                            temp_output_symbol.append(statence_list[i])

                elif statence_list[i]=="(":
                    temp_output_symbol.append(statence_list[i])
                elif statence_list[i]==")":
                    j=len(temp_output_symbol)-1
                    while j>=0:
                        if temp_output_symbol[j]=="(":
                            break
                        temp_output.append(temp_output_symbol.pop())
                        j-=1
                    if j==-1:
                        print("lack of a (.")
                        exit(-1)
                    temp_output_symbol.pop()
                else:
                    temp_output.append(statence_list[i])
            else:
                temp_output.append(statence_list[i])

        j=len(temp_output_symbol)-1
        while j>=0:
            temp_output.append(temp_output_symbol.pop())
            j-=1
        ans=[]
        for i in range(len(temp_output)):
            if isinstance(temp_output[i],str):
                if priority.get(temp_output[i])!=None:
                    if len(ans)<2:
                        print("error.Binary operation")
                        exit(-1)
                    first_op=ans.pop()
                    second_op=ans.pop()
                    if isinstance(first_op,str) and priority.get(first_op)!=None:
                        print("can't use the operator as the operate number.")
                        exit(-1)
                    if isinstance(second_op,str) and priority.get(second_op)!=None:
                        print("can't use the operator as the operate number.")
                        exit(-1)
                    ans.append([temp_output[i],second_op,first_op])
                    continue
            ans.append(temp_output[i])
        if isinstance(ans[0],list):
            return ans[0]
        return ans

def cal(x,stop,env,ast):
    if isinstance(x,str):
        if x=="map":
            return dict()
        elif env.get(x)!=None:
            return env[x]
        else:
            print("use the unknown variable.")
            exit(-1)
    elif not isinstance(x,list):
        return x
    elif len(x)==0:
        print("error.empty ast.")
        exit(-1)
    elif x[0]=="printf":
        print_temp=cal(x[1],stop,env,ast)
        print_str=print_temp.val
        if not isinstance(print_temp,RSStr):
            print("the first args of the printf is not a string.")
            exit(-1)
        print_args=[]
        for i in range(len(x))[2:]:
            temp=cal(x[i],stop,env,ast)
            if isinstance(temp,RSStr):
                print_args.append(temp.val)
            elif isinstance(temp,int):
                print_args.append(temp)
            else:
                print("error.attemp to print unknown type.")
                exit(-1)
        if len(print_args)>0:
            print(print_str %tuple(print_args),end="")
        else:
            print(print_str,end="")
    elif x[0]=="input":
        if len(x)!=2:
            print("error.the number of the args of the input must be 1.")
            exit(-1)
        second_op=cal(x[1],stop,env,ast)
        if not isinstance(second_op,RSStr):
            print("error.the arg must be string")
            exit(-1)
        if second_op.val=="num":
            return int(input())
        elif second_op.val=="str":
            return RSStr(input())
        else:
            print("unknow type of the input.")
            exit(-1)
    elif x[0]=="if":
        if len(x)==3:
            if cal(x[1],stop,env,ast)==True:
                return cal(x[2],stop,env,ast)
            return None
        if len(x)==4:
            if cal(x[1],stop,env,ast)==True:
                return cal(x[2],stop,env,ast)
            return cal(x[3],stop,env,ast)
    elif x[0]=="while":
        while cal(x[1],stop,env,ast)==True:
            temp=cal(x[2],stop,env,ast)
            if stop[0]==True:
                return temp
        return None
    elif x[0]=="begin":
        for i in range(len(x))[1:]:
            temp=cal(x[i],stop,env,ast)
            if stop[0]==True:
                return temp
        return None
    elif x[0]=="return":
        stop[0]=True
        return cal(x[1],stop,env,ast)
    elif x[0]=="setmap":
        if(len(x)!=4):
            print("error.the length of the args of the setmap function is not 3.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        second_op_temp=cal(x[2],stop,env,ast)
        second_op=0
        if isinstance(second_op_temp,RSStr):
            second_op=second_op_temp.val
        elif isinstance(second_op_temp,int):
            second_op=second_op_temp
        else:
            print("use hashable key,error.")
            exit(-1)
        env[x[1]][second_op]=cal(x[3],stop,env,ast)
        return None
    elif x[0]=="getmap":
        if(len(x)!=3):
            print("error.the length of the args of the getmap function is not 2.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        second_op_temp=cal(x[2],stop,env,ast)
        second_op=0
        if isinstance(second_op_temp,RSStr):
            second_op=second_op_temp.val
        elif isinstance(second_op_temp,int):
            second_op=second_op_temp
        else:
            print("use hashable key,error.")
            exit(-1)
        return env[x[1]][second_op]
    elif x[0]=="maplen":
        if(len(x)!=2):
            print("error.the length of the args of the maplen function is not 1.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        return len(env[x[1]])
    elif x[0]=="inmap":
        if(len(x)!=3):
            print("error.the length of the args of the inmap function is not 2.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        second_op_temp=cal(x[2],stop,env,ast)
        second_op=0
        if isinstance(second_op_temp,RSStr):
            second_op=second_op_temp.val
        elif isinstance(second_op_temp,int):
            second_op=second_op_temp
        else:
            print("use hashable key,error.")
            exit(-1)
        return 1 if env[x[1]].get(second_op)!=None else 0
    elif x[0]=="mapremove":
        if(len(x)!=3):
            print("error.the length of the args of the mapremove function is not 2.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        second_op_temp=cal(x[2],stop,env,ast)
        second_op=0
        if isinstance(second_op_temp,RSStr):
            second_op=second_op_temp.val
        elif isinstance(second_op_temp,int):
            second_op=second_op_temp
        else:
            print("use hashable key,error.")
            exit(-1)
        env[x[1]].pop(second_op)
        return None
    elif x[0]=="func":
        if len(x)!=2:
            print("error.the length of the args of the func function is not 1")
        second_op=x[1]
        if isinstance(x[1],str):
            second_op=cal(x[1],stop,env,ast)
        if not isinstance(second_op,RSStr):
            print("error.the args is not the string")
            exit(-1)
        second_op_str=second_op.val
        if ast.get(second_op_str)==None:
            print("error.attemp to get the undefine function object.")
            exit(-1)
        return ast[second_op_str]
    elif x[0]=="strappend":
        if len(x)!=3:
            print("error.the length of the args of the strappend function is not 2.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        if not isinstance(first_op,RSStr):
            print("error.the first arg must be string.")
            exit(-1)
        if not isinstance(second_op,RSStr):
            print("error.the second arg must be string.")
            exit(-1)
        return RSStr(first_op.val+second_op.val)
    elif x[0]=="strindex":
        if len(x)!=3:
            print("error.the length of the args of the strindex function is not 2.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        if not isinstance(first_op,RSStr):
            print("error.the first arg must be string.")
            exit(-1)
        if not isinstance(second_op,int):
            print("error.the second arg must be num.")
            exit(-1)
        t=first_op.val[second_op]
        return RSStr(t)
    elif x[0]=="strlen":
        if len(x)!=2:
            print("error.the length of the args of the strlen function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if not isinstance(first_op,RSStr):
            print("error.the first arg must be string.")
            exit(-1)
        return len(first_op.val)
    elif x[0]=="ord":
        if len(x)!=2:
            print("error.the length of the args of the ord function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if not isinstance(first_op,RSStr):
            print("error.the first arg must be string.")
            exit(-1)
        return ord(first_op.val)
    elif x[0]=="chr":
        if len(x)!=2:
            print("error.the length of the args of the chr function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if not isinstance(first_op,int):
            print("error.the first arg must be num.")
            exit(-1)
        return RSStr(chr(first_op))
    elif x[0]=="str":
        if len(x)!=2:
            print("error.the length of the args of the str function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if not isinstance(first_op,int):
            print("error.the first arg must be num.")
            exit(-1)
        return RSStr(str(first_op))
    elif x[0]=="num":
        if len(x)!=2:
            print("error.the length of the args of the num function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if not isinstance(first_op,RSStr):
            print("error.the first arg must be num.")
            exit(-1)
        return int(first_op.val)
    elif x[0]=="type":
        if len(x)!=2:
            print("error.the length of the args of the type function is not 1.")
            exit(-1)
        first_op=cal(x[1],stop,env,ast)
        if isinstance(first_op,RSStr):
            return RSStr("str")
        elif isinstance(first_op,int):
            return RSStr("num")
        elif isinstance(first_op,RSFunc):
            return RSStr("function")
        elif isinstance(first_op,dict):
            return RSStr("map")
        else:
            return RSStr("unkown")
    elif x[0]=="*":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op*second_op
    elif x[0]=="/":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        if second_op==0:
            print("error.div a zero.")
        return first_op/second_op
    elif x[0]=="%":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        if second_op==0:
            print("error.div a zero.")
        return first_op%second_op
    elif x[0]=="+":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op+second_op
    elif x[0]=="-":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op-second_op
    elif x[0]=="<<":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op<<second_op
    elif x[0]==">>":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op>>second_op
    elif x[0]=="<":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op<second_op
    elif x[0]==">":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op>second_op
    elif x[0]=="<=":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op<=second_op
    elif x[0]==">=":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op>=second_op
    elif x[0]=="==":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op==second_op
    elif x[0]=="!=":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op!=second_op
    elif x[0]=="&":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op&second_op
    elif x[0]=="|":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return first_op|second_op
    elif x[0]=="&&":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return (first_op and second_op)
    elif x[0]=="||":
        first_op=cal(x[1],stop,env,ast)
        second_op=cal(x[2],stop,env,ast)
        return (first_op or second_op)
    elif x[0]=="=":
        second_op=cal(x[2],stop,env,ast)
        env[x[1]]=second_op
        return None
    elif ast.get(x[0])!=None:
        function_call_env={}
        if len(ast[x[0]].var)!=len(x)-1:
            print("error.the number of the args is not equal the number of the function args.")
            exit(-1)
        for i in range(len(ast[x[0]].var)):
            function_call_env[ast[x[0]].var[i]]=cal(x[i+1],stop,env,ast)
        return cal(ast[x[0]].code,[False],function_call_env,ast)
    elif env.get(x[0])!=None:
        if not isinstance(env[x[0]],RSFunc):
            print("error.the attemp to call the unknow function.")
            exit(-1)
        function_call_env={}
        if len(env[x[0]].var)!=len(x)-1:
            print("error.the number of the args is not equal the number of the function args.")
            exit(-1)
        for i in range(len(env[x[0]].var)):
            function_call_env[env[x[0]].var[i]]=cal(x[i+1],stop,env,ast)
        return cal(env[x[0]].code,[False],function_call_env,ast)
    return None

if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage:rubbish_interpreter <RubbishScript-file>")
        exit(1)
    s=open(sys.argv[1]).read()
    ast=Parse(s).analysis()
    if ast.get("main")==None:
        print("error.do not have the main function.")
        exit(-1)
    exit_code=cal(ast["main"].code,[False],{},ast)
    print("exit with code %d" %(exit_code))