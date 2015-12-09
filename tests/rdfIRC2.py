import social as S, percolation as P, os, re, sys
import  importlib, datetime
importlib.reload(S.irc)
importlib.reload(P.rdf)
c=P.utils.check

scriptpath=os.path.realpath(__file__)
fpath="./publishing/irc/"
#a=S.irc.publishLog("../data/irc/labmacambira_lalenia2.txt",fpath,"labMacambiraLaleniaLog2",scriptpath,datetime.date(2013, 10, 15),latin=True)
#b=S.irc.publishLog("../data/irc/labmacambira_lalenia3.txt",fpath,"labMacambiraLaleniaLog3",scriptpath,datetime.date(2015, 9, 15) ,latin=True)

#fnames="labmacambira_lalenia2.txt","labmacambira_lalenia3.txt","#foradoeixo.log","#hackerspace-cps.log","#hackerspaces-br.log","#matehackers.log"
#fnames=["labmacambira_lalenia2.txt",]
##fnames=["labmacambira_lalenia3.txt",]
#fnames=["#foradoeixo.log","#hackerspace-cps.log","#hackerspaces-br.log","#matehackers.log"]
fdirs="#wikimedia-dev","#wikimedia-wikidata","#mediawiki",
dpath="../data/irc/"
for fdir in fdirs: print(os.path.isdir(dpath+fdir))
for fdir in fdirs:
    b=S.irc.publishLog2("../data/irc/{}".format(fdir),fpath,None,scriptpath,datetime.datetime.now(), "the {} IRC channel log".format(fdir), latin=False,c8859=True)
    c("finished " + fdir)
#b=S.irc.publishLog("../data/irc/labmacambira_lalenia3.txt",fpath,"labMacambiraLaleniaLog3",scriptpath,datetime.date(2015, 10, 15) ,latin=True)
#b=S.irc.publishLog("../data/irc/labmacambira_lalenia3.txt",fpath,"labMacambiraLaleniaLog3",scriptpath,datetime.date(2015, 10, 15) ,latin=True)
# set(re.findall("\<[a-zA-Z0-9_\-\<\]\[\\\^\{\}]*\>",b))
# cria rdf com usuarios, mensagens, horarios das mensagens
# horarios das entradas e saídas
# adicionar triplas sobre os usuários sobre:
# ==> se é bot
# ==> se não é bot
# ==> id no /fb
# ==> alias de nick de usuario




