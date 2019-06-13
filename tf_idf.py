import re
import pandas
import jieba
import operator
import time
import pickle

start_time = time.time()
term_freq_dict = {}
doc_list = []
tmp_list = []
voc_list = []
with open("西游记_吴承恩_shushu8.com.txt", "r", encoding="utf-8") as f:
    while 1:
        line = f.readline()
        if line:
            if re.match(r'第[0-9]{3}', line):
                doc_list.append(tmp_list)
                voc_list += list(set(tmp_list))
                voc_list = list(set(voc_list))
                tmp_list = []
            else:
                tmp_list += jieba.lcut(line)
        else:
            break
# 计算IDF值，因为这个过程比较耗时间所以可以计算完之后保存结果用的时候直接从文件加载
# for voc in voc_list:
#     for doc in doc_list:
#         if doc.__contains__(voc):
#             try:
#                 term_freq_dict[voc] += 1
#             except KeyError:
#                 term_freq_dict[voc] = 1
#             continue
#
# import math
# term_idf_dict = {}
# for t in term_freq_dict:
#     term_idf_dict[t] = math.log2(term_freq_dict[t]/100)
#
# 保存结果
# idf_pkl = open("idf_pkl", "wb")
# pickle.dump(term_idf_dict, idf_pkl, -1)
# idf_pkl.close()
#
# 加载结果
idf_pkl_r = open("idf_pkl", "rb")
term_idf_dict = pickle.load(idf_pkl_r)
idf_pkl_r.close()


def get_keyword(num_doc):
    doc_tf_idf_dict = {}
    term_freq = pandas.value_counts(pandas.Series(doc_list[num_doc]))
    for t in term_freq.keys():
        if len(t) > 1:
            try:
                doc_tf_idf_dict[t] = -term_freq[t]*term_idf_dict[t]
            except KeyError:
                pass
    sorted_list = sorted(doc_tf_idf_dict.items(),
                         key=operator.itemgetter(1), reverse=True)
    return sorted_list


keyword_list = get_keyword(72)
print("耗时：%s s" % int(time.time()-start_time))
print(50*"=")
print("词\t\t\t\ttf-idf")
print(50*"=")
for idx, k in enumerate(keyword_list):
    if idx < 100:
        print("%-25s\t%10s" % (k[0], str(k[1])))
        print(50*"-")
    else:
        break
