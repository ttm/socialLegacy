import time, os, pickle, multiprocessing as mp
from splinter import Browser

class ScrapyBrowser:
    """Opens a browser for user to login to facebook.

    Such browser pulls data as requested by user."""
    def __init__(self,user_email=None, user_password=None,basedir="~/.social/"):
        self._BASE_DIR=basedir.replace("~",os.path.expanduser("~"))
        if not os.path.isdir(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)
        print("Opening *Scrappy* firefox browser. Please wait.")
        self.browser=browser=Browser(wait_time=2)
        url="http://facebook.com"
        browser.visit(url)
        if (not user_email) or (not user_password):
            input("\n\n==> Input user and password and login, please.\
                    and then press <enter>")
        else:
            browser.fill("email",user_email)
            browser.fill("pass",user_password)
            browser.find_by_value("Log In").click()
    def getFriends(self,user_id="astronauta.mecanico",write=True):
        """Returns user_ids (that you have access) of the friends of your friend with user_ids"""
        while user_id not in self.browser.url:
            self.browser.visit("http://www.facebook.com/{}/friends".format(user_id), wait_time=3)
        #self.go("http://www.facebook.com/{}/friends".format(user_id))
        T=time.time()
        while 1:
            h1=self.browser.evaluate_script("document.body.scrollHeight")
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            h2=self.browser.evaluate_script("document.body.scrollHeight")
            if h1 != h2:
                T=time.time()
            elif time.time()-T>10:
                break
        #links=self.browser.find_link_by_partial_href("hc_location=friends_tab")
        links=self.browser.find_by_css(".fcb")
        friends=[]
        for link in links:
            name=link.value
            user_id_=link.find_by_tag("a")["href"].split("/")[-1].split("?")[0]
            friends.append((user_id_,name))
        tdict={}
        tdict["name"]=self.browser.find_by_id("fb-timeline-cover-name").value
        tdict["user_id"]=user_id
        tdict["friends"]=friends
        infos=self.browser.find_by_css("._3c_")
        mutual=0
        for info in infos:
            if info.value=="Mutual Friends":
                if info.find_by_css("._3d0").value:
                    tdict["n_mutual"]=info.find_by_css("._3d0").value
                    mutual=1
            if info.value=="All Friends":
                    tdict["n_friends"]=info.find_by_css("._3d0").value
        if mutual==0:
            links=self.browser.find_by_css("._gs6")
            if "Mutual" in links.value:
                tdict["n_mutual"]=links.value.split(" ")[0]
        if write:
            if not os.path.isdir("{}/fb_ids/".format(self._BASE_DIR)):
                os.mkdir("{}/fb_ids/".format(self._BASE_DIR))
            with open("{}fb_ids/{}.pickle".format(self._BASE_DIR,user_id),"wb") as f:
                pickle.dump(tdict,f)
        self.tdict=tdict
        return tdict

        




