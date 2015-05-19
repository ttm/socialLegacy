import twython as T, pickle, maccess

# Consumer Key (API Key)  iub8wm03f4sI4EMvxgdoicwIe
# Consumer Secret (API Secret)    wlMxqHGSKjrKjhTPhQtkdR9bUnK7sZyjgsUEEcxDlHqoJCHO4D

# Access Token    18882547-183eFHigoFCYlZDh4IUSkVtsF6WM0CbX6yvu0Ah3a
# Access Token Secret YrWWp3GNudB7rXgHaj6cokJyXM6SW3GUTmO1tqoIYv6Y9

#twitter = T.Twython(app_key="iub8wm03f4sI4EMvxgdoicwIe",
#                  app_secret="wlMxqHGSKjrKjhTPhQtkdR9bUnK7sZyjgsUEEcxDlHqoJCHO4D",
#                  oauth_token="18882547-183eFHigoFCYlZDh4IUSkVtsF6WM0CbX6yvu0Ah3a", 
#                  oauth_token_secret="YrWWp3GNudB7rXgHaj6cokJyXM6SW3GUTmO1tqoIYv6Y9")
#
#twitter=T.Twython(app_key=            maccess.tw4.tak ,
#                  app_secret=         maccess.tw4.taks,
#                  oauth_token=        maccess.tw4.tat ,
#                  oauth_token_secret= maccess.tw4.tats)
#search = twitter.search_gen('#g1')
#search = twitter.search_gen('#python')
#search = twitter.search_gen('#prayforthephilippines')
#search = twitter.search_gen('felipao')
#search = twitter.search_gen('#ReadyForScorch')
#search = twitter.search_gen('#obama')
#search = twitter.search_gen('#dilma')
#search = twitter.search_gen('#science')
#rr=[]
#for result in search:
#    rr.append(result)

#f=open("pickleDir/tweetsHASHdilma.pickle","wb")
#pickle.dump(rr,f,-1)
#f.close()

ff=open("pickleDir/tweetsPython.pickle","rb")
tt1=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHg1.pickle","rb")
tt2=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHprayforthephilippines.pickle","rb")
tt3=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsFelipao.pickle","rb")
tt4=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHReadyForScorch.pickle","rb")
tt5=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHobama.pickle","rb")
tt6=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHdilma.pickle","rb")
tt7=pickle.load(ff)
ff.close()

ff=open("pickleDir/tweetsHASHscience.pickle","rb")
tt8=pickle.load(ff)
ff.close()

tt=[tt1,tt2,tt3,tt4,tt5,tt6,tt7,tt8]

# make retweet network
import networkx as x
edges=[]
GG=[]
for ttt in tt:
    G=x.DiGraph()
    for tweet in ttt:
        text=tweet["text"]
        if text.startswith("RT @"):
            us=tweet["user"]["screen_name"]
            prev_us=text.split(":")[0].split("@")[1]
            print(us,prev_us,text)
            edges.append((prev_us,us))
            if G.has_edge(prev_us,us):
                G[prev_us][us]["weight"]+=1
            else:
                G.add_edge(prev_us, us, weight=1.)
    GG.append(G)


# whenever a tweet is a Retweet, add egde from
# original sender to current retweeter
# if edge exists: add one to weight
# make network with and without disconnected vertices

