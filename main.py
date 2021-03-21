import string

from util import save_index


import nltk
from collections import defaultdict
# Assuming we're working with English
from nltk.stem.snowball import EnglishStemmer
import re
from gensim.parsing.preprocessing import remove_stopwords
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer
import time
import pickle


if __name__ == "__main__":
    # raw_data_blocks = load_data_blocks()

    # print(raw_data_blocks)
    # save_index(raw_data_blocks.compute())

    # clean_data = filter_data_blocks(raw_data_blocks)

    file = open("full.csv", "rt")
    data = file.readlines()
    # data = clean_data
    # data = data[:20000]
    first = True
    dic = {}
    dic2 = {}
    dic3 = {}
    line_counter = 0
    words_per_article = []
    for line in data:
        line_counter += 1
        if line_counter % 100 == 0:
            print(line_counter)
        if first:
            first = False
            continue
        # print(line)
        try:
            line_split = line.split(",", 9)
            content = line_split[9]
            doc_id = line_split[1]
        except Exception as e:
            print(e)
            print(line_counter)
            continue

        content = unidecode(content).replace('"', '').replace("'", '')
        content = content.replace(".", " ")
        content = content.replace(",", " ")
        content = content.translate(str.maketrans('', '', string.punctuation))
        content = content.lower()

        title = unidecode(line_split[2]).replace('"', '').replace("'", '')
        title = title.replace(".", " ")
        title = title.replace(",", " ")
        title = title.translate(str.maketrans('', '', string.punctuation))
        title = title.lower()
        # FILTER STOP WORDS HERE
        filtered_content = remove_stopwords(content)
        content = filtered_content
        filtered_title = remove_stopwords(title)
        title = filtered_title
        # sentences = content.split('123dot321')
        words = content.split()
        artlen = len(words)
        if artlen < 10:
            continue
        words_title = title.split()
        words2 = []
        words_title2 = []
        for i in words:
            words2.append(EnglishStemmer().stem(i))
        words = words2
        for i in words_title:
            words_title2.append(EnglishStemmer().stem(i))
        words_title = words_title2

        # words2 = [word for word in words if not word in stopwords.words()]
        # words = words2
        words_per_article.append(len(words))

        doc_dic = {}
        doc_dic2 = {}
        doc_dic3 = {}
        for w in words:
            # print(w)
            # print(EnglishStemmer().stem(w))
            # input()
            if w in doc_dic:
                doc_dic[w] += 1
            else:
                doc_dic[w] = 1
        for w in words_title:
            # print(w)
            # print(EnglishStemmer().stem(w))
            # input()
            x = int(artlen // 100)
            if x > 10:
                x = 10
            if x < 3:
                x = 3
            if w in doc_dic:
                doc_dic[w] += x
            else:
                doc_dic[w] = x

        # for s in sentences:
        #     words = s.split()
        #     words2 = []
        #     for i in words:
        #         words2.append(EnglishStemmer().stem(i))
        #     words = words2
            # for i in range(len(words)-1):
            #     w2 = str(words[i]+" "+words[i+1])
            #     if w2 in doc_dic2:
            #         doc_dic2[w2]+=1
            #     else:
            #         doc_dic2[w2]=1

            # for i in range(len(words)):
            #     for j in range(len(words)):
            #         if words[i] != words[j] and abs(i-j) < 5 and doc_dic[words[i]] > 2 and doc_dic[words[j]] > 2:
            #             if words[i] > words[j]:
            #                 w3 = str(words[j]+" "+words[i])
            #             else:
            #                 w3 = str(words[j]+" "+words[i])
            #             if w3 in doc_dic3:
            #                 doc_dic3[w3]+=1
            #             else:
            #                 doc_dic3[w3]=1

        for w in doc_dic:
            if doc_dic[w] / (artlen + 1) > 1:
                print("ALARMA")
                print([doc_id, doc_dic[w] / (artlen + 1),
                      artlen, line_split[2], content[:300]])
                input()
            if artlen > 250:
                rel = doc_dic[w] / (artlen + 1)
            else:
                rel = doc_dic[w] / (artlen + 1) * artlen / 250
            if w in dic:
                dic[w].append(
                    [doc_id, rel, artlen, line_split[2], content[:300]])
                if len(dic[w]) > 600:
                    dic[w].sort(key=lambda x: x[1], reverse=True)
                    dic[w] = dic[w][:400]
            else:
                dic[w] = [[doc_id, rel, artlen, line_split[2], content[:300]]]

        # for w in doc_dic2:
        #     if w in dic2:    # for w in doc_dic2:
        #     if w in dic2:
        #         dic2[w].append([doc_id, doc_dic2[w]/artlen, artlen, line_split[2]])
        #     else:
        #         dic2[w] = [[doc_id, doc_dic2[w]/artlen, artlen, line_split[2]]]
        #         dic3[w].append([doc_id, doc_dic3[w]/artlen, artlen])
        #         # print(len(dic3[w]))
        #     else:
        #         dic3[w] = [[doc_id, doc_dic3[w]/artlen, artlen]]
        #     if len(dic3[w]) > 200:
        #         # print('resizing     '+str(w))
        #         dic3[w].sort(key = lambda x: x[1], reverse=True)
        #         dic3[w] = dic3[w][:100]

    for i in dic:
        dic[i].sort(key=lambda x: x[1], reverse=True)

    # for i in dic2:
    #     dic2[i].sort(key = lambda x: x[1], reverse=True)

    # for i in dic3:
    #     dic3[i].sort(key = lambda x: x[1], reverse=True)

    # data = data.translate(str.maketrans('', 'to_pop = []
    # for i in dic:
    #     if dic[i] == 1:
    #         to_pop.append(i)

    # for i in to_pop:
    #     dic.pop(i)

    # for i in to_pop:
    #     dic.pop(i)

    # print(dic)
    # print(len(dic))
    # print(min(words_per_article))
    # print(words_per_article.index(min(words_per_article)))
    # print(max(words_per_article))

    # print(dic["work"][:6])
    # print(dic["working"][:6])
    # print(dic['man'][:6])
    # print(dic['men'][:6])

    # a_file = open("dic1.pkl", "wb")

    # pickle.dump(dic, a_file)

    # a_file.close()
    save_index(dic, "dic1_index")

    print(len(dic))
    # print(len(dic2))
    # print(len(dic3))

    # print(dic2[EnglishStemmer().stem("work")+" "+EnglishStemmer().stem("desk")])
    start = time.time()
    counter = 0
    candidates = []
    for i in dic['work']:
        if counter > 10:
            break
        for j in dic['desk']:
            if i[0] == j[0]:
                candidates.append([i[0], i[1] + j[1], i[3], i[4]])
                counter += 1
                if counter > 10:
                    break

    print('counter')
    print(counter)

    candidates.sort(key=lambda x: x[1], reverse=True)
    print(candidates[:7])
    end = time.time()
    print(end - start)
