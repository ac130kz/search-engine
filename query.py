import argparse
import pickle
import string
from util import timeit, load_index
from nltk.stem.snowball import EnglishStemmer
from gensim.parsing.preprocessing import remove_stopwords
import nltk 
from nltk.corpus import wordnet 

@timeit
def query(index: dict, request: str):
    request = request.replace("."," ")
    request = request.replace(","," ")
    request = request.translate(str.maketrans('', '', string.punctuation))
    request = request.lower()
    request = remove_stopwords(request)
    raw_request = request
    words = request.split()
    words2 = []
    for i in words:
        words2.append(EnglishStemmer().stem(i))
    words = words2


    if len(words) == 1:
        if request in index:
            if len(index[request]) >=5:
                for i in range(5):
                    print(index[request][i])
            else:
                candidates = []
                synonyms = []
                for i in index[request]:
                    candidates.append(i)
                for syn in wordnet.synsets(raw_request): 
                    for l in syn.lemmas(): 
                        synonyms.append(l.name()) 
                for i in set(synonyms):
                    s = EnglishStemmer().stem(i)
                    for i in range(min(5,len(index[s]))):
                        candidates.append([index[s][i][0],index[s][i][1]/2,index[s][i][2],index[s][i][3],index[s][i][4]])
                candidates.sort(key = lambda x: x[1], reverse=True)
                for i in range(5):
                    print(candidates[i])
        else:
            candidates = []
            synonyms = []
            for syn in wordnet.synsets(raw_request): 
                for l in syn.lemmas(): 
                    synonyms.append(l.name()) 
            for i in set(synonyms):
                s = EnglishStemmer().stem(i)
                if s in index:
                    for i in range(min(5,len(index[s]))):
                        candidates.append([index[s][i][0],index[s][i][1]/2,index[s][i][2],index[s][i][3],index[s][i][4]])
                else:
                    continue
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
            

    if len(words) == 2:
        counter = 0
        candidates = []
        for i in index[words[0]]:
            if counter > 10:
                break
            for j in index[words[1]]:
                if i[0] == j[0]:
                    candidates.append([i[0],i[1]+j[1],i[2],i[3],i[4]])
                    counter+=1
                    if counter > 10:
                        break
        if len(candidates) >= 5:
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
        else:
            if words[0] in index:
                for i in range(min(5,len(index[words[0]]))):
                    candidates.append([index[words[0]][i][0],index[words[0]][i][1]/10000,index[words[0]][i][2],index[words[0]][i][3],index[words[0]][i][4]])
            if words[1] in index:
                for i in range(min(5,len(index[words[1]]))):
                    candidates.append([index[words[1]][i][0],index[words[1]][i][1]/10000,index[words[1]][i][2],index[words[1]][i][3],index[words[1]][i][4]])
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])

    if len(words) == 3:
        counter = 0
        candidates = []
        for i in index[words[0]]:
            if counter > 10:
                break
            for j in index[words[1]]:
                if i[0] == j[0]:
                    candidates.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter+=1
                    if counter > 10:
                        break
        counter2 = 0
        candidates2 = []
        for i in index[words[1]]:
            if counter2 > 10:
                break
            for j in index[words[2]]:
                if i[0] == j[0]:
                    candidates2.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter2+=1
                    if counter2 > 10:
                        break
        for i in candidates2:
            candidates.append(i)
        if len(candidates) >= 5:
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
        else:
            if words[0] in index:
                for i in range(min(5,len(index[words[0]]))):
                    candidates.append([index[words[0]][i][0],index[words[0]][i][1]/10000,index[words[0]][i][2],index[words[0]][i][3],index[words[0]][i][4]])
            if words[1] in index:
                for i in range(min(5,len(index[words[1]]))):
                    candidates.append([index[words[1]][i][0],index[words[1]][i][1]/10000,index[words[1]][i][2],index[words[1]][i][3],index[words[1]][i][4]])
            if words[2] in index:
                for i in range(min(5,len(index[words[2]]))):
                    candidates.append([index[words[2]][i][0],index[words[2]][i][1]/10000,index[words[2]][i][2],index[words[2]][i][3],index[words[2]][i][4]])
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
    

    if len(words) == 4:
        counter = 0
        candidates = []
        for i in index[words[0]]:
            if counter > 10:
                break
            for j in index[words[1]]:
                if i[0] == j[0]:
                    candidates.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter+=1
                    if counter > 10:
                        break
        counter2 = 0
        candidates2 = []
        for i in index[words[1]]:
            if counter2 > 10:
                break
            for j in index[words[2]]:
                if i[0] == j[0]:
                    candidates2.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter2+=1
                    if counter2 > 10:
                        break
        counter3 = 0
        candidates3 = []
        for i in index[words[2]]:
            if counter3 > 10:
                break
            for j in index[words[3]]:
                if i[0] == j[0]:
                    candidates3.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter3+=1
                    if counter3 > 10:
                        break
        for i in candidates3:
            candidates.append(i)
        if len(candidates) >= 5:
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
        else:
            if words[0] in index:
                for i in range(min(5,len(index[words[0]]))):
                    candidates.append([index[words[0]][i][0],index[words[0]][i][1]/10000,index[words[0]][i][2],index[words[0]][i][3],index[words[0]][i][4]])
            if words[1] in index:
                for i in range(min(5,len(index[words[1]]))):
                    candidates.append([index[words[1]][i][0],index[words[1]][i][1]/10000,index[words[1]][i][2],index[words[1]][i][3],index[words[1]][i][4]])
            if words[2] in index:
                for i in range(min(5,len(index[words[2]]))):
                    candidates.append([index[words[2]][i][0],index[words[2]][i][1]/10000,index[words[2]][i][2],index[words[2]][i][3],index[words[2]][i][4]])
            if words[3] in index:
                for i in range(min(5,len(index[words[3]]))):
                    candidates.append([index[words[3]][i][0],index[words[3]][i][1]/10000,index[words[3]][i][2],index[words[3]][i][3],index[words[3]][i][4]])    
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
        
        
    if len(words) == 5:
        counter = 0
        candidates = []
        for i in index[words[0]]:
            if counter > 10:
                break
            for j in index[words[1]]:
                if i[0] == j[0]:
                    candidates.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter+=1
                    if counter > 10:
                        break
        counter2 = 0
        candidates2 = []
        for i in index[words[1]]:
            if counter2 > 10:
                break
            for j in index[words[2]]:
                if i[0] == j[0]:
                    candidates2.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter2+=1
                    if counter2 > 10:
                        break
        counter3 = 0
        candidates3 = []
        for i in index[words[2]]:
            if counter3 > 10:
                break
            for j in index[words[3]]:
                if i[0] == j[0]:
                    candidates3.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter3+=1
                    if counter3 > 10:
                        break
        for i in candidates3:
            candidates.append(i)
        counter4 = 0
        candidates4 = []
        for i in index[words[3]]:
            if counter4 > 10:
                break
            for j in index[words[4]]:
                if i[0] == j[0]:
                    candidates4.append([i[0],i[1]+j[1],j[2],i[3],i[4]])
                    counter4+=1
                    if counter4 > 10:
                        break
        for i in candidates4:
            candidates.append(i)
        if len(candidates) >= 5:
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])
        else:
            if words[0] in index:
                for i in range(min(5,len(index[words[0]]))):
                    candidates.append([index[words[0]][i][0],index[words[0]][i][1]/10000,index[words[0]][i][2],index[words[0]][i][3],index[words[0]][i][4]])
            if words[1] in index:
                for i in range(min(5,len(index[words[1]]))):
                    candidates.append([index[words[1]][i][0],index[words[1]][i][1]/10000,index[words[1]][i][2],index[words[1]][i][3],index[words[1]][i][4]])
            if words[2] in index:
                for i in range(min(5,len(index[words[2]]))):
                    candidates.append([index[words[2]][i][0],index[words[2]][i][1]/10000,index[words[2]][i][2],index[words[2]][i][3],index[words[2]][i][4]])
            if words[3] in index:
                for i in range(min(5,len(index[words[3]]))):
                    candidates.append([index[words[3]][i][0],index[words[3]][i][1]/10000,index[words[3]][i][2],index[words[3]][i][3],index[words[3]][i][4]])
            if words[4] in index:
                for i in range(min(5,len(index[words[4]]))):
                    candidates.append([index[words[4]][i][0],index[words[4]][i][1]/10000,index[words[4]][i][2],index[words[4]][i][3],index[words[4]][i][4]])        
            candidates.sort(key = lambda x: x[1], reverse=True)
            for i in range(min(5,len(candidates))):
                print(candidates[i])

    return


def loop(index):
    while True:
        request = input("> ")
        if not request:
            break
        print(f"quering: {request}")
        query(index, request)


if __name__ == "__main__":
    nltk.download('wordnet')
    index = load_index("dic1_index.zstd")
    loop(index)
