import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.tw)
importlib.reload(P.rdf)
importlib.reload(P.utils)
c=P.utils.check

scriptpath=os.path.realpath(__file__)
fpath="./publishing/tw/"
fnames=["python.pickle","arenaNETmundial.pickle"]
descriptions=["tweets with the #python hashtag","tweets with the #arenaNETmundial hashtag"]
for fname,desc in zip(fnames,descriptions):
    b=S.tw.publishSearch("../data/tw/{}".format(fname),fpath,
            None,scriptpath,datetime.date(2015, 10, 15),
            desc)
#
