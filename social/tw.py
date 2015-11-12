from maccess import tw2 as tw
from twython import Twython
class Twitter:
    """Simplified Twitter interface for Stability observance

    # function to set authentication: __init__()
    # function to set hashtag and other tweets selection criteria: searchTag()
    # function to search tweets: searchTag()
    # function to stream tweets: void
    """
    TWITTER_API_KEY             = tw.tak
    TWITTER_API_KEY_SECRET      = tw.taks
    TWITTER_ACCESS_TOKEN        = tw.tat
    TWITTER_ACCESS_TOKEN_SECRET = tw.tats
    def __init__(self,app_key=           None,
                      app_secret=        None,
                      oauth_token=       None,
                      oauth_token_secret=None,):
            """Start twitter seach and stream interface"""
            if not app_key:

                app_key=           self.TWITTER_API_KEY
                app_secret=        self.TWITTER_API_KEY_SECRET
                oauth_token=       self.TWITTER_ACCESS_TOKEN
                oauth_token_secret=self.TWITTER_ACCESS_TOKEN_SECRET   
            self.t = Twython(app_key           =app_key           ,
                            app_secret        =app_secret        ,
                            oauth_token       =oauth_token       ,
                            oauth_token_secret=oauth_token_secret)
    def searchTag(self,HTAG="#arenaNETmundial"):
        """Set Twitter search or stream criteria for the selection of tweets"""
        search =self.t.search(q=HTAG,count=100,result_type="recent")
        ss=search[:]
        search = self.t.search(q=HTAG,count=150,max_id=ss[-1]['id']-1,result_type="recent")
        #search = t.search(q=HTAG,count=150,since_id=ss[-1]['id'],result_type="recent")
        while seach:
            ss+=search[:]
            search = self.t.search(q=HTAG,count=150,max_id=ss[-1]['id']-1,result_type="recent")
        self.ss=ss
            #search = t.search(q=HTAG,count=150,since_id=ss[-1]['id'],result_type="recent")


    # function to set authentication: __init__()
    # function to set hashtag and other tweets selection criteria: searchTag()
    # function to search tweets: searchTag()
    # function to stream tweets: void
