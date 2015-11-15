import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.irc)
importlib.reload(P.rdf)
c=P.utils.check

scriptpath=os.path.realpath(__file__)
fpath="./publishing/irc/"
a=S.irc.publishLog("../data/irc/labmacambira_lalenia2.txt",fpath,"labMacambiraLaleniaLog2",scriptpath,datetime.date(2013, 10, 15),latin=True)
b=S.irc.publishLog("../data/irc/labmacambira_lalenia3.txt",fpath,"labMacambiraLaleniaLog3",scriptpath,datetime.date(2015, 9, 15) ,latin=True)

# set(re.findall("\<[a-zA-Z0-9_\-\<\]\[\\\^\{\}]*\>",b))
# cria rdf com usuarios, mensagens, horarios das mensagens
# horarios das entradas e saídas
# adicionar triplas sobre os usuários sobre:
# ==> se é bot
# ==> se não é bot
# ==> id no /fb
# ==> alias de nick de usuario




