import social as S, percolation as P, os, re
import  importlib, datetime
importlib.reload(S.tw)
importlib.reload(P.utils)
import maccess
c=P.utils.check
ttag,tid="#SyriaVote",1
ttag,tid="#art",6
ttag,tid="#porn",4
ttag,tid="#ChennaiFloods",3
ttag,tid="#QuartaSemRacismoClubeSDV",0
ttag,tid="#SnapDetremura",8
#ttag,tid="#physics",2 #pouco fluxo
ttag,tid="#music",2 #pouco fluxo
ttag,tid="#obama",5
ttag,tid="#god",7
ttag,tid="#game",3
ttag,tid="#science",6
# deixar algumas tags com pouco fluxo puxando por dias
# fuck physics shit brasil dilma europe africa etc.

tws=S.tw.Twitter(*P.utils.cred(maccess.TW[tid]))
#tws.streamTag(ttag)
# dont forguet to tws.finishStream() afterwards
# load with P.utils.pRead2("../data/tw/{}_tw_.pickle".format(ttag[1:]))
# will hava a list of 100 tweets per element
while 1:
    try:
        tws.streamTag(ttag)
    except:
        c("erro")
#try:
#    tws.streamTag(ttag)
#except:
#    c("erro")
#    try:
#        tws.streamTag(ttag)
#    except:
#        c("erro")
#        try:
#            tws.streamTag(ttag)
#        except:
#            c("erro")
#            try:
#                tws.streamTag(ttag)
#            except:
#                c("erro")
#                tws.streamTag(ttag) # erros ao todo pode dar de decodificacao

