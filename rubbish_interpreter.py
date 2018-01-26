__author__ = 'Administrator'

from copy import deepcopy

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
class Func():
    def __init__(self,code,name,var):
        self.code=code
        self.name=name
        self.var=var
    def __str__(self):
        return str(self.code)
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
                ans[func]=Func(self.parse(self.func_map[func].pos,self.tokens),func,deepcopy(self.func_map[func].var))
        return ans

    def inner_function(self):
        print_function=Function("printf",-1)
        self.func_map["printf"]=print_function

        input_function=Function("input",-1)
        self.func_map["input"]=input_function

        set_map_function=Function("setmap",-1)
        self.func_map["setmap"]=set_map_function

        get_map_function=Function("getmap",-1)
        self.func_map["getmap"]=get_map_function

        map_len_function=Function("maplen",-1)
        self.func_map["maplen"]=map_len_function
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
            return statence[0].token
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
                ans.append(eval(statence[pos].token))
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
        print_str=x[1]
        print_args=[]
        for i in range(len(x))[2:]:
            print_args.append(cal(x[i],stop,env,ast))
        if len(print_args)>0:
            print(print_str %tuple(print_args))
        else:
            print(print_str)
    elif x[0]=="input":
        return int(input())
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
        env[x[1]][cal(x[2],stop,env,ast)]=cal(x[3],stop,env,ast)
        return None
    elif x[0]=="getmap":
        if(len(x)!=3):
            print("error.the length of the args of the setmap function is not 2.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        return env[x[1]][cal(x[2],stop,env,ast)]
    elif x[0]=="maplen":
        if(len(x)!=2):
            print("error.the length of the args of the setmap function is not 1.")
            exit(-1)
        if env.get(x[1])==None:
            print("error.use the unknow variable.")
            exit(-1)
        if not isinstance(env[x[1]],dict):
            print("error.use the variable is not the map.")
            exit(-1)
        return len(env[x[1]])
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
        for i in range(len(ast[x[0]].var)):
            function_call_env[ast[x[0]].var[i]]=cal(x[i+1],stop,env,ast)
        return cal(ast[x[0]].code,[False],function_call_env,ast)
    return None

if __name__=="__main__":
    s=open("C:\\Users\\Administrator\\Desktop\\code\\test.txt").read()
    ast=Parse(s).analysis()
    if ast.get("main")==None:
        print("error.do not have the main function.")
        exit(-1)
    exit_code=cal(ast["main"].code,[False],{},ast)
    print("exit with code %d" %(exit_code))