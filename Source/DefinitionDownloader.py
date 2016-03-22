# -*- coding: utf-8 -*-

import sys
import re

from robobrowser import RoboBrowser

class Translation:
    def __init__(self, baseWord, wClass, trans):
        self.baseWord = baseWord
        self.wordClass = wClass
        self.translations = trans

def GetTranslations(wordToFind):
    print("\nGet translations for " + wordToFind)
    # Browser
    browser = RoboBrowser(history=True, parser="html5lib")

    #Open the login page. Setup our login info. Submit the info.
    print ("Connecting to Ord.se ...")
    browser.open('http://www.ord.se/oversattning/engelska/?s='+wordToFind+'&l=SVEENG')
    definitions = browser.find_all(class_="search-result-word-wrapper")

    Translations = []
    #Get rid of defitions without class... :)
    for definition in definitions:
        #print(definition)
        #print()
        wordClasses = definition.find_all(class_="word-class")
        if not wordClasses:
            definitions.remove(definition)
        else:
            for wordClass in wordClasses:
                wordClass = wordClass.getText()
                #print(definition)
                #print("\n")
                actualSearchWord = definition.find(class_="search-result-head-word").getText()
                actualSearchWord = actualSearchWord.rstrip()
                htmlDefinitions = definition.find_all(class_="normal font1 readable")
                translations = []
                for translation in htmlDefinitions:
                    translations.append(translation.getText())
                Translations.append(Translation(actualSearchWord, wordClass, translations))
    return Translations

def ChooseOptionsFromTranslations(translations):
    wordIndex = 1
    for translation in translations:
        try:
            print("   " + str(wordIndex) + ". " + translation.baseWord + " - " + translation.wordClass)
        except UnicodeEncodeError:
            print("         Unhandled character in string. Maybe a ... or something")
            
        translationIndex = 1
        for option in translation.translations:
            try:
                print("      " + str(wordIndex) + "." + str(translationIndex) + "; " + option)
                translationIndex = translationIndex + 1
            except UnicodeEncodeError:
                print("         Unhandled character in string. Maybe a ... or something")
        wordIndex = wordIndex + 1

    prompt = "Choose the options (1.1 3.4 etc...) you wish to take; "
    choices = input(prompt).split()

    firstWord = translations[int(choices[0].split('.')[0]) - 1]
    wordForms = GetWordForms(firstWord.baseWord, firstWord.wordClass)

    phrasesAndTranslations = [wordForms, []]
    for choice in choices:
        wordIndex = int(choice.split('.')[0]) - 1
        translationIndex = int(choice.split('.')[1]) - 1
        translation = translations[wordIndex]
        phrasesAndTranslations[1].append(translation.translations[translationIndex])
    return phrasesAndTranslations

def GetWordForms(word, wordClass):
    print("\nGetting the forms of " + word + " (" + wordClass + ")")
    #Convert the ord class to wiktionary table class form
    wordClassDict = {'SUBSTANTIV':'subst', 'VERB':'verb', 'TRANSITIVT VERB':'verb', 'INTRANSITIVT VERB':'verb', 'INTRANSITIVT DEPONENSVERB':'verb', 'ADVERB':'adverb', 'ADJEKTIV':'adj'}
    browser = RoboBrowser(history=True, parser="html5lib")
    browser.open('http://sv.wiktionary.org/wiki/'+word)
    tableClass = "template-sv-" + wordClassDict[wordClass.upper()]

    #wordFormTable = browser.find_all(class_=re.compile(r"grammar\s+"))
    wordFormTable = browser.find_all(class_=re.compile(tableClass))

    forms = [word]
    if wordFormTable:
        forms = []
        for table in wordFormTable:
            tableheader = table.find("tbody")
            tableSiblings = tableheader.find_all(class_=re.compile("b-"))
            for sibling in tableSiblings:
                if not sibling.getText() in forms and sibling.getText().isalpha():
                    forms.append(sibling.getText())
                    
        formIndex = 1
        print ("Choose the forms to use; ")
        for form in forms:
            print(str(formIndex) + ". " + form)
            formIndex = formIndex + 1
        keepIndexes = list(map(int, input().split()))

        if len(keepIndexes) > 0:
            finalForms = []
            for index in keepIndexes:
                finalForms.append(forms[index-1])
            forms = finalForms
   
    return forms

def DetermineVerbSex(verb, pageText):
    enForms = [" en " + verb + " ", " " + verb + "en "]
    enCount = pageText.count(enForms[0]) + browser.parsed.getText().count(enForms[1])

    ettForms = [" ett " + verb + " ", " " + verb + "et "]
    ettCount = pageText.count(ettForms[0]) + browser.parsed.getText().count(ettForms[1])

    if enCount > ettCount:
        return "en "
    elif enCount < ettCount:
        return "ett "
    else:
        return "?"
