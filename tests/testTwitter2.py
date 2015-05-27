import twython as T, maccess, time, pickle
import multiprocessing as mp

terms=["#jesus",
       "#g1",
       "#prayforthephilippines",
       "#felipao",
       "#ReadyForScorch",
       "#obama",
       "#dilma",
       "#science",
       "#god"]
fnames=["pickleDir/{}".format(term.replace("#","HASH")+".pickle") for term in terms]
twitters=[]
searchs=[]
for tw,term in zip(maccess.TW,terms):
    twitter=T.Twython(app_key=            tw.tak ,
                      app_secret=         tw.taks,
                      oauth_token=        tw.tat ,
                      oauth_token_secret= tw.tats)
    search= twitter.cursor(twitter.search, q=term)
    #search = twitter.search_gen(term)
    twitters.append(twitter)
    searchs.append(search)

def rodaSearch(search,fname,output,rr=None):
    if not rr:
        rr=[]
    for result in zip(list(range(2500)),search):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname, len(rr))
    time.sleep(15*63)
    #output.put(rr)
    print("AWAKE "+fname,len(rr))
    rodaSearch(search,fname,output,rr)
    #f=open(fname,"wb")
    #rrr=rr[:]
    #pickle.dump(rrr,f,-1)
    #f.close()
    output.put(rr)

#pool=mp.Pool(processes=9)
#results__=[pool.apply_async(rodaSearch,args=(search,fname)) for search,fname in zip(searchs,fnames)]
output=mp.Queue()
processes=[mp.Process(target=rodaSearch,args=(search,fname,output)) for search,fname in zip(searchs,fnames)]


#output=[p.get() for p in results__]
for p in processes:
    p.start()
#for p in processes:
#    p.join()
#results=[output.get() for p in processes]
#print(results)


"""
def rodaSearch(search,fname,output,rr=None):
    if not rr:
        rr=[]
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)
    for result in zip(search,list(range(2500))):
        print("result "+fname)
        rr.append(result)
    f=open(fname,"wb")
    rrr=rr[:]
    pickle.dump(rrr,f,-1)
    f.close()
    print("SLEEP "+fname)
    time.sleep(15*62)
    print("AWAKE "+fname)








"""
