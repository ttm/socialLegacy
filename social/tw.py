import pickle, datetime, os, shutil
import percolation as P
from twython import Twython
from maccess import tw2 as tw
c=P.utils.check


def publishSearch(fname,fpath,aname=None,scriptpath=None,created_at=None,tweets_info="a hashtag or a topic (probably)",donated_by="labMacambira.sf.net",latin=False,utf8_fix=True,acquired_through="Twitter search engine"):
    if not aname:
        print(fname,aname)
        aname=fname.split("/")[-1].split(".")[0]
    tg=P.rdf.makeBasicGraph([["po","tw"],[P.rdf.ns.po,P.rdf.ns.tw]],"Twitter messages linked data")
    tg2=P.rdf.makeBasicGraph([["po","tw"],[P.rdf.ns.po,P.rdf.ns.irc]],"Metadata for the snapshot of Twitter messages")
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))
    P.rdf.link([tg2],ind,"Snapshot {}".format(aname),
                          [P.rdf.ns.po.createdAt,
                          P.rdf.ns.po.triplifiedIn,
                          P.rdf.ns.po.donatedBy,
                          P.rdf.ns.po.availableAt,
                          P.rdf.ns.po.originalFile,
                          P.rdf.ns.po.rdfFile,
                          P.rdf.ns.po.ttlFile,
                          P.rdf.ns.po.discorveryRDFFile,
                          P.rdf.ns.po.discoveryTTLFile,
                          P.rdf.ns.po.acquiredThrough,
                          P.rdf.ns.rdfs.comment,
                          ],
                          [created_at,
                           datetime.datetime.now(),
                           donated_by,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")[-1]),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           acquired_through,
                                "The Twitter messages related to {}".format(tweets_info),
                           ])


    tweets=P.utils.pRead(fname)
    for tweet in tweets:
        tid=tweet["id"]
        imsg=P.rdf.IC([tg],P.rdf.ns.tw.Message,tid)

        uris=[P.rdf.ns.tw.messageID]
        data=[tid]

        msg=tweet["text"]
        uris+=[P.rdf.ns.tw.messageContent]
        data+=[msg]

        uris+=[P.rdf.ns.tw.retweetCount]
        data+=[tweet["retweet_count"]]

        uris+=[P.rdf.ns.tw.lang]
        data+=[tweet["lang"]]

        uris+=[P.rdf.ns.tw.sentAt]
        data+=[tweet["created_at"]]

        if tweet["in_reply_to_user_id"]:
            uris+=[P.rdf.ns.tw.inReplyToUID]
            data+=[tweet["in_reply_to_user_id"]]

        P.rdf.link([tg],imsg,msg,uris,data)

        if "retweeted_status" in tweet.keys():
            tid2=tweet["retweeted_status"]["id"]
            imsg2=P.rdf.IC([tg],P.rdf.ns.tw.Message,tid2)

            uris=[P.rdf.ns.tw.messageID]
            data=[tid2]

            uris+=[P.rdf.ns.tw.messageContent]
            data+=[tweet["retweeted_status"]["text"]]

            P.rdf.link([tg],imsg,msg,uris,data)

            sid2=tweet["retweeted_status"]["user"]["screen_name"]
            iuser2=P.rdf.IC([tg],P.rdf.ns.tw.Participant,sid2)

            uris=[P.rdf.ns.tw.sid]
            data=[sid2]

            uris+=[P.rdf.ns.tw.uid]
            data+=[tweet["retweeted_status"]["user"]["id"]]

            data+=[tweet["retweeted_status"]["user"]["name"]]
            uris+=[P.rdf.ns.tw.name]

            P.rdf.link([tg],iuser2,sid2,uris,data)

        sid=tweet["user"]["screen_name"]
        iuser=P.rdf.IC([tg],P.rdf.ns.tw.Participant,sid)

        uris=[P.rdf.ns.tw.sid]
        data=[sid]

        uris+=[P.rdf.ns.tw.uid]
        data+=[tweet["user"]["id"]]

        if tweet["user"]["location"]:
            uris+=[P.rdf.ns.tw.uLocation]
            data+=[tweet["user"]["location"]]

        data+=[tweet["user"]["favourites_count"]]
        uris+=[P.rdf.ns.tw.favouritesCount]
        data+=[tweet["user"]["followers_count"]]
        uris+=[P.rdf.ns.tw.followersCount]
        data+=[tweet["user"]["friends_count"]]
        uris+=[P.rdf.ns.tw.friendsCount]
        data+=[tweet["user"]["utc_offset"]]
        uris+=[P.rdf.ns.tw.utcOffset]
        P.rdf.link([tg],iuser,sid,uris,data)

        uris2=[P.rdf.ns.tw.author]
        data=[iuser]
        if "retweeted_status" in tweet.keys():
            uris+=[P.rdf.ns.tw.retweetOf]
            uris2+=[imsg2]
        P.rdf.link_([tg],imsg,msg,uris,uris2)

        # linka msg com usuarios
        # e usuarios entre si?

        # achar a id da mensagem aa qual esta eh retweet ou resposta
        # fazer as uris corretamente para o user e o reply to
        # achar as hashtags e colocar jah

    c("tudo em RDF")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}/{}/".format(fpath,aname)
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)

    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copy(fname,fpath_+"base/")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)

    # faz um README
    dates=[i for i in tg_[0].query(r"SELECT ?p WHERE {?s tw:sentAt ?p} ORDER BY ASC(?p)")]
    date1=dates[0][0].value
    date2=dates[1][0].value
    #return tg_
    #nicks=queryMe(tg_[0],"SELECT ?s ?o WHERE {?s irc:nick ?o}")

    nnicks=P.utils.countMe(tg_[0],"tw:author")
    nicks= P.utils.getAll(  tg_[0],"tw:author")

    nreplies= P.utils.countMe(tg_[0],"tw:replyTo")
    nretweets=P.utils.countMe(  tg_[0],"tw:retweetOf")
    nmsgs=    P.utils.countMe(  tg_[0], "tw:messageContent","true")
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the Twitter messages about {}
collected around {}, with messages from {} to {} and {} users.
Total messages count {} of which {} replies and {} retweets
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from lalenia (a Supybot) in data/\n
\nNICKS: {}\n""".format(
            tweets_info,created_at,date1,date2,
            nnicks,nmsgs,nreplies,nretweets,nicks))
    return tg_


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
