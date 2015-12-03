# read both pickle data that starts with the defined string
# write packs of < 50MB pickle data
# write triples in packs of < 50MB
import percolation as P

ddir="../data/tw/"
sid="QuartaSemRacismoClubeSDV_tw"
a=P.utils.pRead2(ddir+ "{}.pickle".format(sid))
b=P.utils.pRead2(ddir+"{}_.pickle".format(sid))
aa=a+b
bb=[i for j in aa for i in j]
#cc=zip(*[iter(bb)]*3)
cc=[bb[i:i+10000] for i in range(0,len(bb),10000)]
i=0
for chunck in cc:
    P.utils.pDump(ddir2+"{}{:04d}".format(sid,i))
    i+=1
