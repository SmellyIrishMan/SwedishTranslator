# -*- coding: utf-8 -*-
import sys
import configparser
import re
from robobrowser import RoboBrowser

Config = configparser.ConfigParser()
Config.read("TranslatorConfig.ini")

forvoUsername = Config.get("ForvoLogin", "username")
forvoPassword = Config.get("ForvoLogin", "password")
saveDirectory = Config.get("Translator", "downloadFolder")

def DownloadPronunciations(words):
    print("Aiming to download " + str(words))
    browser = RoboBrowser(history=True, parser="html5lib")
    print ("Connecting to Forvo...")
    browser.open('http://www.forvo.com/login/')
    form = browser.get_form(action=re.compile(r'login'))
    form["login"].value = forvoUsername
    form["password"].value = forvoPassword
    browser.submit_form(form)

    filepaths = []
    for word in words:
        try:
            print ("Trying to download; " + word)
            #The #sv tells it to look for sverige!
            wordUrl = "http://www.forvo.com/word/" + word + "/#sv"
            browser.open(wordUrl)
        
            ConvertedDownloadWord = word
            ConvertedDownloadWord = ConvertedDownloadWord.replace("ö", "%C3%B6")
            ConvertedDownloadWord = ConvertedDownloadWord.replace("å", "%C3%A5")
            ConvertedDownloadWord = ConvertedDownloadWord.replace("ä", "%C3%A4")
            searchString = '"/download/mp3/' + ConvertedDownloadWord + '/sv/"'

            #print(browser.get_links("download"))
            #print(browser.select('a[href*="download"]'))

            downloads = browser.select('a[href*='+searchString+']')
            #for link in downloads:
            #    print(link)
            
            if downloads:
                try:
                    fullDownloadUrl = downloads[0].attrs["href"]
                    print ('Attempt to download mp3 from ' + fullDownloadUrl)
                    browser.open(fullDownloadUrl)
                    #print ('Opened the mp3 site.')
                    mp3Response = browser.response
                    #print ('Read the mp3 response.')

                    filepath = saveDirectory + word + ".mp3"
                    file = open(filepath, 'wb')             
                    file.write(mp3Response.content)
                    file.close()
                    filepaths.append(filepath)
                except IndexError:
                    print ("Could not load the webpage ", fullDownloadUrl)
                except NameError:
                    print ("I'm not sure what this was. Maybe an incorrectly encoded string")
                except:
                    print("Unexpected error while downloading:", sys.exc_info()[0])
            else:
                print ("Couldn't find a download link :(.")
                
        except NameError :
            print ("Couldn't find ",searchWord)
        except :
            print("Unexpected error while searching:", sys.exc_info()[0])
    return filepaths
