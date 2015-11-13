import social as S, percolation as P, os
import  importlib
importlib.reload(S.fb)
importlib.reload(P.rdf)
#fnames=("../data/Antonio.gdf",thata,ricardo,marilia,debora,rita,massimo,vilson,penalva,grupos)
fnames="AntonioAnzoategui18022013huge_100003608428288_2013_02_18_21_34_f74ca978ec921548c0b7caf3287f2335.gml","RonaldCosta12062013.gml"
tdir="../data/fb/gml/"
fnames=[tdir+i for i in fnames]
sids="antonio.anzoateguifabbri" , "scherolt" # ids do fb do Antonio e do Ronald
uids="100003608428288" , "1457302032" # ids do fb do Antonio e do Ronald
#fpath="/home/r/repos/linkedRFabbri/"
fpath="./publishing/fb/"
scriptpath=os.path.realpath(__file__)
# idealmente todos os arquivos gdf e gml no data/fb/
for fname,uid,sid in zip(fnames,uids,sids):
    S.fb.triplifyGML(fname,fpath,scriptpath,uid,sid)



