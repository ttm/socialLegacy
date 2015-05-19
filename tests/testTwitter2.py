import twython as T, pickle, maccess

terms=["#python",
       "#g1",
       "#prayforthephilippines",
       "#felipao",
       "#ReadyForScorch",
       "#obama",
       "#dilma",
       "#science",
       "#god"]
twitters=[]
searchs=[]
for tw,term in zip(maccess.TW,terms):
    twitter=T.Twython(app_key=            tw.tak ,
                      app_secret=         tw.taks,
                      oauth_token=        tw.tat ,
                      oauth_token_secret= tw.tats)
    search = twitter.search_gen(term)
    twitters.append(twitter)
    searchs.append(search)


