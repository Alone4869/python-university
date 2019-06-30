"""
 文法：
    E->E+T | T
    T->T*F | F
    F->(E)|i
 消除左递归：
    E->TH       (H代替E')
    H->+TH|e    (e替代空)
    T->FY       (Y代替T')
    Y->*FY|e
    F->(E)|i
 非终结符：
    E，H，T，Y，F
 终结符:
    i,+,*,(,),#
"""


from prettytable import PrettyTable
table = PrettyTable(["步骤", "分析栈", "当前输入a","剩余输入串", "所用产生式"])

# 构造预测分析表
dists = {
    ('E', 'i'): 'TH',('E', '('): 'TH',('H', '+'): '+TH',
    ('H', ')'): 'e',('H', '#'): 'e',('T', 'i'): 'FY',
    ('T', '('): 'FY',('Y', '+'): 'e',('Y', '*'): '*FY',
    ('Y', ')'): 'e',('Y', '#'): 'e',('F', 'i'): 'i',
    ('F', '('): '(E)',
    }

# 构造终结符集合
Vt = ('i', '+', '*', '(', ')')

# 构造非终结符集合
Vh = ('E', 'H', 'T', 'Y', 'F')


# 获取输入栈中的内容
def printstack(stack):
    rtu = ''
    for i in stack:
        rtu += i
    return rtu


# 得到输入串剩余串
def printstr(str, index):
    rtu = ''
    for i in range(index, len(str), 1):
        rtu += str[i]
    return rtu


# 定义error函数
def error():
    print('Error')
    exit()


# 总控程序
def masterctrl(str):
    '''
    总控程序，用于进程文法的判断
    '''
    # 用列表模拟栈
    stack = []
    location = 0
    # 将#号入栈
    stack.append(str[location])

    # 将文法开始符入栈
    stack.append('E')
    # 将输入串第一个字符读进a中
    location += 1
    a = str[location]

    flag = True
    count = 1       #计算步骤
    table.add_row([count, printstack(stack),a, printstr(str, location),''])
    while flag:
        if count == 1:
            pass
        else:
            if x in Vt:
                table.add_row([count, printstack(stack),a, printstr(str, location),''])
            else:
                temp = x + '->' + s
                table.add_row([count, printstack(stack),a, printstr(str, location),temp])
        x = stack.pop()
        if x in Vt:          #栈顶是终结符
            if x == str[location]:   #该字符匹配，输入串向后挪一位
                location += 1
                a = str[location]
            else:            #否则错误
                error()
        elif x == '#':       #栈顶是结束符
            if x == a:       #当前输入字符也是结束符，分析结束
                flag = False
            else:            #否则错误
                error()
        elif (x, a) in dists.keys():    #M[x,a]是产生式
            s = dists[(x, a)]
            for i in range(len(s) - 1, -1, -1):         #倒序入栈
                if s[i] != 'e':
                    stack.append(s[i])
        else:
            error()
        count += 1


if __name__ == '__main__':
    str = '#i+i#'
    masterctrl(str)
    table.align['步骤'] = 'l'
    table.align['分析栈'] = 'l'
    table.align['剩余输入串'] = 'l'
    table.align['所用产生式'] = 'l'
    table.align['当前输入a'] = 'l'
    print(table)
    print("分析成功!")
