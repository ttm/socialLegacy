import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.irc)
importlib.reload(P.rdf)
c=P.utils.check

scriptpath=os.path.realpath(__file__)
fpath="./publishing/irc/"
#a=S.irc.publishLog("../data/irc/labmacambira_lalenia2.txt",fpath,"labMacambiraLaleniaLog2",scriptpath,datetime.date(2013, 10, 15),latin=True)
#b=S.irc.publishLog("../data/irc/labmacambira_lalenia3.txt",fpath,"labMacambiraLaleniaLog3",scriptpath,datetime.date(2015, 9, 15) ,latin=True)

#fnames="labmacambira_lalenia2.txt","labmacambira_lalenia3.txt","#foradoeixo.log","#hackerspace-cps.log","#hackerspaces-br.log","#matehackers.log"
fnames=["labmacambira_lalenia2.txt",]
fnames=["labmacambira_lalenia3.txt",]
fnames+=["#foradoeixo.log","#hackerspace-cps.log","#hackerspaces-br.log","#matehackers.log"]
for fname in fnames:
    if "#" in fname:
        fname_=fname[1:-4]
    else:
        if "2" in fname:
            fname_="labMacambiraLaleniaLog2"
        else:
            fname_="labMacambiraLaleniaLog3"
    b=S.irc.publishLog("../data/irc/{}".format(fname),fpath,fname_,scriptpath,datetime.date(2015, 10, 15), "the {} IRC channel log".format(fname), latin=True)
    c("finished " + fname)
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




