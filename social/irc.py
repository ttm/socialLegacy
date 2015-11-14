import time, os, pickle, shutil, datetime, re, random
#import networkx as x
import rdflib as r
from urllib.parse import quote
import percolation as P
c=P.utils.check
def Q(string):
    return quote(string).replace("%","")
def B(abool):
   if abool:
       a=asdjkl

def publishLog(fname,fpath,aname=None,scriptpath=None,created_at=None,channel_info="channel #labmarambira at Freenode",donated_by="labMacambira.sf.net",latin=False):
    if not aname:
        name=aname=fname.split(".")[0]
    if not created_at:
        created_at=datetime.datetime.now()
    tg=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"My facebook ego friendship network")
    tg2=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"RDF metadata for the facebook friendship network of my son")
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))
    P.rdf.link([tg2],ind,"Snapshot {}".format(aname),
                          [P.rdf.ns.po.createdAt,
                          P.rdf.ns.po.triplifiedIn,
                          P.rdf.ns.po.donatedBy,
                          P.rdf.ns.po.availableAt,
                          P.rdf.ns.po.originalFile,
                          P.rdf.ns.po.rdfFile,
                          P.rdf.ns.po.ttlFile,
                          P.rdf.ns.po.discorveryRDFFile,
                          P.rdf.ns.po.discoveryTTLFile,
                          P.rdf.ns.po.acquiredThrough,
                          P.rdf.ns.rdfs.comment,
                          ],
                          [created_at,
                           datetime.datetime.now(),
                           donated_by,
                           "https://github.com/ttm/".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")[-1]),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Lalenia supybot",
                                "The IRC log of {}".format(channel_info),
                           ])

    with open(fname,"rb") as f:
        t_=f.read()
    if latin:
        t=t_.decode("latin-1")
    else:
        t=t_.decode("utf-8",errors="ignore")
    # get users, messages, times
    d={}
    exp=r"(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2})  \<(.*?)\> (.*)"
    # ver se estamos jogando algo fora TTM
    count=1
    timestamps=set()
    for match in re.findall(exp,t, re.U):
        year, month, day, hour, minute, second, nick, msg=match
        nick=Q(nick)
        # achar direct message com virgula! TTM
        directed_to=re.findall(r"(^[^\s:]+):",msg)
        if directed_to:
            nick2=Q(directed_to[0])
            msg_=re.findall(r"^[^\s]*:\s*(.*)",msg)[0]

        # cria indivíduos: mensagem e usuarios para os nicks
        ind=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick))
        #if "discutir se a prioridade" in msg:
        #    wer=asd
        uris=[P.rdf.ns.irc.nick]
        data=[nick]
        P.rdf.link([tg],ind,nick,uris,data)
        # usuario se conecta com o nick (strings)
        #P.rdf.link([tg],ind,nick,uris,data)
        if directed_to:
            ind2=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick2))
            data=[nick2]
            P.rdf.link([tg],ind2,nick2,uris,data)

        # mensagem se conecta com usuarios (URIS) e textos (strings)
        dt=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute,second)])
        timestamp=dt.isoformat()
        while timestamp in timestamps:
            timestamp+='_r_%05x' % random.randrange(16**5)
        timestamps.update(timestamp)
        imsg=P.rdf.IC([tg],P.rdf.ns.irc.Message,"{}-{}".format(aname,timestamp))
        if msg:
            uris=[P.rdf.ns.irc.messageContent]
            data=[msg]
            if directed_to:
                uris+=[P.rdf.ns.irc.cleanedMessage]
                data+=[msg_]
        else:
            uris=[P.rdf.ns.irc.empty]
            data=[True]
            msg="EMPTYMSG"
        uris+=[P.rdf.ns.irc.sentAt]
        data+=[dt]
        P.rdf.link([tg],imsg,msg,uris,data)
            # adiciona tripla da msg para empty message true

        uris=[P.rdf.ns.irc.author]
        uris2=[ind]
        if directed_to:
            uris+=[P.rdf.ns.irc.directedTo]
            uris2+=[ind2]
        P.rdf.link_([tg],imsg,msg,uris,uris2)

        if (1+count)%1000==0:
            c("check 1000")
        count+=1
    c("tudo em RDF")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}/{}/".format(fpath,aname)
#    return fpath_, tg_,exp,t,t_
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)
    # copia o script que gera este codigo
    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    #shutil.copy(this_dir+"/../tests/rdfMyFNetwork2.py",fpath+"scripts/")
    shutil.copy(scriptpath,fpath_+"scripts/")
    # copia do base data
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copy(fname,fpath_+"base/")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)
    # faz um README
    date1=0
    date2=0
    nnicks=0
    ndnicks=0
    ndirect=0
    nmsgs=0
    nops=0
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the IRC Network {} collected around {}, with messages from {} to {}.
It has {} nicks (~{} different) with {} directed messages.
Total messages count {}
of which {} are operational.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from lalenia (a Supybot) in data/\n""".format(
            channel_info,created_at,date1,date2,
            nnicks,ndnicks,ndirect,nmsgs,nops))


    return t
