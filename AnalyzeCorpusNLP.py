# -*- coding: utf-8 -*-
"""
//Mert Karagöz
"""
import os
import nltk
from nltk.util import ngrams
from nltk.probability import FreqDist


FILE_PATH_TRAIN = "C:/Users/vndlz/Desktop/brown_hw/Train"

corpus = []
for path, dirs, files in os.walk(FILE_PATH_TRAIN):
    for f in files:
        fileName = os.path.join(path,f)
        with open(fileName,"r") as f:
            corpus.append(f.read())
   
#PosTags.Txt
#train'den aldığım test corpusunu kucuk harfe ve string formatına çevirdikten sonra nltk.split.str2tuple kullanarak tag'ları
#corpusLowerSTR_SPLIT'e çekiyorum. Daha sonra FreqDist ve mostcommon() kullanarak sıralamayı yapıp sırayla bastırıyorum.
#make the sentence lowerCase
corpusLowerTXT = nltk.Text(word.lower() for word in corpus)
corpusLowerSTR = str(corpusLowerTXT)
corpusLowerSTR_SPLIT = [nltk.tag.str2tuple(t) for t in corpusLowerSTR.split()]
corpusLower_TAG_FD = nltk.FreqDist(tag for (word, tag) in corpusLowerSTR_SPLIT)
PosTags = corpusLower_TAG_FD.most_common() #PosTags.txt
##buradan çıkan outputu direk text dosyasına kopyaladım hocam
##Kendi bilgisayarınızda denemek isterseniz diye print kısmını comment'ledim. yukarıdaki FILE_PATH'ı ayarlayarak deneyebilirsiniz.
print("POSTAGS.TXT ->> OK.")
with open('PosTags.txt','w') as pt:
 for item in range(len(PosTags)):
    #print(PosTags[item]) 
    pt.write(str(PosTags[item])+'\n')


# TransitionProbs.txt
# P(tagb|taga) bulmak için bigram_Sorted'da count(taga tagb)'leri bulduktan sonra hepsini count(taga)'ya böldürüyorum
# bunun için de PosTags ve bigram_Sorted'in hepsini tarayacak bir nested for loop yazdım. For loop bigram_Sorted(taga tagb)'in içinde
# PosTag (tag a) olup olmadığını kontrol ediyor ve karşılaştırmadan noktalama işaretlerini çıkartıyor.Son olarak .index() < 4 kullanarak
# tagA'ları karşılaştırdığımdan emin olduktan sonra count(taga tagb)/count(tag a) yaparakTransitionProbs.txt'ye yazdırıyor.
bigrams = ngrams((tag for (word, tag) in corpusLowerSTR_SPLIT), 2)
bigramFreq = FreqDist(bigrams)  
bigram_Sorted = bigramFreq.most_common(200)##200'den sonrasını spyder consola basınca üsttekileri silmeye başlıyor.
print("TRANSITION PROBS.TXT ->> OK.")
with open('TransitionProbs.txt','w') as tp:
 for i in range(len(bigram_Sorted)):
  for j in range(len(PosTags)):
   if (str(PosTags[j][0]) in str(bigram_Sorted[i][0])):
    if not str(bigram_Sorted[i][0]).index(str(PosTags[j][0])) < 3 and round(bigram_Sorted[i][1]/PosTags[j][1],3)<1 :
    #print(str(bigram_Sorted[i][0])+ " " +str(round(bigram_Sorted[i][1]/PosTags[j][1],3)))
     tp.write(str(bigram_Sorted[i][0])+ " " +str(round(bigram_Sorted[i][1]/PosTags[j][1],3))+'\n')

# Vocabulary.txt
# most common tagı eksik
print("Vocabulary.TXT ->> OK.")
corpusLowerSTR_WORDS = [nltk.tag.str2tuple(t) for t in corpusLowerSTR.split()]
corpusLower_WORDS_FD = nltk.FreqDist(word for (word, tag) in corpusLowerSTR_WORDS)
Vocabulary = corpusLower_WORDS_FD.most_common()
with open('Vocabulary.txt','w') as w:
 for i in range(len(Vocabulary)):     
   w.write(str(Vocabulary[i])+'\n')

# EmissionProbs.txt
# Tag/Kelime bigramlarını bulduktan sonra listeden noktalama işaretli olanları çıkartıyorum.
# sonra dosyaya yazdırma işlemi for loop içinde başlıyor.
print("EmissionProbs.TXT ->> OK.")
bigramsEP = ngrams((corpusLowerSTR_SPLIT), 1)
bigramsEP_Freq = FreqDist(bigramsEP)
bigramsEP_Sorted = bigramsEP_Freq.most_common()
dontWriteTwice = []
with open('EmissionProbs.txt','w') as ep:
 ep.write("kelime ve tag tuppleda ayni elemanda oldugu icin yerleri ters oldu."+'\n')
 for i in range(len(bigramsEP_Sorted)):
    for j in range(len(PosTags)):
     if (str(PosTags[j][0]) in str(bigramsEP_Sorted[i][0])):
        if round(bigramsEP_Sorted[i][1]/PosTags[j][1],3) < 1 :
         ep.write(str(bigramsEP_Sorted[i][0])+" "+ str(round(bigramsEP_Sorted[i][1]/PosTags[j][1],3)) +'\n')       
         continue
# InitialProbs.txt
initialProbs = []
for i in range(len(PosTags)):
    if corpusLowerSTR.startswith(str(corpusLowerSTR_SPLIT[i][0])+"/"+str(corpusLowerSTR_SPLIT[i][1])):
        initialProbs[i] = str(corpusLowerSTR_SPLIT[i][1])

FILE_PATH_TEST = "C:/Users/vndlz/Desktop/brown_hw/Test"

corpus_TEST = []
for path, dirs, files in os.walk(FILE_PATH_TEST):
    for f in files:
        fileName = os.path.join(path,f)
        with open(fileName,"r") as f:
            corpus_TEST.append(f.read())

corpusLowerTXT_TEST = nltk.Text(word.lower() for word in corpus_TEST)
corpusLowerSTR_TEST = str(corpusLowerTXT_TEST)
corpusLowerSTR_SPLIT_TEST = [nltk.tag.str2tuple(t) for t in corpusLowerSTR_TEST.split()]

counter = 0
with open('Sonuc.txt','w') as sn:
 sn.write("There are " + str(len(corpusLowerSTR_SPLIT_TEST))+" words in test corpus." + '\n' )
 for i in range(len(corpusLowerSTR_SPLIT_TEST)):
  for j in range(len(bigramsEP_Sorted)):
   if (str(corpusLowerSTR_SPLIT_TEST[i][0]) == str(bigramsEP_Sorted[j][0][0][0]) and str(corpusLowerSTR_SPLIT_TEST[i][1]) == str(bigramsEP_Sorted[j][0][0][1])):
       counter += 1
   else: 
    continue
 sn.write(str(counter)+" of "+str(len(corpusLowerSTR_SPLIT_TEST)) +" is used correctly. Algorithm count the punctuation marks, so the real result may be slight different"+'\n')

print('\n') 
FILE_PATH_ca41 = "C:/Users/vndlz/Desktop/brown_hw/Test/ca41"
 
with open(FILE_PATH_ca41) as f:
    contents_ca41 = f.read()
    
corpusLowerSTR_ca41 = contents_ca41.lower()
corpusLowerSTR_SPLIT_ca41 = [nltk.tag.str2tuple(t) for t in corpusLowerSTR_ca41.split()]

counter_ca41 = 0

with open('Sonuc.txt','a') as sn:
  sn.write("There are " + str(len(corpusLowerSTR_SPLIT_ca41))+" words in ca41." + '\n' )
  for i in range(len(corpusLowerSTR_SPLIT_ca41)):
   for j in range(len(bigramsEP_Sorted)):
    if (str(corpusLowerSTR_SPLIT_ca41[i][0]) == str(bigramsEP_Sorted[j][0][0][0]) and str(corpusLowerSTR_SPLIT_ca41[i][1]) == str(bigramsEP_Sorted[j][0][0][1])):
        counter_ca41 += 1
        sn.write(str(corpusLowerSTR_SPLIT_ca41[i][0]+"/"+str(corpusLowerSTR_SPLIT_ca41[i][1]+" ")))
    else: 
     continue
  sn.write(str(counter_ca41)+" of "+str(len(corpusLowerSTR_SPLIT_ca41)) +" is used correctly. Algorithm count the punctuation marks, so the real result may be slight different"+'\n')
  
   
