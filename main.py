import cmath
import math
import re
import json
import os.path
import ast
from os import path
import nltk
from nltk.stem import WordNetLemmatizer
from tkinter import *
from tkinter import ttk
tf_vectors={}
idf={}
alpha=0.001


struct=Tk()
struct.geometry("354x550")
struct.title("VSM Model")
label=Label(struct,text="Personal Search Engine",bg="teal",fg="white",font=("Times",20,"bold"))
label.pack(side=TOP)
struct.config(background="teal")

game_frame = Frame(struct)
game_frame.pack(side=BOTTOM)
game_scroll = Scrollbar(game_frame)
game_scroll.pack(side=RIGHT, fill=Y)
my_game = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set)

my_game['columns'] = ('Documents')
my_game.column("#0", width=0,  stretch=NO)
my_game.column("Documents",anchor=CENTER, width=80)
my_game.heading("#0",text="",anchor=CENTER)
my_game.heading("Documents",text="Documents",anchor=CENTER)











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

    return  words

def preprocess():

    s = open("Stopword-List.txt")
    stopwords = s.read()
    stopwords = stopwords.lower()
    stopwords = stopwords.split("\n")



    n=449
    lem=WordNetLemmatizer()
   # print(lem.lemmatize('weakness'))
    for doc in range(1, 449):
        f = open("Abstracts/" + str(doc) + ".txt", "r")
        words = f.read()
        words = proccessdocs(words)
        # for w in words:
        #    if w not in stopwords:
        #         dictionary.add(w)
        tf_vectors[doc]={}
        n_word=len(words)
        flag={}
        wn=0

        for w in words:
            if w == '':
                continue
            w = w.lower()
            if w not in stopwords:
                lem_w=lem.lemmatize(w)

                if lem_w not in idf.keys():
                    idf[lem_w]=0

                if lem_w not in flag.keys():
                    flag[lem_w]=True
                if flag[lem_w]:
                    idf[lem_w]=idf[lem_w]+ 1
                    flag[lem_w]=False
                   # print(lem_w)

                if lem_w not in tf_vectors[doc].keys():
                    tf_vectors[doc][lem_w]=0
                tf_vectors[doc][lem_w]+=float(1/n_word)

    for id in idf.keys():
        #print(type(idf[id]))
        #print(type(n/(idf[id]+1)))
        #idf[id]=float(n/(idf[id]+1))
        idf[id]=math.log(float((idf[id]+1)))

    for d in tf_vectors.keys():
        for id in tf_vectors[d].keys():
            tf_vectors[d][id]=  tf_vectors[d][id]*idf[id]
            #print(type(tf_vectors[d][id]))

    with open('tf-idf.txt', 'w') as convert_file:
        convert_file.write(json.dumps(tf_vectors))
    with open('idf.txt', 'w') as convert_file1:
        convert_file1.write(json.dumps(idf))

qvec={}
def vecnorm(vec):
    mag=0
    for v in vec.keys():
        mag+= (vec[v]*vec[v])
    mag=math.sqrt(mag)
    return mag
def runquery(qvec,tf_vectors):
    ranked_list=[]
    for d in tf_vectors.keys():
        cosim=0
        for w in qvec.keys():
            if w in tf_vectors[d].keys():
                cosim+=((qvec[w]*tf_vectors[d][w]))
            if  d==299:
               print(cosim)
        cosim/=(vecnorm(qvec)*vecnorm(tf_vectors[d]))
        if cosim>=alpha:
            ranked_list.append(d)

    return ranked_list
import time
text=StringVar()

def search_query():
    count=0
    q = proccessdocs(text.get())
    qvec = tfidfquery(q)
    res=runquery(qvec,tf_vectors)
    my_game.delete(*my_game.get_children())

    for r in res:
        my_game.insert(parent='', index='end', iid=count, text='',values=(r))
        count += 1
    my_game.pack()


    game_scroll.config(command=my_game.yview)
    count1=count
def tfidfquery(q):
    qtf={}
    for w in q:
        if w not in qtf.keys():
            qtf[w]=0
        qtf[w]+=1/len(q)
    for w in qtf.keys():
        if w in idf.keys():
            qtf[w]=qtf[w]*idf[w]
    return qtf
fname='tf-idf.txt'
if path.exists(fname):
    i = open(fname)
    inv = i.read()
    tf_vectors = ast.literal_eval(inv)
    j = open('idf.txt')
    inv1 = j.read()
    idf = ast.literal_eval(inv1)
else:
    preprocess()





label=Label(struct,text="Enter here to search",bg="teal",fg="white",font=("Times",15,"bold"))
label.place(x=50,y=100)
enter=Entry(struct,font=("Times",10,"bold"),textvar=text,width=30,bd=2,bg="white")
enter.place(x=50,y=130)
button=Button(struct,text="Search",font=("Times",10,"bold"),width=30,bd=2,command=search_query)
button.place(x=50,y=170)
struct.mainloop()