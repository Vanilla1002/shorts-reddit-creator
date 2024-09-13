import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

url_confession = 'https://www.reddit.com/r/confession/top/'
chrome_path =r'C:\Users\user\AppData\Local\Google\Chrome\chromedriver.exe' 
class RedditPostInfo:
    def __init__(self, label, link, score):
        self.label = label
        self.link = link
        self.score = score
    def __dict__(self):
        return {
            self.label : {
            "link": self.link,
            "score": self.score
            }
        }


#setting up the driver
def setup_driver(url : str):
    service = Service(executable_path=chrome_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    driver.implicitly_wait(10)
    return driver


def use_driver(url : str)-> list:
    driver = setup_driver(url)
    time.sleep(5)  
    #open the post, scroll down

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_articles = soup.find_all("article")
    driver.quit()
    return  [article for article in all_articles]


def information_of_articles(list_of_articles : list , minimum_score : int) -> list:
    result  = []
    for article in list_of_articles:
        shreddit_post = article.find('shreddit-post')
        
        label = article.get("aria-label")
        link = shreddit_post.get("content-href")

        score = shreddit_post.get("score")
        
        if int(score) > minimum_score:
            RedditPostInfoElement = RedditPostInfo(label, link, score)
            result.append(RedditPostInfoElement)
    return result


def text_of_articles(article_link : str) -> str:
    request = requests.get(article_link)
    soup = BeautifulSoup(request.text, "html.parser")
    text = soup.find("div", {"class": "md"}).get_text()
    text.replace("\n", " ")
    return text

x = information_of_articles(use_driver(url_confession),0)

for article in x:
    print (article.label, text_of_articles(article.link))

