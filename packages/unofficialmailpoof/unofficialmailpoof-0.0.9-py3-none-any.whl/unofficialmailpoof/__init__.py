from time import sleep
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MailpoofBot:
    def __init__(self, email, noheadless=0):
        chrome_options = Options()
        if noheadless == 0:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        if (os.path.isdir(os.path.join(os.getcwd(), 'unofficialmailpoof', 'uBlock0.chromium'))):
            chrome_options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'unofficialmailpoof', 'uBlock0.chromium'))
        if (os.path.isdir(os.path.join(os.getcwd(), 'uBlock0.chromium'))):
            chrome_options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'uBlock0.chromium'))
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1280, 800)
        if not re.match(email, 'mailpoof'):
            email = email + '@mailpoof.com'
        self.driver.get("https://mailpoof.com/mailbox/" + email)
        sleep(5)
        # Now try to click on consent ads
        try:
            ad_btn = self.driver.find_element_by_class_name('ljEJIv')
            ad_btn.click()
        except:
            pass        
        sleep(1)
        try:
            cookie_btn = self.driver.find_element_by_class_name('cookie_policy_close')
            cookie_btn.click()
        except:
            pass

    def getmails(self):
        mails = self.driver.find_elements_by_class_name('mail-item')
        mailarray = []

        for m in mails:
            self.driver.find_element_by_id(m.get_attribute("id")).click()
            sleep(1)
            mailelement = self.driver.find_element_by_id("content-" + m.get_attribute("id"))
            linkelements = self.driver.find_elements_by_tag_name("a")
            links = []
            meta = mailelement.text.split('\n', 3)
            x = re.findall("\S+@\S{3,}", meta[1])
            text = mailelement.text

            for link in linkelements:
                if re.search("^((?!mailpoof).)*$", link.get_attribute("href")) is not None:
                    links.append(link.get_attribute("href"))

            mail = [meta[0], x[0], meta[2], text, links]
            mailarray.append(mail)

        return mailarray


def getallmails(email,noheadless=0):
    mp = MailpoofBot(email, noheadless)
    # First try to fetch mails
    mails = mp.getmails()
    # If no mails are found, the following code will start until mails are fetched before the deadline
    if (mails == []):
        sleep(5)
        mails = mp.getmails()
    if (mails == []):
        sleep(10)
        mails = mp.getmails()
    if (mails == []):
        sleep(15)
        mails = mp.getmails()
    if (mails == []):
        sleep(20)
        mails = mp.getmails()
    if (mails == []):
        sleep(25)
        mails = mp.getmails()
    if (mails == []):
        sleep(30)
        mails = mp.getmails()
    return mails
