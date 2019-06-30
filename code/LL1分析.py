from prettytable import PrettyTable
from lexical_Analysis import Showstack,Showstr,error,Analysis
Vn = set()  # 非终结符集合
Vt = set()  # 终结符集合
First = {}  # First集
Follow = {}  # Follow集
GramaDict = {}  # 处理过的产生式    例如{E:{'ε','+TE'},F:{'TE','+'}}
Code = []  # 读入的产生式
AnalysisList = {}  # 分析表
StartSym = ""  # 开始符号
EndSym = '#'  # 结束符号为“#“
Epsilon = "ε"
dicts = {}

# 构造First集
def getFirst():
    global Vn, Vt, First, Follow
    for X in Vn:
        First[X] = set()  # 初始化非终结符First集为空
    for X in Vt:
        First[X] = set(X)  # 初始化终结符First集为自己
    Change = True
    while Change:  # 当First集没有更新则算法结束
        Change = False
        for X in Vn:
            for Y in GramaDict[X]:
                k = 0
                Continue = True
                while Continue and k < len(Y):
                    if not First[Y[k]] - set(Epsilon) <= First[X]:  # 没有一样的就添加，并且改变标志
                        if Epsilon not in First[Y[k]] and Y[k] in Vn and k > 0:
                            '''Epsilon not in First[Y[k]] and Y[k] in Vn and k > 0:  '''
                            Continue = False
                        else:               # Y1到Yi候选式都有ε存在
                            First[X] |= First[Y[k]] - set(Epsilon)
                            Change = True
                    if Epsilon not in First[Y[k]]:
                        Continue = False
                    k += 1
                if Continue:  # X->ε或者Y1到Yk均有ε产生式
                    First[X] |= set(Epsilon)
                    # FirstA[Y] |= set(Epsilon)

# 构造Follow集
def getFollow():
    global Vn, Vt, First, Follow, StartSym
    for A in Vn:
        Follow[A] = set()
    Follow[StartSym].add(EndSym)  # 步骤1,将结束符号加入Follow[开始符号]中
    Change = True
    while Change:           # 当Follow集没有更新算法结束
        Change = False
        for X in Vn:
            for Y in GramaDict[X]:
                for i in range(len(Y)):
                    if Y[i] in Vt:
                        continue
                    Flag = True
                    for j in range(i + 1, len(Y)):  # continue
                        if not First[Y[j]] - set(Epsilon) <= Follow[Y[i]]:
                            Follow[Y[i]] |= First[Y[j]] - set(Epsilon)  # 步骤2 FIRST(β)/ε 加入到FOLLOW(B)中。
                            Change = True
                        if Epsilon not in First[Y[j]]:
                            Flag = False
                        break
                    if Flag:            #A->αBβ and β->ε
                        if not Follow[X] <= Follow[Y[i]]:  # 步骤3 β->ε,把FOLLOW(A)加到FOLLOW(B)中
                            Follow[Y[i]] |= Follow[X]
                            Change = True

#构造分析表
def getAnalysisList():
    for k in GramaDict:  # 初始化分析表
        AnalysisList[k] = dict()
        for e in Vt:
            AnalysisList[k][e] = None
    for k in GramaDict:
        l = GramaDict[k]
        for s in l:
            if s[0].isupper():  # S->ɑ ɑ[0]属于非终结符时 包括 ɑ !-> ε 和 ɑ -> ε 的First(ɑ)
                for e in Vt:
                    if e in First[s[0]]:
                        AnalysisList[k][e] = s

            if s[0] in Vt:  ## S->ɑ ɑ[0]属于终结符 例如  select(S->+E) = First(+E) = +
                AnalysisList[k][s[0]] = s

            if (s[0].isupper() and (Epsilon in First[s[0]])) or (s == Epsilon):
                for c in Follow[k]:  # S->ɑ and ɑ->ε 的 Follow(S)
                    AnalysisList[k][c] = s

    for item,val in AnalysisList.items():
        for k in val:
            if val[k]:
                dicts.update({(item,k):val[k]})

    #画表
    print("构造LL1分析表:")
    data = []
    data.append('')
    for i in Vt:
        data.append(i)
    table1 = PrettyTable(data)
    for item in Vn:
        production = []
        production.append(item)
        for i in AnalysisList[item]:
            production.append(AnalysisList[item][i])
        table1.add_row(production)
    print(table1)


# 消除左递归
sets = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
def remove_recursion(production):
    Vn = set()
    for item in production:
        Vn.add(item[0])

    global sets
    sets = set(sets)
    sets -= Vn
    sets = list(sets)

    #消除左递归
    gdict = {}              #用字典保存消除左递归的文法
    for i in range(len(production)):
        X, Y = production[i].split('->')    #左右部分开
        Y = Y.split('|')                    #右部根据|再分
        ss = ''               # 保存候选式没有直接左递归的 消除左递归之后的字符串
        s = sets.pop()        #弹出一个非终结符集里面没有的字母
        nlx = []              #保存没有左递归的候选式
        flag = False          #存在左递归的标志
        temp = []             #保存有左递归的去掉头的候选式
        for Yi in Y:
            if Yi[0] == X:    #该候选式存在左递归
                flag = True
        if flag:              #存在左递归的处理
            for Yi in Y:
                if Yi[0] == X:          #对于E->E+T|T 的 E+T  >>>>>  E'->+TE'
                    temp.append(Yi[1:] + s)
                else:
                    gdict[X] =  Yi + s  #对于E->E+T|T 的 T  >>>>>  E->TE'
                    nlx.append(gdict[X])

            #有左递归的候选式的合并
            gdict[s] = s + '->'
            for i in range(len(temp)):
                if i == len(temp) - 1:
                    gdict[s] = gdict[s] + temp[i]
                else:
                    gdict[s] = gdict[s] + temp[i] + '|'
            if s in gdict:             #在 E'->+TE'的基础上 >>>>> E'->+TE'|ε
                gdict[s] = gdict[s] + '|ε'

            # 没有左递归的候选式的合并
            for i in range(len(nlx)):
                if i == len(nlx) - 1:
                    ss = ss + nlx[i]
                else:
                    ss = ss + nlx[i] + '|'
            gdict[X] = X + '->' + ss

        else:       #不存在左递归就直接添加改产生式
            for Yi in Y:
                gdict[X] = production[i]

    #得出消除左递归后的最终文法
    result = []
    for k,v in gdict.items():
        result.append(v)
    return result

#消除回溯
from collections import defaultdict
def remove_recall(production):
    sets = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    Vn = set()
    for i in production:
        Vn.add(i[0])

    sets = set(sets)
    sets -= Vn
    sets = list(sets)

    result = {}  # 保存整个文法的结果
    for i in range(len(production)):
        X, Y = production[i].split('->')  # 左右部分开
        Y = Y.split('|')  # 右部根据|再分
        s = sets.pop()  # 弹出一个字符作为回溯的处理
        dicts = defaultdict(list)

        for Yi in Y:
            dicts[Yi[0]].append(Yi)  # 根据候选式的首字符分组放进字典

        temp1 = []  # 保存有回溯的候选式
        temp2 = []  # 保存没有回溯的候选式
        flag = False  # 存在回溯的标志

        result_tmp = {}  # 保存每个产生式的结果
        ss = ''
        for k, v in dicts.items():
            if len(v) > 1:  # 存在回溯
                flag = True
                # 找到公共左因子ss
                zipped = zip(*v)  # 拉链函数 比如zip(*[abc,abd]) 将列表的元素作为参数传递给zip >>> (a,a),(b,b),(c,d)
                for i in zipped:
                    if len(set(i)) == 1:  # 是公共左因子的部分就拼接
                        ss += i[0]
                    else:
                        break
                # 去掉有回溯的候选式的公共左因子
                for i in range(len(v)):
                    dicts[k][i] = dicts[k][i].replace(ss, '')
                    if dicts[k][i] == '':  # 候选式刚好等于公共左因子
                        dicts[k][i] = 'ε'
                temp1.extend(dicts[k])
            else:  # 不存在回溯的候选式
                temp2.extend(dicts[k])

        # 存在回溯的处理
        if flag:
            # 有回溯的候选式的合并
            result_tmp[s] = s + '->'
            for i in range(len(temp1)):
                if i == len(temp1) - 1:
                    result_tmp[s] = result_tmp[s] + temp1[i]
                else:
                    result_tmp[s] = result_tmp[s] + temp1[i] + '|'

            # 没有回溯的候选式的合并
            nonrecall = ''
            for i in range(len(temp2)):
                if i == len(temp2) - 1:
                    nonrecall = nonrecall + temp2[i]
                else:
                    nonrecall = nonrecall + temp2[i] + '|'
            result_tmp[X] = X + '->' + ss + s + '|' + nonrecall
        # 不存在回溯的处理
        else:
            for Yi in Y:
                result_tmp[X] = production[i]
        result.update(result_tmp)
    result_new = []
    for k, v in result.items():
        result_new.append(v)
    return result_new


# 总控程序
def LL1():
    global Vn, Vt, First, Follow, StartSym, Code
    f = open('E://test1.txt','r')
    production = []
    print("原文法：")
    for line in f:          #读取文件中每一行
        data = line.strip()
        production.append(data)
        print('\t\t\t\t',data)

    StartSym = production[0][0]
    Code = remove_recursion(production) #消除左递归
    Code = remove_recall(Code)          #消除回溯
    n = int(len(Code))

    print('消除左递归和回溯：')
    for i in range(n):
        X, Y = Code[i].split('->')  #产生式的分离，生成左部和右部
        print('\t\t\t\t', Code[i])
        Vn.add(X)
        Y = Y.split('|')        #右部的分离，即每个候选式
        for Yi in Y:
            Vt |= set(Yi)
        if X not in GramaDict:
            GramaDict[X] = set()
        GramaDict[X] |= set(Y)  # 生成产生式集
    Vt -= Vn
    print('非终结符:', Vn)
    print('终结符:', Vt)
    getFirst()          # 生成全部的First集
    getFollow()         # 生成全部的Follow集
    print("FIRST集:")
    for k in Vn:
        print('     FIRST[', k, ']: ', First[k])
    print("FOLLOW集:")
    for k, v in Follow.items():
        print('     FOLLOW[', k, ']: ', v)
    Vt -= set(Epsilon)
    Vt |= set(EndSym)

    getAnalysisList()  #LL1得到分析表

    Vt.remove('#')



if __name__ == "__main__":

    LL1()

    str = input(">>>")
    for i in str:
        if i not in Vt:
            exit("输入串存在字符在文法里不存在！！！")
    table = PrettyTable(["Steps", "Stack", "Input_a_now", "Remain_str", "Use_production"])

    #这里是导入之前写好的语法分析接口
    Analysis(str,StartSym,table,dicts,Vt,Vn)

    #格式控制，输出语法分析表
    table.align['步骤'] = 'l'
    table.align['分析栈'] = 'l'
    table.align['剩余输入串'] = 'l'
    table.align['所用产生式'] = 'l'
    table.align['当前输入a'] = 'l'
    print(table)
