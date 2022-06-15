from bs4 import BeautifulSoup
import webbrowser
import threading
import requests
import time
import math
import os   

chrome_path = None
isAutomatic = None
outputDirectory = None
RequestCooldown = 0.5

print("+------------------------------------------- MULTIUP.ORG LINK SCRAPER -------------------------------------------+")
print("|                                 1. Output download links for manual opening                                    |")
print("|                                    2. Open download links in browser                                           |")
print("+----------------------------------------------------------------------------------------------------------------+")
print("This script was made by u/Nick_Zacker. Please message me if you encounter any problems.")
print("!!! MADE EXCLUSIVELY FOR MULTIUP.ORG/DOWNLOAD LINKS !!!")
print("!!! CREATE A FILE CALLED 'URLLoader.txt' IN THE SAME DIRECTORY AND INSERT YOUR MULTIUP DOWNLOAD LINKS (DO NOT INCLUDE NEWLINES) !!!\n")
choice = input("Enter choice (1 OR 2) >> ")
if choice == "1":
    isAutomatic = False
    outputDirectory = input("Enter Output Directory (or write DEFAULT to use the default directory (output.txt)) >> ")
    if outputDirectory.lower() == "default":
        outputDirectory = "output.txt"
elif choice == "2":
    chrome_path = input("Enter Browser Path (Or write DEFAULT to use the default path (Only compatible w/ Chrome and may cause problems)) >> ")
    if chrome_path.lower() == "default":
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    isAutomatic = True

    RequestCooldown = input("Enter Request Cooldown (URL Requests Per Second) (Default is 0.5 RPS to avoid overflowing your RAM) >> ")
else:
    print(f"Choice {choice} is not an option."); input()

print("\nReading URLs...\n")

class Scraper:
    def __init__(self, openCooldown = 1, browserpath = None):
        self.openCooldown = openCooldown
        self.browserpath = browserpath

        self.elapsedTime = 0
        self.enableThread = True

    def Scrape_HTML_Element(self, url, element, params=None):
        try:
            url_request = requests.get(url)
            html_page = url_request.text

            soup = BeautifulSoup(html_page, "html.parser")
            if params == None:
                return soup.findAll(element)

            else:
                ParamsList = []
                for link in soup.findAll(element):
                    ParamsList.append(link.get(params))
                    return ParamsList

        except Exception as ParseExcpt:
            return str(ParseExcpt)

    def CalculateElapsedTime(self):
        while self.enableThread:
            s = 0
            while s <= 1:
                time.sleep(0.1)
                s += 0.1
                self.elapsedTime += 0.1

    def OpenURL(self, urls, isAutomatic):
        if "<class 'list'>" not in str(type(urls)):
            return f"Error: {urls} must be a list."
        
        else:
            if not isAutomatic:
                with open(outputDirectory, "w") as output:
                    output.write("")

            urlIteration = 0
            urlHosters = []
            chosenHoster = ""
            useDefault = "n"

            startThread = False

            for url in urls:
                url = url.replace('download', 'en/mirror')
                url_request = None
                try:
                    url_request = requests.get(url)
                except Exception:
                    print(f"\nFinished Scraping in {math.ceil(self.elapsedTime)}s.")
                    if not isAutomatic:
                        print(f'Trying to open "{outputDirectory}"... (or you can manually open it in the same directory as this script)')
                        os.system(f"notepad.exe {outputDirectory}")

                    input(); quit()

                html_page = url_request.text

                soup = BeautifulSoup(html_page, "html.parser")
                for link in soup.findAll('button'):
                    if useDefault == "n":
                        for element in soup.findAll('button'):
                            try:
                                if str(element.get('namehost')) != "None":
                                    urlHosters.append(str(element.get('namehost')))
                            except Exception as e: print(e)

                        print(f"{len(urlHosters)} Hoster(s) Detected (Some of them may be invalid, you gotta check for it yourself.):")
                        index = 0
                        for urlHoster in urlHosters:
                            index += 1
                            print(f"    {index}. {urlHoster}")
                        chosenHoster = input("\nWhich hoster would you like to use? (Use the index of their corresponding hosters) >> ")
                        chosenHoster = int(int(chosenHoster) - 1)
                        useDefault = input(f'Use Hoster "{urlHosters[chosenHoster]}" as the default hoster? (y/n) >> ')
                        useDefault = useDefault.lower()

                    if urlHosters[chosenHoster] in str(link.get('link')):
                        url = str(link.get('link'))
                
                urlIteration += 1
                if not startThread:
                    startThread = True
                    threading.Thread(target=self.CalculateElapsedTime, daemon=True).start()

                print(f'[ Iteration: {urlIteration} | Elapsed Time: {math.ceil(self.elapsedTime)}s ] Requesting URL "{url}"', end="\r")
                try:
                    if isAutomatic:
                        webbrowser.get(self.browserpath).open(url) 
                        time.sleep(self.openCooldown)
                    else:
                        with open(outputDirectory, "a") as output:
                            output.write(f"{url}\n")
                except Exception as e:
                    self.enableThread = False
                    #print(str(e)) Enable for fixing bugs
            self.enableThread = False
            quit()
with open("URLLoader.txt") as LoaderObj:
    Urls = [Urls.rstrip('\n') for Urls in LoaderObj]
    inst = Scraper(openCooldown=RequestCooldown)
    inst.OpenURL(Urls, isAutomatic=isAutomatic)
