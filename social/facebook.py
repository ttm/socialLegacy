import time
from splinter import Browser

class ScrapyBrowser:
    """Opens a browser for user to login to facebook.

    Such browser pulls data as requested by user."""
    def __init__(self,user_email=None, user_password=None):
        print("Opening *Scrappy* firefox browser. Please wait.")
        self.browser=browser=Browser(wait_time=2)
        url="http://facebook.com"
        browser.visit(url)
        if (not user_email) or (not user_password):
            input("==> Input user and password and login, please.\
                    and then press <enter>")
        else:
            browser.fill("email",user_email)
            browser.fill("pass",user_password)
            browser.find_by_value("Log In").click()
    def getFriends(self,user_id="astronauta.mecanico"):
        """Returns user_ids (that you have access) of the friends of your friend with user_ids"""
        self.browser.visit("http://www.facebook.com/{}/friends".format(user_id))
        # div class fsl fwb fcb // a href="https://www.facebook.com/vjpalm?fref=pb&hc_location=friends_tab"
        while user_id not in self.browser.url:
            self.browser.visit("http://www.facebook.com/{}/friends".format(user_id))
        h1=0
        h2=self.browser.evaluate_script("document.body.scrollHeight")
        T=time.time()
        while 1:
            h1=self.browser.evaluate_script("document.body.scrollHeight")
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            h2=self.browser.evaluate_script("document.body.scrollHeight")
            if h1 != h2:
                T=time.time()
            elif time.time()-T>10:
                break

        # find stop condition
        links=self.browser.find_link_by_partial_href("hc_location=friends_tab")
        self.friend_ids=set([l["href"].split("/")[-1].split("?")[0] for l in links])
        return self.friend_ids

        




