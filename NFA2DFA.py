from graphviz import Digraph

# 状态转移函数类
class MovFn:
    def __init__(self, src, edge, dst):
        self.src = src  # 源状态
        self.edge = edge  # 转换条件
        self.dst = dst  # 目标状态

# 检查字符x是否在字符串str中
def check(str, x):
    return x in str

# 检查状态x是否从集合setp中的任何状态可达
def is_reachable(x, setp, NFA):
    for state in setp:
        for trans in NFA:
            if trans.src == state and trans.dst == x:
                return True
    return False

# 计算ε-closure
def closure(setp, NFA):
    def recursive_closure(state, current_closure):
        for trans in NFA:
            if trans.src == state and trans.edge == '&' and trans.dst not in current_closure:
                current_closure.add(trans.dst)
                recursive_closure(trans.dst, current_closure)

    closure_set = set(setp)
    for state in setp:
        recursive_closure(state, closure_set)

    return ''.join(sorted(closure_set))

# 给定状态t和输入字符a，根据已知的NFA来计算状态的转移
def move(t, a, NFA):
    temp = ""
    for i in range(len(t)):  # 遍历当前状态t里面的每个状态
        for j in range(len(NFA)):  # 遍历NFA里面的转移函数
            if t[i] == NFA[j].src and NFA[j].edge == a:  # 检查当前转移是否与状态 t 和输入字符 a 匹配
                if not check(temp, NFA[j].dst):  # 如果temp没有包含此状态
                    temp += NFA[j].dst  # 添加新状态到temp
    return temp

# 检查元素是否为新状态
def checkINrawDFA(rawDFA, u):
    return u in rawDFA

def checkFlag(t):
    for i in range(len(t)):
        if not t[i]:
            return i
    return -1

def checkINdex(rawDFA, u):
    for i in range(len(rawDFA)):
        if rawDFA[i] == u:
            return i
    return -1

NFA = []  # 状态转移函数列表
NFA_temp = []  # (源,目标)二元组列表
NFADic = {}  # (源,目标)二元组作为键，转移条件作为值
dot = Digraph(comment='The Test Table')

num = int(input('输入转换数量: '))
print('输入格式为: 源状态 转换条件 目标状态 (以空格分隔)，&表示空转换:')
for i in range(num):
    x, y, z = input().split()
    temp = []  # 状态转移关系
    temp.append(int(x))
    temp.append(int(z))

    NFA_temp.append(temp)
    NFADic[tuple(temp)] = y 
    temp = MovFn(x, y, z)
    NFA.append(temp)
    # 原始NFA的图
    dot.node(x, x)
    dot.edge(x, z, y)

# 接收终止状态集
end_states = input('输入终止状态集(以空格分隔): ').split()

# 可视化NFA
dot.render('NFA.gv', view=True)
for i in range(len(NFA)):
    print(f'源：{NFA[i].src}, 转换条件：{NFA[i].edge}, 目标：{NFA[i].dst}')

# 获取输入字符集
sigma = set()
for transition in NFA:
    if transition.edge != '&':
        sigma.add(transition.edge)
sigma = list(sigma)

start = closure("0", NFA)
start = "".join(sorted(start))
rawDFA = []
rawDFA.append(start)
rawDFAflag = []
rawDFAflag.append(False)
while checkFlag(rawDFAflag) != -1:
    m = checkFlag(rawDFAflag)  # 第一个未处理的状态索引
    rawDFAflag[m] = True
    for i in range(len(sigma)):
        u = closure(move(rawDFA[m], sigma[i], NFA), NFA)  # 计算新状态的闭包
        u = "".join(sorted(u))  # 新状态u
        if u and not checkINrawDFA(rawDFA, u):  # 检查新状态是否可达以及是否为新状态
            rawDFA.append(u)
            rawDFAflag.append(False)

DFA = []
DFA_temp = []
DFADic = {}

# 遍历每个DFA的状态
for i in range(len(rawDFA)):
    # 计算每个状态在所有输入字符上的转换结果
    transitions = {s: "".join(sorted(closure(move(rawDFA[i], s, NFA), NFA))) for s in sigma}
    # 打印当前状态及其对应的转换结果
    print(f'状态 {rawDFA[i]}: {transitions}')
    # 将当前状态添加到DFA列表中
    DFA.append(rawDFA[i])

# 画图
dot2 = Digraph(comment='The Test Table')
for i in range(len(DFA)):
    if any(state in end_states for state in DFA[i]):
        dot2.node(str(i), '{' + ','.join(DFA[i]) + '}', shape='doublecircle')
    else:
        dot2.node(str(i), '{' + ','.join(DFA[i]) + '}', shape='circle')

for i in range(len(DFA)):
    for s in sigma:
        temp = []
        temp.append(i)
        new_state = "".join(sorted(closure(move(DFA[i], s, NFA), NFA)))
        if new_state:  # 如果新状态不是空字符串
            temp.append(checkINdex(rawDFA, new_state))  # 新状态索引
            DFA_temp.append(temp)
            DFADic[tuple(temp)] = s
            dot2.edge(str(i), str(checkINdex(rawDFA, new_state)), s)

dot2.render('DFA.gv', view=True)

# 打印终止状态
dfa_end_states = [state for state in DFA if any(e in state for e in end_states)]
print("DFA的终止状态:")
for state in dfa_end_states:
    print(state)
