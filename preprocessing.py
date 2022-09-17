'''
预处理baker数据集的label
最后分别生成训练集和数据集，存在filelists下
'''
import re
import random

from text.utils_ch import pinyin_dict

old_label_path = 'filelists/origin_baker_label.txt'
train_label_path = 'filelists/baker_train_with_01234.txt'
val_label_path   = 'filelists/baker_val_with_01234.txt'


def add_label(l1,l2):
    '''根据l1中的label，将#1#2#3#4添加到l2中的对应位置，并插入#0停顿'''
    l1 = list(re.findall('[A-Za-z\u4e00-\u9fa5#1234]',l1))
    l2 = l2.split(" ")
    l1.reverse()
    l2.reverse()
    pinyin_list = list()
    i=j=0
    while i < len(l1):
        if l1[i] in '1234' and l1[i+1]=='#':
            add = '#'+l1[i]
            pinyin_list.append(add)
            i+=1
        else:
            if j < len(l2):
                pinyin_list.append(l2[j])
                j+=1
        i+=1
    pinyin_list.reverse()
    '''此处在每一个音素的后面插入一个#0停顿'''
    final_list = pinyin_list
    k = 0
    final_length = len(l2)*2    #最终长度为音节数量的两倍，即每个音节后面一个停顿，！能够处理带有儿化音的长度问题
    try:
        while k <= final_length - 1:
            # 如果这个值不是停顿符，下一个值也不是停顿符，就是一个音素
            if pinyin_list[k][0] !='#' and pinyin_list[k+1][0] != '#':
                final_list.insert(k+1,'#0')
                k+=1
            k+=1
    except:
        print(final_length)
        print(k,final_list)
        print(l1)
        print(l2)

    return ' '.join(final_list)

'''将baker的标注进行处理，放入all_list中'''
all_list=list()
with open(old_label_path,'r') as f:
    lines = f.readlines()
    for i in range(0,len(lines),2):
        wav, labels = lines[i].strip().split('\t')
        pys = lines[i+1].strip()
        wav_path = 'baker_waves/' + wav +'.wav'
        pys_added = add_label(labels,pys)
        
        one_piece = wav_path + '|' + pys_added + '|' + labels
        # print(one_piece)
        all_list.append(one_piece)

'''我们现在不处理儿化音和中英混合情况，所以要处理all_list中存在的特殊字符，返回all_list_without_erhua列表'''
all_list_without_erhua = list()
for line in all_list:
    line_list = line.strip().split('|')
    wav_path, pys, real_labels = line_list[0], line_list[1],line_list[2]
    py_list = pys.split(' ')
    result = ['sil']
    flag = 0 # 是否含有儿化或未知字符的flag
    for py in py_list:
        if py[:-1] in pinyin_dict:
            tone = py[-1]
            a = py[:-1]
            a1, a2 = pinyin_dict[a]
            result += [a1, a2 + tone]
        else:
            if py[:-1] != '#':
                # print(py) #打印儿化音或未知字符
                flag = 1
                break
            else:
                result += ['#'+py[-1]]

    if flag == 0:
        result+=['sil','eos']
        new_line = wav_path + '|'+' '.join(result) + "|" +real_labels
        all_list_without_erhua.append(new_line)

print(all_list_without_erhua[:10])

random.shuffle(all_list_without_erhua)
train_list,val_list = all_list_without_erhua[200:],all_list_without_erhua[:200]
with open(train_label_path,'w') as f2:
    for p in train_list:
        f2.write(p)
        f2.write('\n')
with open(val_label_path,'w') as f3:
    for p in val_list:
        f3.write(p)
        f3.write('\n')
