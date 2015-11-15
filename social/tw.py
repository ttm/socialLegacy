import pickle, percolation as P
from twython import Twython
from maccess import tw2 as tw


def publishSearch(fname,fpath,aname=None,scriptpath=None,created_at=None,tweets_info="probably tweets with a hashtag or about a topic",donated_by="labMacambira.sf.net",latin=False,utf8_fix=True):
    tweets=P.utils.pRead(fname)
    for tweet in tweets:
        tid=tweet["id"]
        uid=tweet["user"]["screen_name"]
        imsg=P.rdf.IC([tg],P.rdf.ns.tw.Message,tid)


                text=tweet["text"]
        uris=[P.rdf.ns.tw.messageContent]
        data=[text]
        uris+=[P.rdf.ns.tw.retweetCount]
        data+=[tweet["retweet_count"]]

        uris+=[P.rdf.ns.tw.retweeted]
        data+=[tweet["retweeted"]]
        if "retweeted_status" in tweet.keys():
            tid2=tweet["retweeted_status"]["id"]
            imsg2=P.rdf.IC([tg],P.rdf.ns.tw.Message,tid2)
            data+=[tid]
            uris+=[P.rdf.ns.tw.messageID]
            data+=[tweet["retweeted_status"]["text"]]
            uris+=[P.rdf.ns.tw.messageContent]

            uid2=tweet["retweeted_status"]["user"]["id"]
            iuser=P.rdf.IC([tg],P.rdf.ns.tw.Participant,uid2)
            data+=[tweet["retweeted_status"]["user"]["screen_name"]
            uris+=[P.rdf.ns.tw.sid]
            data+=[uid2]
            uris+=[P.rdf.ns.tw.uid]
            data+=[tweet["retweeted_status"]["user"]["name"]]
            uris+=[P.rdf.ns.tw.name]

        uris+=[P.rdf.ns.tw.lang]
        data+=[tweet["lang"]]

        if tweet["in_reply_to_user_id"]:
            data+=[tweet["in_reply_to_user_id"]] #
            uris+=[P.rdf.ns.tw.inReplyTo]

        iuser=P.rdf.IC([tg],P.rdf.ns.tw.Participant,uid)
        data+=[uid]
        uris+=[P.rdf.ns.tw.screenName]
        if tweet["user"]["location"]:
            data+=[tweet["user"]["location"]]
            uris+=[P.rdf.ns.tw.uLocation]
        data+=[tweet["user"]["favourites_count"]]
        uris+=[P.rdf.ns.tw.favouritesCount]
        data+=[tweet["user"]["followers_count"]]
        uris+=[P.rdf.ns.tw.followersCount]
        data+=[tweet["user"]["friends_count"]]
        uris+=[P.rdf.ns.tw.friendsCount]
        data+=[tweet["user"]["utc_offset"]]
        uris+=[P.rdf.ns.tw.utcOffset]

        # achar a id da mensagem aa qual esta eh retweet ou resposta
        # fazer as uris corretamente para o user e o reply to
        # achar as hashtags e colocar jah

    return tweets,len(tweets)

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
