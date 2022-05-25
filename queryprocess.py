import json
import ast
import re
from nltk.stem import PorterStemmer
def proccessdocs(words):
    symbolssp=['.','-','\n',',',';',':']
    symbols=['(',')','?-',"'",'(', ')','?-','.','"','?','$','--','-','”','`','~','×','—','“','\\','+','<','>','[',']','{','}','!','#','@','$','%','^','&','=','–']
    # words = words.replace('\n\n', ' ')
    for s in symbolssp:
        words=words.replace(s,' ')
    for s in symbols:
        if s not in symbolssp:
            words=words.replace(s,'')
    # |} | { | [ |] | \ | / | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |  # |%|^|&|!|@
    words = re.split('\s|;|,|\*|:', words)
    return  words

def readinv(): #Method to read Inv_Index from file
    i = open("inverted.txt")
    inv=i.read()
    js=ast.literal_eval(inv)
    return js
def readpos(): #Method to read Pos_Index from file
    i = open("position.txt")
    pos=i.read()
    js=ast.literal_eval(pos)
    return js
def union(l1 , l2): #method to perform Or operation on two lists
    result=[]

    len1=len(l1)
    len2=len(l2)
    i=0
    j=0
    while i < len1 and j < len2:

        if l1[i] == l2[j]:
            result.append(l1[i])
            i = i+1
            j = j+1
        elif l1[i] < l2[j]:
            result.append(l1[i])

            i = i+1
        else:
            result.append(l2[j])
            #i = i + 1
            j=j+1
    while i < len1:
            result.append(l1[i])
            i = i+1
    while j < len2:
            result.append(l2[j])
            j = j + 1
    return result
def intersectopt(l): # method for intersection optimal
   # print(l[0])
   # print(l[1])
   # print(l[2])
    l=sorted(l,key=len)
    result=intersect(l[0],l[1])
    for i in range(2,len(l)):
        result=intersect(result,l[i])
    return result
def unionall(l): #method for union of multiple lists
    result=union(l[0],l[1])
    for i in range(2,len(l)):
        result=union(result,l[i])
    return result

def intersect(l1 , l2): #method for intersection of two lists
    result=[]

    len1=len(l1)
    len2=len(l2)
    i=0
    j=0
    while i < len1 and j < len2:

        if l1[i] == l2[j]:
           # print(type(l1[i]))
            result.append(l1[i])
            i = i+1
            j = j+1
        elif int(l1[i]) < int(l2[j]):
            i = i+1
        else:
            j = j+1
    return result

def proxquery(t1, t2, k): #method for proximity query
    result=[]
    l1=list(t1.keys())
    l2=list(t2.keys())
    com=intersect(l1,l2)
    for x in com:
        c1=t1[x]
        c2=t2[x]
        for x1 in c1:
            for x2 in c2:
                if abs(x1-x2)<=k+1:
                    if x not in result:
                        result.append(x)



    return result
def not_1(l1): #method for Not operation
    uni = list(range(1,449))
    j = 0
    res=[]
    i=0
    while j<len(l1):

        if uni[i]!=l1[j]:
            res.append(uni[i])

        else:
            j = j + 1
        i+=1
    while i<len(uni):
        res.append(uni[i])
        i+=1
    return res

def queryparse(inv_index,pos_index,ps): #method to parse boolean query
    print("please enter query or type exit to exit the program:")
    query = input()
    if query.lower()=='exit':
        return True
    query = proccessdocs(query)
    terms = []
    op = []
    notop = {}
    i = 1

    for w in query:
        if w.lower() == 'and' or w.lower() == 'or' or ('/' in w.lower()):
            op.append(w.lower())

        elif w.lower() == 'not':
            notop[i] = 'not'

        else:
            terms.append(ps.stem(w.lower()))
            i = i + 1
    if len(op) == 0 and len(notop) == 0:
        print(inv_index[terms[0]])
    elif len(notop) == 1 and len(terms) == 1 and len(op) == 0 and notop[1] == 'not':
        print(not_1(inv_index[terms[0]]))

    elif '/' == op[0][0]:
        op[0] = op[0].replace('/', '')
        print(proxquery(pos_index[terms[0]], pos_index[terms[1]], int(op[0])))
    else:
        ml = []
        for t in terms:
            ml.append(inv_index[t])
        for k in notop.keys():
            ml[k - 1] = not_1(ml[k - 1])

        if 'or' not in op:
            print(intersectopt(ml))
        elif 'and' not in op:
            print(unionall(ml))
        else:
            res = ml[0]
            for i in range(0, len(op)):
                if op[i] == 'and':

                    res = intersect(res, ml[i + 1])
                elif op[i] == 'or':

                    res = union(res, ml[i + 1])


            print(res)
            return False
inv_index = readinv()
pos_index = readpos()
ps = PorterStemmer()

while True:
    if queryparse(inv_index,pos_index,ps):
        break



