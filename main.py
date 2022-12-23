import re
from copy import deepcopy
file_name = input()
lines = open(file_name, mode='r').read().split('\n')

variables = dict() # 변수이름: 정수 집합
conditions = list()

def remove_space(s):
    pattern = re.compile('[^ ]*')
    return "".join(re.findall(pattern, s))

def get_set(set_: str):
    if set_[0] != '{' or set_[-1] != '}':
        raise ValueError(line + "  집합이아님")
    set_ = set_[1:-1]
    if '~' in set_:
        mid = set_.index('~')
        f = int(set_[0:mid])
        t = int(set_[mid+1:])
        return list(range(f, t+1))
    s = list(map(int, set_.split(',')))
    return s

def define(line):
    words = line.split()
    if words[0] != 'def':
        raise ValueError(line + "  잘못된 정의")
    for word in words[1:]:
        variables.update({word: None})
    

def include(line):
    front, back= None, None
    for i in range(len(line)-1):
        if line[i] == '<' and line[i+1] == '<':
            front = line[0:i]
            back = line[i+2:]
            break
    front = remove_space(front)
    back = get_set(remove_space(back))
    variables.update({front: back})
    pass

def get_front_back(s, key):
    mid = s.index(key)
    front = s[0:mid]
    back = s[mid+len(key):]
    return front, back


#공백없는 문자열을 받음
def small_condition_expression(exp):
    for key in ['==', '!=', '>=', '<=', '>', '<']:
        if key in exp:
            front, back =get_front_back(exp, key)
            return [key, front, back]
    
    raise ValueError(exp + '조건연산자가 없음')

# and, or은 띄워 써야됨, a>b>c 같은거 안됨
def condition_expression(line):
    words= line.split()
    r = []
    r_o = []
    temp = []
    for word in words:
        if word == 'and' or word == 'or':
            exp = remove_space("".join(temp))
            exp = small_condition_expression(exp)
            r_o.append(word)
            r.append(exp)
            temp.clear()
        else:
            temp.append(word)
    exp = remove_space("".join(temp))
    exp = small_condition_expression(exp)
    r.append(exp)
    return r, r_o
    

# when k >= 2 와같이 상수만 쓸 수 있다.
def when(line):
    front, back = get_front_back(line, 'when')
    r, r_o = condition_expression(back)
    
    
    pass


# 전처리
for line in lines:
    if 'when' in line:
        when(line)   # line을 수정
    if 'def' in line:
        define(line)
    elif '<<' in line:
        include(line)
    else:
        #조건만 있는 식
        conditions.append(condition_expression(line))

        

length = len(variables)
variable_names = list(variables)
combination = dict()
cases = []

def get_value(string: str):
    if string.isdecimal():
        # 숫자 리터럴 (int형)
        return int(string)
    else:
        # 변수 이름
        return combination.get(string)

def check_exp(exp):
    operator = exp[0]
    a = get_value(exp[1])
    b = get_value(exp[2])
    if operator == '==':
        return a == b
    elif operator == '!=':
        return a != b
    elif operator == '>=':
        return a >= b
    elif operator == '<=':
        return a <= b
    elif operator == '>':
        return a > b
    elif operator == '<':
        return a < b
    else:
        raise ValueError(operator +" 는 비교연산자가 아님")

def is_okay():
    for condition in conditions:
        i = 0
        operators = condition[1]
        operators_len = len(operators)
        values = list(map(check_exp, condition[0]))
        top = values[0]
        while i < operators_len:
            operator = operators[i]
            if operator == 'and':
                top = top and values[i + 1]
            elif operator == 'or':
                top = top or values[i + 1]
            else:
                raise ValueError(operator + "는 연산자가 아님")
            i += 1
        if not top:
            return False
    return True

def dfs(depth):
    if depth == length:
        if is_okay():
            cases.append(deepcopy(combination))
        pass
    elif depth < length:
        var = variable_names[depth]
        for value in variables.get(var):
            combination.update({var: value})
            dfs(depth+1)
            
    else:
        raise ValueError("depth > length - 1")


# 계산
dfs(0)

def output():
    print()
    print("Code:")
    for line in lines:
        print(line)
    print()
    print(f"Total {len(cases)} cases possible.")
    i = 0
    for case in cases:
        i += 1
        case:dict
        s = f'Case {i}: '
        for key in case.keys():
            s += f'{key} = {case.get(key)}, '
        print(s)
output()
