import re
keyword = {'main':1, 'int':2, 'char':3, 'if':4, 'else':5, 'for':6, 'while':7,'return':8,'void':9}

Symbol = {'=': 21, '+': 22, '-': 23, '*': 24, '/': 25, '(': 26, ')': 27, '[': 28, ']': 29, '{': 30,
          '}': 31, ',': 32, ':': 33, ';': 34, '>': 35, '<': 36, '>=': 37, '<=': 38, '==': 39, '!=': 40}

#总正则表达式
# all=re.compile('(\d+\.\d+[eE][-+]?\d+|\d+\.\d+|[1-9]\d*|0[0-7]+|0x[0-9a-fA-F]+|[a-zA-Z_]\w*|&gt;&gt;|&lt;&lt;|::|-&gt;|\.|\+=|\-=|\*=|/=|%=|&gt;=|&lt;=|==|!=|&amp;&amp;|\|\||\+|\-|\*|/|=|&gt;|&lt;|!|^|%|~|\?|:|,|;|\(|\)|\[|\]|\{|\}|\'|\")')
all=re.compile('([0-9]+[a-z|A-Z|_]+[0-9]*|\d+\.\d+[eE][-+]?\d+|\d+\.\d+|[1-9]\d*|0[0-7]+|0x[0-9a-fA-F]+|'
               '[a-z|A-Z|0-9|_]*\".*?\"[a-z|A-Z|0-9|_]*|[a-zA-Z_]\w*|\".*\"|>>|<<|'
               '::|->|\+=|\-=|\*=|/=|%=|>=|<=|==|!=|&&|\|\||\+|\-|\*|/|=|>|'
               '<|!|\^|%|\~|\?|:|,|;|\(|\)|\[|\]|\{|\}|\"|\')')


def Judge(s):
    if s[0].isalpha() and s in keyword:         #判断关键字
        print('( ',s,'->',keyword[s],' )')
    elif s[0].isalpha() and s not in keyword and s.isalnum():     #判断标识符
        print('( ', s, '->', 10, ' )')
    elif s.isdigit():                           #判断数字
        print('( ', s, '->', 20, ' )')
    elif s in Symbol:                           #判断运算符或边界符
        print('( ', s, '->', Symbol[s], ' )')
    else:
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':    #判断字符串
            print('( ',s, '->', 50, ' )')
        else:                                   #没定义或者错误串
            print('( ',s,'->','暂无定义',' )')

if __name__ == '__main__':
    #读取文件
    f = open('E://test.txt', 'r')
    result = []
    for line in f:
        if len(line) == 1:
            result.extend(line)
        else:
            result.extend(all.findall(line))
    print(result)
    # 去掉列表中残留的空字符
    for i in result:
        if '' in result:
            result.remove('')

    #词法分析
    for i in result:
        Judge(i)




# import re
# all=re.compile('([0-9]+[a-z|A-Z|_]+|\d+\.\d+[eE][-+]?\d+|\d+\.\d+|[1-9]\d*|0[0-7]+|0x[0-9a-fA-F]+|'
#                '[a-z|A-Z|0-9|_]*\".*\"[a-z|A-Z|0-9|_]*|[a-zA-Z_]\w*|\".*\"|>>|<<|'
#                '::|->|\+=|\-=|\*=|/=|%=|>=|<=|==|!=|&&|\|\||\+|\-|\*|/|=|>|'
#                '<|!|^|%|~|\?|:|,|;|\(|\)|\[|\]|\{|\}|\"|\')')
#
# ss = 'int main(){ int a = 1;"}'
# list = []
# f = open('E://test.txt','r')
# for line in f:
#     if len(line) == 1:
#         list.extend(line)
#     else:
#         list.extend(all.findall(line))
# print(list)