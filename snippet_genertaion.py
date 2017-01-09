import math

class Snippets:
    def __init__(self, bm25_ranking, hashmap, queries):
        self.ranking = bm25_ranking
        self.h = hashmap
        self.queries = queries
        self.index = self.get_index()
        self.idf = self.idfv()

    def get_list_of_senences(self, filepath_with_name):
        f=open(filepath_with_name,'r')
        k=f.read()
        k=k.split()
        topk=12
        sentences=[]
        count=0
        while count <len(k):
            sentence=""
            if len(k)<=12:
                for i in range(0,len(k)):
                    sentence=sentence+" "+k[i]
            if count+topk>len(k):
                for i in range(count,len(k)):
                    sentence=sentence+" "+k[i]
            else:
                for i in range(count,count+topk):
                    sentence=sentence+" "+k[i]
            sentences.append(sentence)
            count=count+topk
        return sentences[:]
    
    def createIndex(self, dic,filename):
        path="tokenized_corpus/"
        d=dic.copy()
        docId = filename
        f= open(path+filename,'r')
        k = f.read()
        k = k.split()
        term_count = len(set(k))
        for c in range(0, len(k)- 1):
            item = k[c]
            if item in d:
                if docId in d[item]:
                    d[item][docId] = d[item][docId] + 1
                else:
                    d[item][docId] = 1
            else:
                d[item] = {docId: 1}
        return d.copy()

    def get_index(self):
        dic={}
        for name in self.h.values():
                dic=self.createIndex(dic.copy(),name)
        return dic.copy()

    def get_sentences_for_all_topkfiles(self, filenames):
        s=[]
        for filename in filenames:
            filename="C:/Users/saura/Downloads/tokenized_corpus/tokenized_corpus/"+filename
            s.extend(self.get_list_of_senences(filename))
        return s

    def idfv(self ):
        idf_uni={}
        N=len(self.index)
        for k,v in self.index.items():
            idf_uni[k]=math.log10(N*1.0/len(self.index[k]))
        return idf_uni.copy()

    def queryVec(self,query):
        qv={}
        q=query.split()
        N=len(q)
        for k in q:
            if k in self.idf:
                qv[k]=(float(1.0*self.occurenceofword(k,query))/N)*self.idf[k]
            else:
                qv[k]=(1.0*self.occurenceofword(k,query)/N)*1
        return qv.copy()

    def occurenceofword(self,word,query):
        q=query.split()
        count=0
        for k in q:
            if word==k:
                count=count+1
        return count*1.0

    def Cosine(self, sentences,uni,query):
        cv={}
        for sentence in sentences:
            dv=self.queryVec(sentence)
            qv=self.queryVec(query)
            sumdv=self.sqrsum(dv)
            sumqv=self.sqrsum(qv)
            c=0
            for k1, v1 in uni.items():
                if k1 in dv and k1 in qv:
                    c=c+(dv[k1]*qv[k1]*1.0)
            c=c/math.sqrt(sumdv*sumqv)
            cv[sentence]=c
        return cv.copy()

    def sqrsum(self,dv):
        c=0
        for k,v in dv.items():
            c=c+v*v
        return c

    def get_snippet(self,cv):
        l=sorted(cv, key=cv.get,reverse=True)
        return l[:10]

    def get_snippets_all(self):
        sn={}
        cacmTopk=[]
        topk=5
        for j in range (0, len(self.ranking)):
            snippet={}
            for i in range(0,topk):
                cacmTopk.append(self.ranking[j+1][i][0]) #top 10 for query 1
            filenames=[]
            for docid in cacmTopk:
                filenames.append(self.h[str(docid)])
            for filename in filenames:
                filepath_with_name="tokenized_corpus/"+filename
                sentences=self.get_list_of_senences(filepath_with_name)

            cv = self.Cosine(sentences,self.index, self.queries[j])
            snippet[filename]=cv
            new_dic={}
            for k,v in snippet.items():
                new_dic=self.makeDic(new_dic,v)

            l=sorted(new_dic,key=new_dic.get,reverse=True)
            l=l[:5]
            sn[j+1]=l

        x = self.highlight2(sn)
        return x

    def highlight2(self, sn):
        count=0
        sn2={}
        for k,v in sn.items():
            ls=[]
            for sentence in v:
                s=""
                k=sentence.split()
                for word in k:
                    if word in self.queries[count].split():
                        word=word.upper()
                    sentence=sentence+" "+word
                ls.append(sentence)
            sn2[count]=ls
            count=count+1
        return sn2

    def makeDic(self,updateDic,d):
        for k, v in d.items():
            if k not in updateDic.keys():
                updateDic[k]=v
        return updateDic

    def get_key(self,ele,snippet):
        for k,v in snippet.items():
            if ele in v.values():
                return k
    
  
    



    
    