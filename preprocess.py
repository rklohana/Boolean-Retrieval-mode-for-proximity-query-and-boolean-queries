#please pu abstracts in same folder as the program
import json
import re
from collections import OrderedDict
from nltk.stem import PorterStemmer
def proccessdocs(words):
    symbolssp=['.','-','\n',',',';',':']
    symbols=['(',')','?-',"'",'(', ')','?-','.','"','?','$','--','-','”','`','~','×','—','“','\\','+','<','>','/','[',']','{','}','!','#','@','$','%','^','&','1','2','3','4','5','6','7','8','9','0','=','–']
    # words = words.replace('\n\n', ' ')
    for s in symbolssp:
        words=words.replace(s,' ')
    for s in symbols:
        if s not in symbolssp:
            words=words.replace(s,'')
    # |} | { | [ |] | \ | / | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |  # |%|^|&|!|@
    words = re.split('\s|;|,|\*|:', words)
    words.remove('')
    return  words

def readfiles():
    inv_index = {}
    pos_index = {}
    ps=PorterStemmer()
    s = open("Stopword-List.txt")
    stopwords = s.read()
    stopwords=stopwords.lower()
    stopwords = stopwords.split("\n")

    for doc in range(1, 449):
        f = open("Abstracts/" + str(doc) + ".txt", "r")
        words = f.read()
        words=proccessdocs(words)
        # for w in words:
        #    if w not in stopwords:
        #         dictionary.add(w)
        pos=1

        for w in words:
            if w=='':
                continue
            w = w.lower()
            if w not in stopwords:

                p=ps.stem(w)
                if p not in inv_index.keys():
                    inv_index[p] = []
                if doc not in inv_index[p]:
                    inv_index[p].append(doc)

                if p not in pos_index.keys():
                    pos_index[p]={doc : [pos]}
                elif doc in pos_index[p]:
                    pos_index[p][doc].append(pos)
                else:
                    pos_index[p][doc] = [pos]
            pos = pos + 1
                #if p not in pos_index.keys():
       # print(p)



    inv_index = dict(sorted(inv_index.items()))
    pos_index = dict(sorted(pos_index.items()))
   # print(ps.stem('classification'))
    #print(inv_index)
    with open('inverted.txt', 'w') as convert_file:
        convert_file.write(json.dumps(inv_index))
    with open('position.txt', 'w') as convert_file:
        convert_file.write(json.dumps(pos_index))
    return inv_index,pos_index

i_index,p_index=readfiles()
#print(i_index)