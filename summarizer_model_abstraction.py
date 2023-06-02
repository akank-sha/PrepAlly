""" This file takes different concept net model function and combines them into one function function call.
    It's ab abstraction layer for the model.
"""
from summarizer import Summarizer
from summarizer_model_base_functions import get_wordsense,get_distractors_wordnet, get_distractors_conceptnet, get_nouns_multipartite, tokenize_sentences, get_sentences_for_keyword
import re
import random

def sanitizeCorpusForPreProcessing(corpus):
    """ This function takes a corpus and preprocesses it.
        It uses the concept net model to generate questions.
    """
    model = Summarizer()
    result = model(corpus, min_length=60, max_length = 500 , ratio = 0.4)
    summarized_text = ''.join(result)
    keywords = get_nouns_multipartite(corpus) 
    filtered_keys=[]
    for keyword in keywords:
        if keyword.lower() in summarized_text.lower():
            filtered_keys.append(keyword)
    return [filtered_keys,summarized_text]


def preProcessCorpusForNet(summarizedText,filteredKeys):
    sentences = tokenize_sentences(summarizedText)
    keyword_sentence_mapping = get_sentences_for_keyword(filteredKeys, sentences)
    return keyword_sentence_mapping


def getDistractorFromPreProcessedCorpus(keyWordSentenceMapping):
    key_distractor_list = {}
    for keyword in keyWordSentenceMapping:
        if len(keyWordSentenceMapping[keyword])!=0:
            wordsense = get_wordsense(keyWordSentenceMapping[keyword][0],keyword)
        if wordsense:
            distractors = get_distractors_wordnet(wordsense,keyword)
            if len(distractors) ==0:
                distractors = get_distractors_conceptnet(keyword)
            if len(distractors) != 0:
                key_distractor_list[keyword] = distractors
        else:
            
            distractors = get_distractors_conceptnet(keyword)
            if len(distractors) != 0:
                key_distractor_list[keyword] = distractors
    return key_distractor_list


def getQuestionsFromDistractors(keyDistractorList, keyWordSentenceMapping):
    index = 1
    questions = []
    for each in keyDistractorList:
        if len(keyWordSentenceMapping[each])!=0:
            try:
                currentQuestion = {"question":"","choices":[],"moreOptions":[]}
                sentence = keyWordSentenceMapping[each][0]
                pattern = re.compile(each, re.IGNORECASE)
                output = pattern.sub( " _______ ", sentence)
                currentQuestion["question"] = output
                choices = [each.capitalize()] + keyDistractorList[each]
                top4choices = choices[:4]
                random.shuffle(top4choices)
                optionchoices = ['a','b','c','d']
                for idx,choice in enumerate(top4choices):
                    currentQuestion["choices"].append({"choice":choice, "index":optionchoices[idx], "isCorrect":False})
                randomlyCorrectAnsIndex = random.randint(0,3)
                currentQuestion["choices"][randomlyCorrectAnsIndex]["isCorrect"] = True
                currentQuestion["moreOptions"] = choices[4:20]
                questions.append(currentQuestion)
            except Exception as e:
                print(e)
            index = index + 1
    return questions


def generateQuestionsFromCorpus(corpus) :
    """ This function takes a corpus and generates questions from it.
        It uses the concept net model to generate questions.
    """
    [filteredKeys, sanitizedText] = sanitizeCorpusForPreProcessing(corpus)
    keyWordSentenceMapping = preProcessCorpusForNet(sanitizedText,filteredKeys)
    keyDistractorList = getDistractorFromPreProcessedCorpus(keyWordSentenceMapping)
    questions = getQuestionsFromDistractors(keyDistractorList, keyWordSentenceMapping)
    return questions
    
if __name__ == "__main__":
    f = open("hi.txt","r",encoding="utf-8")
    full_text = f.read()   
    questions = generateQuestionsFromCorpus(full_text)
    print(questions)
