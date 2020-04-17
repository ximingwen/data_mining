import nltk
from nltk.util import ngrams
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import os


def transform_dictionary(num):
	f=open("enwiktionary.a.list.txt",'r')
	dic={}
	line = f.readline().strip('\n')
	while line: 
		dic[str(line)]=list(ngrams(str(line),num))
		line = f.readline().strip('\n')
	return dic


def transform_word(word,num):
	word=set(ngrams(word,num))
	return word

def calculate_Jaccard(target,num):
	dic=transform_dictionary(num)
	target_grams=transform_word(target,num)
	Jaccard_dic={}
	for each_word in dic:
		each_word_grams=dic.get(each_word)
	#calculate a_or_b and a_and_b

		A_or_B=len(each_word_grams)
		A_and_B=0
		for gram in target_grams:
			if (gram not in each_word_grams):
				A_or_B+=1
			if (gram in each_word_grams):
				A_and_B+=1
			Jaccard=1-(A_and_B/A_or_B)
			Jaccard_dic[each_word]=Jaccard

	return Jaccard_dic

def sort_by_value(d):
	items=d.items()
	backitems=[[v[1],v[0]] for v in items]
	backitems.sort()
	return [[backitems[i][1],backitems[i][0]] for i in range(0,len(backitems))]

def sort_by_value_reverse(d):
	items=d.items()
	backitems=[[v[1],v[0]] for v in items]
	backitems.sort(reverse=True)
	return [[backitems[i][1],backitems[i][0]] for i in range(0,len(backitems))]

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def calculate_levenshtein(word):
	f=open("enwiktionary.a.list.txt",'r')
	dic={}
	line = f.readline().strip('\n')
	while line: 
		dic[str(line)]=levenshtein(str(line),word)
		line = f.readline().strip('\n')
	return dic


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

def main():
	word_list=["abreviation","abstrictiveness","accanthopterigious","artifitial inteligwnse","agglumetation"]
	string=""
	string_show=""
	for word in word_list:
		print(word+"\n")
		string=string+word+"\n"
		string_show=string_show+word+"\n"
		print("result for"+" levenshtein:\n")
		string=string+"result for"+" levenshtein:\n"
		string_show=string_show+"result for"+" levenshtein:\n"
		J=sort_by_value(calculate_levenshtein(word))
		for i in range(10):
			str_s="top"+str(i)+"is :"+str(J[i][0])+" and the levenshtein_distance is "+str(J[i][1])
			print(str_s)
			string=string+str_s+"\n"
			string_show=string_show+str(J[i][0])+"\n"
		print("\n")
		j=2
		while(j<6):
			str_s="result for "+str(j)+"_gram:\n"
			print(str_s)
			string=string+str_s
			string_show=string_show+str_s
			J=sort_by_value(calculate_Jaccard(word,j))
			for i in range(10):
				str_s="top"+str(i)+"is :"+str(J[i][0])+" and the Jaccard is "+str(J[i][1])
				print(str_s)
				string=string+str_s+"\n"
				string_show=string_show+str(J[i][0])+'\n'
			print("\n")
			j=j+1
	save_to_file('result_for_assigenment2.txt', string)
	save_to_file("result_for_assigenment2_show.txt",string_show)




if __name__ == "__main__":
    main()



