try:
    import os # os module 
    import sys # sys module
    from bs4 import BeautifulSoup
    from selenium import webdriver # webdriver
    from selenium.webdriver import Chrome # chrome 
    from selenium.webdriver.common.keys import Keys # keys
    from selenium.webdriver.common.by import By # by
    from selenium.webdriver.support.ui import WebDriverWait # webdriverwait
    from selenium.webdriver.support import expected_conditions # expected conditions
    from selenium.common.exceptions import TimeoutException # time out exception
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support import expected_conditions as EC # options
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    import time # time module 
    import re
    import json
    import random
    import requests # request img from web
    import shutil # save img locally
    import numpy as np  
    print("all modules are loaded!")
except ModuleNotFoundError as e:
    print(e)
class SneakerScraper:
    shops = []
    with open("user_agent.txt","r") as f:
        user_agents = [agent for agent in f.readlines()]
        f.close()
    link = "https://www.google.com/search?q=sneakers+uk+online+(%22%40gmail.com%22)+OR+(%22%40%22)+OR+(%22Instagram%22)&sxsrf=ALiCzsbQlfGUsiCjxCYlbAoI8JvKJRP8pQ:1672345491746&ei=k_etY9yPLcbUxc8Pl6CZoAs&start=0&sa=N&ved=2ahUKEwicpei31J_8AhVGavEDHRdQBrQ4ZBDy0wN6BAgaEAQ&biw=1680&bih=939&dpr=1"
    def scraper(self):
        options = Options()
        options.add_argument(f'user-agent={random.choice(self.user_agents)}')
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe",options=options)
        driver.set_window_size(500,700)
        driver.get(self.link)
        #WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="tsuid_9"]/div/div/div/a[1]')))
        while True:
            i = 200
            while i < 2000:
                driver.execute_script(f"window.scrollTo(0, {int(i)});")
                time.sleep(2)
                bs_obj = BeautifulSoup(driver.page_source,features="html.parser")
                infos = bs_obj.find_all("div",{"class":re.compile("kvH3mc BToiNc UK95Uc")})
                for info in infos:
                    shop = f"{info.get_text()}".strip()
                    if shop is not None:
                        if shop not in self.shops:
                            self.shops.append(f"{shop}")
                            print(shop)
                            print("\n")
                i = i + i
            try:
                next_page = driver.find_element(By.XPATH,'//*[@id="pnnext"]/span[2]')
                next_page.click()
            except:
                print(f"Scraping Done! \n Total data {len(self.shops)}")
                break
        print("File Saved Successfully!")
    def cleaner(self):
        final_data_emails = []
        final_data_insta_ids = []
        with open("data.txt","r",encoding="utf-8") as f:
            data = f"{f.readlines()}".split(":::::")
            shops = [shop for shop in data]
            for item in shops:
                emails = []
                numbers = []
                insta_ids = []
                #print(item)
                if item.lower().startswith("how"):
                    shops.remove(item)
                elif item.lower().startswith("where"):
                    shops.remove(item)
                
                insta_pattern = re.compile(r"@([a-zA-Z0-9]+)")
                pattern = re.compile(r"([a-zA-Z0-9]+)\@([a-zA-Z0-9]+)\.(com|org|edu)")
                matches = pattern.finditer(item)
                for email in matches:
                    if email.group() is not None:
                        if email.group() not in emails:
                                emails.append(email.group())
                inst_matches =insta_pattern.finditer(item)
                for item in inst_matches:
                    if item.group() is not None:
                        if item.group() not in insta_ids:
                            if item.group().lower().strip() != "@gmail":
                                if item.group().lower().strip() != "@the":
                                    if item.group().lower().strip() != "@hotmail":
                                        insta_ids.append(item.group())
                final_data_emails.append(emails)
                final_data_insta_ids.append(insta_ids)
            with open("insta.txt","w",encoding="utf-8") as f:
                for item in final_data_insta_ids:
                    for item1 in item:
                        f.write(item1)
                        f.write("\n") 
                f.close()
            with open("emails.txt","w",encoding="utf-8") as f:
                for item in final_data_emails:
                    for item1 in item:
                        f.write(item1)
                        f.write("\n") 
                f.close()              
    def run(self):
        self.scraper()
        with open("data.txt","w",encoding="utf-8")as f:
            for item in self.shops:
                f.write(item)
                f.write(":::::")
            f.close()
        self.cleaner()
if __name__ == "__main__":
    bot = SneakerScraper()
    bot.run()