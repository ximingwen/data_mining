#!/usr/bin/env python
# coding: utf-8


import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.util import ngrams
from collections import Counter
import math
import json

def fill_data():
	with open(os.getcwd()+"/tweets.txt",'r')as fh:
		filedata=fh.read()
	filedata = re.sub('#[^\s]+','',filedata)
	filedata = re.sub('@[^\s]+','',filedata)
	fh = open("tweets_new.txt", 'w')
	fh.write(filedata)
	fh.close()

def format_tweets():
	if (os.path.exists('tweets_new.txt')==False):
		fill_data()
	f=open("tweets_new.txt",'r')
	tweets=[]
	for line in f:
		if(line!="\n"):
			line=line.lower().strip('\n')
			tweets.append(line)
	f.close()
	return tweets


def count_word_freqency_has_stopwords(tweets):
	if(os.path.exists('word_frequency_dic_has_stopwords.json')==False):
		word_frequency={}
		for tweet in tweets:
			token_list = nltk.word_tokenize(tweet)
			token_list2 = list(filter(lambda token: nltk.tokenize.punkt.PunktToken(token).is_non_punct, token_list))
			list_final=set(token_list2)
			for word in list_final:
			    if(word in word_frequency):
			    	word_frequency[word]+=1
			    else:
			    	word_frequency[word]=1
		jsObj = json.dumps(word_frequency)
		fileObject = open('word_frequency_dic_has_stopwords.json','w')
		fileObject.write(jsObj)
		fileObject.close()
	else:
		with open("word_frequency_dic_has_stopwords.json",'r') as load_f:
	      		word_frequency = json.load(load_f)

	return word_frequency




def count_word_frequency(tweets):
	if(os.path.exists('word_frequency_dic.json')==False):
		word_frequency={}
		for tweet in tweets:
			token_list = nltk.word_tokenize(tweet)
			token_list2 = list(filter(lambda token: nltk.tokenize.punkt.PunktToken(token).is_non_punct, token_list))
			token_list3 = list(filter(lambda token: token not in stopwords.words('english'), token_list2))
			list_final=set(token_list3)
			for word in list_final:
				if(word in word_frequency):
					word_frequency[word]+=1
				else:
					word_frequency[word]=1

		jsObj = json.dumps(word_frequency)
		fileObject = open('word_frequency_dic.json','w')
		fileObject.write(jsObj)
		fileObject.close()
	else:
		with open("word_frequency_dic.json",'r') as load_f:
	      		word_frequency = json.load(load_f)

	return word_frequency

        
def count_collocation_frequency(tweets,word_frequency,stop):
		if(os.path.exists('collocation_frequency_dic'+stop+'.json')==False):
			collocation_frequency={}
			collocation_frequency_json={}
			for tweet in tweets:
				token_list = nltk.word_tokenize(tweet)
				bigrams = set(list(ngrams(token_list,2)))# bigrams is a list and element is a tuple
				for element in bigrams:
					element_tran=(element[1],element[0])
					if((element[0] in word_frequency)and(element[1] in word_frequency)and(element[0]!=element[1])):
						string_key= json.dumps(element)
						if(element in collocation_frequency):
							collocation_frequency[element]+=1
							collocation_frequency_json[string_key]+=1
						elif(element_tran in collocation_frequency):
							collocation_frequency[element_tran]+=1
							string_key= json.dumps(element_tran)
							collocation_frequency_json[string_key]+=1
						else:
							collocation_frequency[element]=1
							collocation_frequency_json[string_key]=1
			jsObj = json.dumps(collocation_frequency_json)
			fileObject = open('collocation_frequency_dic'+stop+'.json', 'w')
			fileObject.write(jsObj)
			fileObject.close()
		else:
			with open("collocation_frequency_dic"+stop+".json",'r') as load_f:
				collocation_frequency = json.load(load_f)
		return collocation_frequency

def filter_frequency(dic,num):
	dic={key: value for key, value in dic.items() if value > num}
	return dic


def count_log_lift(collocation_frequency,word_frequency,length,num,file_name):
	count_loglift={}
	count_loglift_json={}
	frequency1=0
	frequency2=0
	for key in collocation_frequency:
		if(type(key)==str):
			list_key= json.loads(key)
			frequency1=word_frequency.get(list_key[0])/length
			frequency2=word_frequency.get(list_key[1])/length
		else:
			frequency1=word_frequency.get(key[0])/length
			frequency2=word_frequency.get(key[1])/length
		joint_frequency=collocation_frequency.get(key)/length
		value=math.log(joint_frequency/(frequency1*frequency2))
		count_loglift[tuple(list_key)]=value
		if(type(key)==tuple):
			json_key=json.dumps(key)
			count_loglift_json[json_key]=value
		else:
			count_loglift_json[key]=value
	jsObj = json.dumps(count_loglift_json)
	fileObject = open('log_lift_'+str(num)+file_name+'.json', 'w')
	fileObject.write(jsObj)
	fileObject.close()
	return count_loglift

def count_chi_square(collocation_frequency,word_frequency,length,num,file_name):
	chi_square={}
	chi_square_json={}
	for key in collocation_frequency:
		if(type(key)==str):
			list_key= json.loads(key)
		frequency1=word_frequency.get(list_key[0])
		frequency2=word_frequency.get(list_key[1])
		expect_count=frequency1*frequency2/length
		value=(collocation_frequency.get(key)-expect_count)**2/expect_count
		chi_square[tuple(list_key)]=[value]
		if(type(key)==tuple):
			json_key=josn.dumps(key)
			chi_square_json[json_key]=value
		else:
			chi_square_json[key]=value
	jsObj = json.dumps(chi_square_json)
	fileObject = open('chi_square_'+str(num)+file_name+'.json', 'w')
	fileObject.write(jsObj)
	fileObject.close()

	return chi_square

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

def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

def print_result_lift(lift,num,stop):
	str_one=""
	str_one_words=""
	for i in range(100):
		que_word=str(list(lift[i][0]))+'\n'
		que="the top"+str(i)+"is :"+str(list(lift[i][0]))+".  and the loglift value is "+str(lift[i][1])+"\n"
		print(que)
		str_one=str_one+que
		str_one_words=str_one_words+que_word
	save_to_file('top100_of_log_lift_'+str(num)+stop+'.txt',str_one)
	save_to_file('top100_of_log_lift_'+str(num)+stop+'show.txt',str_one_words)
	print("finished_saving_file\n")

def print_result_chi_square(square,num,stop):
	str_two=""
	str_two_words=""
	for i in range(100):
		que_word=str(list(square[i][0]))+'\n'
		que="the top"+str(i)+"is :"+str(list(square[i][0]))+".  and the chi_square value is "+str(square[i][1])+"\n"
		print(que)
		str_two=str_two+que	
		str_two_words=str_two_words+que_word
	save_to_file('top100_of_chi_square_'+str(num)+stop+'.txt',str_two)
	save_to_file('top100_of_chi_square_'+str(num)+stop+'show.txt',str_two_words)
	print("finished_saving_file")

def main():
	print("begin preparing sentences...")
	tweets=format_tweets()
	print("finished\n")
	print("begin calculating word_frequency...")
	word_frequency_dic=count_word_frequency(tweets)
	print("begin calculating word_frequency_dic_has_stopwords...")
	word_frequency_dic_has_stopwords=count_word_freqency_has_stopwords(tweets)
	length=len(tweets)
	print("length:"+str(length))
	print("finished\n")
	print("begin calculating collocation_frequency..")
	collocation_frequency_dic=count_collocation_frequency(tweets,word_frequency_dic_has_stopwords,'_stop')
	collocation_frequency_dic_filtered=filter_frequency(collocation_frequency_dic,100)
	print("finished\n")
	#log_lift
	print("begin calculating count_log_lift\n")
	loglift=count_log_lift(collocation_frequency_dic_filtered,word_frequency_dic_has_stopwords,length,100,"_stop")
	lift=sort_by_value_reverse(loglift)
	print_result_lift(lift,100,"_stop")
    #chi_square
	print("begin calculating chi_square\n")
	square=count_chi_square(collocation_frequency_dic_filtered,word_frequency_dic_has_stopwords,length,100,"_stop")
	square=sort_by_value(square)
	print_result_chi_square(square,100,"_stop")
	





if __name__ == "__main__":
    main()






			

