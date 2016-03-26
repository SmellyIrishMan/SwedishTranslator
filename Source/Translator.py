# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser
import pickle

from subprocess import Popen
from anki import Collection

Config = ConfigParser.ConfigParser()
Config.read("TranslatorConfig.ini")
#print(Config.sections())

colLoc = Config.get("Translator", "ankiCollectionDir")
translatorFolder = Config.get("Translator", "directory")
pickleFilename = Config.get("Translator", "pickleFilename")
pronuncLoc = Config.get("Translator", "downloadFolder")

addNewEntryKey = "A"
exitKey = "X"
confirmKey = "Y"

#utf-8 is the same as cp65001
print("What's the stdIn encoding? " + sys.stdin.encoding)

deck = Collection(colLoc)
#print(deck.models.current())

def GetNewWord():
    newWord = raw_input("Enter word to translate. X to exit; ").decode(sys.stdin.encoding)
    return newWord

def CapitaliseList(wordsToCap):
    capped = []
    for word in wordsToCap:
        capped.append(word.title())
    return capped

newWord = GetNewWord()
while newWord.upper() != exitKey.upper():
    print("\nSimilar words...")
    cardsIDs = deck.findCards(newWord)

    i = 1
    for cardID in cardsIDs:
        card = deck.getCard(cardID)
        phrase = deck.getNote(card.nid)["Phrase"]
        translation = deck.getNote(card.nid)["Translation"]
        pronuncFiles = deck.getNote(card.nid)["Pronunciation"]
        print("\t" + str(i) + "; " + phrase + " - " + translation)
        card = deck.getCard(cardID)
        i = i + 1

    print("Add " + newWord + ". (Y)es? ")
    choice = raw_input().decode(sys.stdin.encoding)
                       
    if choice.upper() == confirmKey.upper():
        print("Adding a new entry.")

        #WE CONVERT TO iso-8859-1 here because that's the format of the bat file.
        print("Grabbing info from the web.")
        p = Popen(["StartWebFetcher.bat", newWord.encode("iso-8859-1")], cwd=translatorFolder)
        stdout, stderr = p.communicate()
        #p.wait()

        #print(os.getcwd())
        print("Returning to Translator")
        pkl_file = open(translatorFolder + pickleFilename, 'rb')
        phrasesAndTranslations = pickle.load(pkl_file)
        downloadedFiles = pickle.load(pkl_file)

        capitalisedPhrases = CapitaliseList(phrasesAndTranslations[0])
        capitalisedTranslations = CapitaliseList(phrasesAndTranslations[1])

        phrases = "/".join(capitalisedPhrases)
        translations = "/".join(capitalisedTranslations)

        newEntry = deck.newNote()
        newEntry["Phrase"] = phrases
        newEntry["Translation"] = translations
        for filepath in downloadedFiles:
            result = deck.media.addFile(filepath)
            filename = filepath[filepath.rfind("/")+1:]
            mediaID = u"[sound:" + filename + u"]"
            newEntry["Pronunciation"] = newEntry["Pronunciation"] + mediaID

        print("Add new note;")
        print(newEntry["Phrase"])
        print(newEntry["Translation"])
        print(newEntry["Pronunciation"])
        confirmation = raw_input("(Y)es? ")
        if confirmation.upper() == confirmKey.upper():
            deck.addNote(newEntry)
            deck.save()
            print("NEW ENTRY ADDED! :D")
        else:
            print("NEW ENTRY IGNORED, FIX THE ISSUES.")
    else:
        print("OK, you already have that word I guess :). Learn it better!")
    newWord = GetNewWord()

deck.close()
