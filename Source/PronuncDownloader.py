# -*- coding: utf-8 -*-
import sys
from robobrowser import RoboBrowser

saveDirectory = "C:/Users/AAAA/Desktop/Swedish/Translator/PronunciationDownloads/"

def DownloadPronunciations(words):
    print("Aiming to download " + str(words))
    browser = RoboBrowser(history=True, parser="html5lib")
    print ("Connecting to Forvo...")
    browser.open('http://www.forvo.com/login/')
    form = browser.get_form("f_login")
    form["login"].value = 'username'
    form["password"].value = 'password'
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
            searchString = "\"/download/mp3/" + ConvertedDownloadWord + "/sv/\""
            
            downloads = browser.select('a[href^='+searchString+"]")
            #for link in downloads:
            #    print(link)
            
            if downloads:
                try:
                    fullDownloadUrl = 'http://www.forvo.com' + downloads[0].attrs["href"]
                    #print ('Attempt to download mp3 from ' + fullDownloadUrl)
                    browser.open(fullDownloadUrl)
                    mp3Response = browser.response

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
