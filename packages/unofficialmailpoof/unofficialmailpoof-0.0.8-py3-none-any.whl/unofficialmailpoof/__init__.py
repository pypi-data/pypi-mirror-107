from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MailpoofBot:
    def __init__(self, email, noheadless=0):
        chrome_options = Options()
        if noheadless == 0:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1280, 800)
        if not re.match(email, 'mailpoof'):
            email = email + '@mailpoof.com'
        self.driver.get("https://mailpoof.com/mailbox/" + email)
        sleep(9)
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
    mails = mp.getmails()
    return mails
