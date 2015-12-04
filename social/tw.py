import pickle, datetime, os, shutil
import percolation as P
from twython import Twython
from twython import TwythonStreamer

import parsedatetime as pdt
parser=pdt.Calendar()
from dateutil.parser import parse
from maccess import tw2 as tw
c=P.utils.check

def publishSearch(fname,fpath,aname=None,scriptpath=None,created_at=None,tweets_info="a hashtag or a topic (probably)",donated_by="labMacambira.sf.net",latin=False,utf8_fix=True,acquired_through="Twitter search engine"):
    if not aname:
        print(fname,aname)
        aname=fname.split("/")[-1].split(".")[0]
        if not aname.endswith("_tw"):
            aname+="_tw"

    tg2=P.rdf.makeBasicGraph([["po","tw"],[P.rdf.ns.po,P.rdf.ns.tw]],"Metadata for the snapshot of Twitter messages")
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
                           "https://raw.githubusercontent.com/ttm/{}/master/base/".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           acquired_through,
                                "The Twitter messages related to {}".format(tweets_info),
                           ])

    tweets=[]
    try:
        tweets+=P.utils.pRead2( fname)[0]
    except:
        c("nao tem " +fname)
    #try:
    #    tweets+=P.utils.pRead2(fname.replace(".pickle","_.pickle"))
    #except:
    #    c("nao tem " +fname.replace(".pickle","_.pickle"))
    fname__=fname.replace(".pickle","_.pickle")
    if os.path.isfile(fname__):
        tweets,fopen=P.utils.pRead3(fname__,tweets)
    #tweets=[i for j in tweets for i in j][:10000*30]
    #tweet_chuncks=[tweets[i:i+10000] for i in range(0,len(tweets),10000)]
    #tweets=[i for j in tweets for i in j][:270]
    #tweet_chuncks=[tweets[i:i+100] for i in range(0,len(tweets),100)]
#    tweet_chuncks=[tweets[i:i+100] for i in range(0,len(tweets),100)]
    ccount=0
    fpath_="{}/{}/".format(fpath,aname)
    nnicks=0
    nicks_=[]
    nreplies=0
    nretweets=0
    nmsgs=0
    dates1=[]
    dates2=[]
    #for chunck in tweet_chuncks:
    while tweets:
        c("chunck {}".format(ccount))
        tg=P.rdf.makeBasicGraph([["po","tw"],[P.rdf.ns.po,P.rdf.ns.tw]],"Twitter messages linked data, chuck {:05d}".format(ccount))
        for tweet in tweets:
            tid=tweet["id_str"]
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
            date=parse(tweet["created_at"])
            data+=[date]

            if tweet["in_reply_to_user_id"]:
                uris+=[P.rdf.ns.tw.inReplyToUID]
                data+=[tweet["in_reply_to_user_id"]]

            P.rdf.link([tg],imsg,msg,uris,data)

            if "retweeted_status" in tweet.keys():
                tid2=tweet["retweeted_status"]["id_str"]
                imsg2=P.rdf.IC([tg],P.rdf.ns.tw.Message,tid2)

                uris=[P.rdf.ns.tw.messageID]
                data=[tid2]

                uris+=[P.rdf.ns.tw.precedingMessageContent]
                data+=[tweet["retweeted_status"]["text"]]

                P.rdf.link([tg],imsg,msg,uris,data)

                sid2=tweet["retweeted_status"]["user"]["screen_name"]
                iuser2=P.rdf.IC([tg],P.rdf.ns.tw.Participant,sid2)

                uris=[P.rdf.ns.tw.sid]
                data=[sid2]

                uris+=[P.rdf.ns.tw.uid]
                data+=[tweet["retweeted_status"]["user"]["id_str"]]

                data+=[tweet["retweeted_status"]["user"]["name"]]
                uris+=[P.rdf.ns.tw.name]

                P.rdf.link([tg],iuser2,sid2,uris,data)

            sid=tweet["user"]["screen_name"]
            iuser=P.rdf.IC([tg],P.rdf.ns.tw.Participant,sid)

            uris=[P.rdf.ns.tw.sid]
            data=[sid]

            uris+=[P.rdf.ns.tw.uid]
            data+=[tweet["user"]["id_str"]]

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

            uris=[P.rdf.ns.tw.author]
            uris2=[iuser]
            if "retweeted_status" in tweet.keys():
                uris+=[P.rdf.ns.tw.retweetOf]
                uris2+=[imsg2]
            P.rdf.link_([tg],imsg,msg,uris,uris2)

            # linka msg com usuarios
            # e usuarios entre si?

            # achar a id da mensagem aa qual esta eh retweet ou resposta
            # fazer as uris corretamente para o user e o reply to
            # achar as hashtags e colocar jah

        P.rdf.writeAll(tg,aname+"Translate{:05d}".format(ccount),fpath_,False,False)
        if not os.path.isdir(fpath_+"base"):
            os.mkdir(fpath_+"base")
        P.utils.pDump(tweets,fpath_+"base/"+"{}{:04d}.pickle".format(aname,ccount))
        ccount+=1
        nnicks+=P.utils.countMe( tg[0],"tw:author")
        nicks = P.utils.getAll2(  tg[0],"tw:author")
        nicks_+=[i.split("#")[-1] for i in nicks]

        nreplies += P.utils.countMe(tg[0],"tw:inReplyToUID")
        nretweets+=P.utils.countMe(  tg[0],"tw:retweetOf")
        nmsgs    +=    P.utils.countMe(  tg[0], "tw:messageContent")
        dates=[i for i in tg[0].query(r"SELECT ?p WHERE {?s tw:sentAt ?p} ORDER BY ASC(?p)")]
        dates1+=[dates[0][0].value]
        dates2+=[dates[-1][0].value]
        tweets=[]
        if os.path.isfile(fname__):
            tweets,fopen=P.utils.pRead3(None,tweets,fopen)

    date1=min(dates1)
    date2=max(dates2)
    c("tudo em RDF")
    #tg_=[tg[0]+tg2[0],tg[1]]
    #fpath_="{}/{}/".format(fpath,aname)
    #P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)

    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")

#    shutil.copy(fname,fpath_+"base/")
    #i=0
    #for chunck in tweet_chuncks:
    #    P.utils.pDump(chunck,fpath_+"base/"+"{}{:04d}.pickle".format(aname,i))
    #    i+=1
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)

    # faz um README
    #dates=[i for i in tg_[0].query(r"SELECT ?p WHERE {?s tw:sentAt ?p} ORDER BY ASC(?p)")]
    #date1=dates[0][0].value
    #date2=dates[-1][0].value
    #return tg_
    #nicks=queryMe(tg_[0],"SELECT ?s ?o WHERE {?s irc:nick ?o}")

    #nnicks=P.utils.countMe( tg_[0],"tw:author")
    #nicks= P.utils.getAll2(  tg_[0],"tw:author")
    #nicks_=[i.split("#")[-1] for i in nicks]

    #nreplies= P.utils.countMe(tg_[0],"tw:inReplyToUID")
    #nretweets=P.utils.countMe(  tg_[0],"tw:retweetOf")
    #nmsgs=    P.utils.countMe(  tg_[0], "tw:messageContent")
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the Twitter messages about {}
collected around {}, with messages from {} to {} and {} users.
Total messages count {} of which {} are replies and {} are retweets
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from Twitter in data/\n
\nUsers: {}\n""".format(
            tweets_info,created_at,date1,date2,
            nnicks,nmsgs,nreplies,nretweets,nicks_))
    return tg, tweets


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
                self.app_key=           self.TWITTER_API_KEY
                self.app_secret=        self.TWITTER_API_KEY_SECRET
                self.oauth_token=       self.TWITTER_ACCESS_TOKEN
                self.oauth_token_secret=self.TWITTER_ACCESS_TOKEN_SECRET   
            else:
                self.app_key=           app_key
                self.app_secret=        app_secret
                self.oauth_token=       oauth_token
                self.oauth_token_secret=oauth_token_secret

    def streamTag(self,HTAG="#python",aname=None):
        if not aname:
            aname=HTAG[1:]+"_tw"
        stream=MyStreamer(self.app_key           ,
                          self.app_secret        ,
                          self.oauth_token       ,
                          self.oauth_token_secret)
        stream.putName(aname)
        self.stream=stream
        stream.statuses.filter(track=HTAG)
    def finishStream(self):
        self.stream.D.close()
    def searchTag(self,HTAG="#python"):
        """Set Twitter search or stream criteria for the selection of tweets"""
        self.t = Twython(app_key           =self.app_key           ,
                        app_secret         =self.app_secret        ,
                        oauth_token        =self.oauth_token       ,
                        oauth_token_secret =self.oauth_token_secret)

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

class MyStreamer(TwythonStreamer):
    C=[]
    i=1
    def putName(self,aname):
        fname="../data/tw/{}_.pickle".format(aname)
        #if os.path.isfile(fname):
        #    self.C=P.utils.pRead(fname)
        self.aname=aname
        self.fname=fname
        self.D=P.utils.Dumper(fname)
    def on_success(self, data):
        if 'text' in data:
            self.C.append(data)            
            print(data['text'])
        if self.i%100==0:
            self.D.dump(self.C)
            self.C=[]
        print(self.i); self.i+=1
    def on_error(self, status_code, data):
        print(status_code)

#print "iniciando streaming"
#stream=MyStreamer(tw.tak,tw.taks,tw.tat,tw.tats)
#stream.statuses.filter(track=HTAG)


