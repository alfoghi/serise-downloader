import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import subprocess
from time import sleep

class AnimeDL():
    def __init__(self):
        self.search = None
        self.selectname = None
        self.selectsesson = None
        self.selected_name = None
    def searsh(self):
        url = "https://wecima.show/search/"

    # Ask user to input the name of the movie
        name = str(input("enter the name of the move ")).strip()

    # Send a GET request to the search URL with the movie name
        r = requests.get(url + name.upper())

    # Parse the response using BeautifulSoup
        supe = BeautifulSoup(r.text, "html.parser")

    # Lists to store movie names and URLs
        movelist = []
        urls_list = []

    # Find all movie items in the search results
        for names in supe.find("div", {"class": "Grid--WecimaPosts"}).findAll("div", {"class": "GridItem"}):
            if names is not None:
            # Extract the movie title and URL, and add them to the lists
                movelist.append(names.find("a")["title"].strip("فيلم الاكشن و المغامرة هدة فيلم مترجم"))
                urls_list.append(names.find("a")["href"])
            else:
                print(f"{name} is not found")

    # Return the lists of movie names and URLs
        self.search_results = (movelist, urls_list)
        return self.search_results
    
    
    def select_name(self):
            if not self.search_results:
                raise Exception("Step 1 must be completed before Step 2")

            movelist, urls_list = self.search_results

            for index, value in enumerate(movelist):
                print(index, value)

            while True:
                try:
                    choice = int(input("Enter the number of your choice: "))
                    if 0 <= choice < len(movelist):
                        print(f"You chose  {movelist[choice]}")
                        self.selected_name = movelist[choice]
                        self.choose_results = urls_list[choice]
                        return self.choose_results
                    else:
                        print(f"Please choose a number between 0 and {len(movelist) - 1}")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")


    def select_session(self):
        url = self.choose_results
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        self.session_urls = []
        self.session_names =[]
        season_div = soup.find("div", {"class": "List--Seasons--Episodes"})
        if season_div:
            season_links = season_div.findAll("a")
            for link in season_links:
                self.session_urls.append(link["href"])
                self.session_names.append(link.text)

            while self.session_names:
                for index, name in enumerate(self.session_names):
                    print(index, name)

                try:
                    choice = int(input("Enter the number of your choice: "))
                    if 0 <= choice < len(self.session_names):
                        chosen_url = self.session_urls[choice]
                        print(f"Start downloading from {chosen_url}")
                        self.chosen_sesson = chosen_url
                        return self.chosen_sesson
                    else:
                        print(f"Please choose a number between 0 and {len(self.session_names) - 1}")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            print("Only one season available.")
            return self.choose_results
        
    def downloading_server(self,url):
        r = requests.get(url)
        supe = BeautifulSoup(r.text,"html.parser")  
        dwonload_server = supe.find("div", {"class": "Download--Wecima--Single"}).find("ul", {"class": "List--Download--Wecima--Single"})
        download_url = dwonload_server.find("a")["href"]
        options = webdriver.ChromeOptions()

        options.add_experimental_option("detach", True) 
        options.add_argument('--headless') 
        options.add_argument('--allow-running-insecure-content') 
        driver = webdriver.Chrome(options=options)
        driver.get(download_url)
        self.current_url = driver.current_url
        return self.current_url
        
        
        
    def startDwonload(self):
        self.urls = []
        url =  self.choose_results
        r= requests.get(url)
        supe = BeautifulSoup(r.text,"html.parser")
        lsitepsodes = supe.find("div",{"class":"Episodes--Seasons--Episodes"})
        for i in  reversed(lsitepsodes.findAll("a")):
            print(f"downloading {i.text}")
            self.urls.append(self.downloading_server(i["href"]))
            sleep(1)
        with open(f"{self.selected_name}.txt", "w") as file:
            for url in  self.urls:
                file.write(url + "\n")

        return "done"

        
        
        
        
        
        
        
        
anime_dl= AnimeDL()
searsh = anime_dl.searsh()
selctname =anime_dl.select_name()
selectsesson= anime_dl.select_session()
startDwonload = anime_dl.startDwonload()

print(startDwonload)
