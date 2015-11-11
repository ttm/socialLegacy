from maccess import tw2 as tw
TWITTER_API_KEY             = tw.tak
TWITTER_API_KEY_SECRET      = tw.taks
TWITTER_ACCESS_TOKEN        = tw.tat
TWITTER_ACCESS_TOKEN_SECRET = tw.tats

class Twitter:
    """Simplified Twitter interface for Stability observance

    # function to set authentication: __init__()
    # function to set hashtag and other tweets selection criteria: searchTag()
    # function to search tweets: searchTag()
    # function to stream tweets: void
    """
    def __init__(self,app_key=TWITTER_API_KEY, 
                      app_secret=TWITTER_API_KEY_SECRET, 
                      oauth_token=TWITTER_ACCESS_TOKEN, 
                      oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET):
        """Start twitter seach and stream interface"""
        self.t = Twython(app_key           =app_key           ,
                    app_secret        =app_secret        ,
                    oauth_token       =oauth_token       ,
                    oauth_token_secret=oauth_token_secret)
    def searchTag(self,HTAG="#arenaNETmundial"):
        """Set Twitter search or stream criteria for the selection of tweets"""
        search = t.search(q=HTAG,count=100,result_type="recent")
        ss=search[:]
        search = t.search(q=HTAG,count=150,max_id=ss[-1]['id']-1,result_type="recent")
        #search = t.search(q=HTAG,count=150,since_id=ss[-1]['id'],result_type="recent")
        while seach:
            ss+=search[:]
            search = t.search(q=HTAG,count=150,max_id=ss[-1]['id']-1,result_type="recent")
            #search = t.search(q=HTAG,count=150,since_id=ss[-1]['id'],result_type="recent")


    # function to set authentication: __init__()
    # function to set hashtag and other tweets selection criteria: searchTag()
    # function to search tweets: searchTag()
    # function to stream tweets: void
