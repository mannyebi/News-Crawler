import requests
from bs4 import BeautifulSoup
import json
import time

class SingeltonCrawler(object):
    def __new__(cls, *args, **kwargs):
        """create a singelton instance, if not created. and if created before
            this will just return the previous object.
        """
        if not hasattr(cls, "instance"):
            cls.instance=super(SingeltonCrawler, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        """initalize a session if not initialized before. 
        """
        if not hasattr(self, "initalized"):
            self.initalized = True
            #create a session so it can presist certain parameters in multiple HTTP requests.
            self.session = requests.session()
            #configure your requests.if server doesn't respond withing 10 seconds, request will fail.
            #user_agent refers to the machine that send request to the server.
            self.config = {"user_agent": "WebCrawler/1.0", "timeout": 10}

    def crawl(self, url, max_page) ->str:
        """send a get request throw self.session, define its headers using self.config
        """
        headers = {"User-Agent": self.config['user_agent']}
        try:
            final_response = ""
            with self.session as s:
                searched_urls = 1
                while searched_urls <= max_page:
                    url_to_search = url + f"?page={searched_urls}"
                    response = s.get(url_to_search, headers=headers, timeout=self.config["timeout"])
                    final_response += f"{response.text} \n"
                    print(f"{url_to_search} - crawled")
                    searched_urls += 1
                return final_response
        except Exception as e:
            print(f"Error occure while crawling {url}: {e}")
            return None
        

def html_parser(html_text):
    """convert the html file into parsed html file
    """
    Crawler_obj = SingeltonCrawler()
    print("parsing started")
    try:
        bs = BeautifulSoup(html_text, "html.parser")
    except TypeError as e:
        print("couldn't parse.")
    a_tags = bs.find_all("a", {"class":"ssrcss-1mrs5ns-PromoLink exn3ah91"})
    print(f"found {len(a_tags)} <a> elements")
    for a in a_tags:
        link = a.get("href")
        title = a.string
        if title:
            Crawler_obj.news_list = Crawler_obj.news_list | {title:link}
    
        

def result_in_json():
    """save the fetched newses in a json file.
    """
    newsCrawler = SingeltonCrawler()
    with open("news.json", "w") as newsFile:
        json.dump(newsCrawler.news_list, newsFile)


if __name__ == "__main__":
    url = "https://www.bbc.co.uk/news/topics/cp7r8vglnnwt"
    max_page = 5
    start = time.time()
    
    crawler = SingeltonCrawler()
    crawler.news_list = {}
    response_in_text = crawler.crawl(url, max_page)
    html_parser(response_in_text)
    result_in_json()
    end = time.time()
    execute_time = end-start
    print(f"{url} crawled in {execute_time}")