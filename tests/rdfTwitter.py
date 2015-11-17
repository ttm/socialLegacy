import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.tw)
importlib.reload(P.rdf)
importlib.reload(P.utils)
c=P.utils.check

scriptpath=os.path.realpath(__file__)
fpath="./publishing/tw/"
fnames=["python.pickle",]
b=S.tw.publishSearch("../data/tw/{}".format(fnames[0]),fpath,
        None,scriptpath,datetime.date(2015, 10, 15),
        "tweets with the #python hashtag")
#
