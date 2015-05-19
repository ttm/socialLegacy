import twython as T, pickle, maccess

# Consumer Key (API Key)  iub8wm03f4sI4EMvxgdoicwIe
# Consumer Secret (API Secret)    wlMxqHGSKjrKjhTPhQtkdR9bUnK7sZyjgsUEEcxDlHqoJCHO4D

# Access Token    18882547-183eFHigoFCYlZDh4IUSkVtsF6WM0CbX6yvu0Ah3a
# Access Token Secret YrWWp3GNudB7rXgHaj6cokJyXM6SW3GUTmO1tqoIYv6Y9

twitter = T.Twython(app_key="iub8wm03f4sI4EMvxgdoicwIe",
                  app_secret="wlMxqHGSKjrKjhTPhQtkdR9bUnK7sZyjgsUEEcxDlHqoJCHO4D",
                  oauth_token="18882547-183eFHigoFCYlZDh4IUSkVtsF6WM0CbX6yvu0Ah3a", 
                  oauth_token_secret="YrWWp3GNudB7rXgHaj6cokJyXM6SW3GUTmO1tqoIYv6Y9")

#twitter=T.Twython(app_key= S.maccess.tw2.tak ,
#                  app_secret=         S.maccess.tw2.taks,
#                  oauth_token=        S.maccess.tw2.tat ,
#                  oauth_token_secret= S.maccess.tw2.tats)
#search = twitter.search_gen('#g1')
search = twitter.search_gen('#prayforthephilippines')
rr=[]
for result in search:
    rr.append(result)

f=open("pickleDir/tweetsHASHg1.pickle","wb")
pickle.dump(rr,f,-1)
f.close()

ff=open("pickleDir/tweetsPython.pickle","rb")
tt1=pickle.load(ff)
ff.close()

