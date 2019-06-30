from collections import defaultdict
def remove_recall(production):
    sets = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    # f = open('E://test3.txt','r')
    # production = []
    Vn = set()
    # for line in f:
    #     data = line.strip()  #读取每一行
    #     production.append(data)
    #     Vn.add(data[0])
    for i in production:
        Vn.add(i[0])

    sets = set(sets)
    sets -= Vn
    sets = list(sets)
    
    result = {}     #保存整个文法的结果
    for i in range(len(production)):
        X, Y = production[i].split('->')    #左右部分开
        Y = Y.split('|')                    #右部根据|再分
        s = sets.pop()                      #弹出一个字符作为回溯的处理
        dicts = defaultdict(list)

        for Yi in Y:
            dicts[Yi[0]].append(Yi)     #根据候选式的首字符分组放进字典

        temp1 = []  # 保存有回溯的候选式
        temp2 = []        # 保存没有回溯的候选式
        flag = False    # 存在回溯的标志

        result_tmp = {}     #保存每个产生式的结果
        ss = ''
        for k,v in dicts.items():
            if len(v) > 1:      #存在回溯
                flag = True
                #找到公共左因子ss
                zipped = zip(*v)  #拉链函数 比如zip(*[abc,abd]) 将列表的元素作为参数传递给zip >>> (a,a),(b,b),(c,d)
                for i in zipped:
                    if len(set(i)) == 1:    #是公共左因子的部分就拼接
                        ss += i[0]
                    else:
                        break
                #去掉有回溯的候选式的公共左因子
                for i in range(len(v)):
                    dicts[k][i] = dicts[k][i].replace(ss,'')
                    if dicts[k][i] == '':       #候选式刚好等于公共左因子
                        dicts[k][i] = 'ε'
                temp1.extend(dicts[k])
            else:               #不存在回溯的候选式
                temp2.extend(dicts[k])

        #存在回溯的处理
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
                    nonrecall =  nonrecall + temp2[i]
                else:
                    nonrecall = nonrecall + temp2[i] + '|'
            result_tmp[X] = X + '->' + ss + s + '|' + nonrecall
        #不存在回溯的处理
        else:
            for Yi in Y:
                result_tmp[X] = production[i]
        result.update(result_tmp)
    result_new =[]
    for k,v in result.items():
        result_new.append(v)
    print(result_new)

# 消除左递归
sets = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
def remove_recursion():
    f = open('E://test1.txt','r')
    production = []
    Vn = set()
    for line in f:
        data = line.strip()  #读取每一行
        production.append(data)
        Vn.add(data[0])

    # print(production)
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


Code = remove_recursion()
remove_recall(Code)