# read both pickle data that starts with the defined string
# write packs of < 50MB pickle data
# write triples in packs of < 50MB
import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.tw)
importlib.reload(P.utils)

ddir="../data/tw/"
#a=P.utils.pRead2(ddir+ "{}.pickle".format(sid))
#b=P.utils.pRead2(ddir+"{}_.pickle".format(sid))
#aa=a+b
#bb=[i for j in aa for i in j]
##cc=zip(*[iter(bb)]*3)
#cc=[bb[i:i+10000] for i in range(0,len(bb),10000)]
#i=0
#for chunck in cc:
#    P.utils.pDump(ddir2+"{}{:04d}".format(sid,i))
#    i+=1
scriptpath=os.path.realpath(__file__)
fpath="./publishing/tw/"
stags=[
"python",
"QuartaSemRacismoClubeSDV_tw",
"arenaNETmundial",
"SnapDetremura_tw",
"art_tw",
"game_tw",
"god_tw",
"music_tw",
"obama_tw",
"science_tw",
"porn_tw",
"ChennaiFloods_tw",
"SyriaVote_tw",
"MAMA2015_tw",
]
stags=["QuartaSemRacismoClubeSDV_tw",
"arenaNETmundial",
"SnapDetremura_tw",
"art_tw"]
umbrella_dir="twitter1/"
stags=[
"game_tw",
"god_tw",
"music_tw",
"obama_tw",
"science_tw",
"porn_tw",
]
umbrella_dir="twitter2/"
stags=[
"ChennaiFloods_tw",
"SyriaVote_tw",
]
umbrella_dir="twitter3/"

stags=[
"MAMA2015_tw",
]
umbrella_dir="twitter3/"

#fnames=[sid+".pickle","arenaNETmundial.pickle"]
fnames=[i+".pickle" for i in stags]
#descriptions=["tweets with the #QuertaSemRacismoClubeSDV hashtag","tweets with the #arenaNETmundial hashtag"]
descriptions=["tweets with the #{} hashtag".format(i) for i in stags]
for fname,desc in zip(fnames,descriptions):
    b=S.tw.publishSearch("../data/tw/{}".format(fname),fpath,
            None,scriptpath,datetime.date(2015, 12, 3),
            desc,umbrella_dir=umbrella_dir)

