# -*- coding: utf-8 -*-
import sys
import pickle

from DefinitionDownloader import GetTranslations
from DefinitionDownloader import ChooseOptionsFromTranslations
from PronuncDownloader import DownloadPronunciations

pickleFilename = "PickledPTD.pkl"

wordToFind = sys.argv[1]
#wordToFind = "vilja"

print ("We're looking for " + wordToFind)

translations = GetTranslations(wordToFind)

if translations:
    phrasesAndTranslations = ChooseOptionsFromTranslations(translations)
    print(phrasesAndTranslations)
    print()

    downloadedFiles = DownloadPronunciations(phrasesAndTranslations[0])

    output = open(pickleFilename, 'wb')
    pickle.dump(phrasesAndTranslations, output, 2)
    pickle.dump(downloadedFiles, output, 2)
    output.close()
else:
    print("No definitions for " + wordToFind + " found.")
