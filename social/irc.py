import time, os, pickle, shutil, datetime, re, random, string, codecs
#import networkx as x
import nltk as k
import rdflib as r
from urllib.parse import quote
import percolation as P
c=P.utils.check
Tbreak=0
def Q(string):
    return quote(string).replace("%","")
def queryMe(ggraph,query):
    ii=ggraph.query(query)
    return [i for i in ii]
def countMe(ggraph,uri,o="?o"):
    query=r"SELECT (COUNT(?o) as ?count) WHERE {{   ?s {} {}}}".format(uri,o)
    return [i for i in ggraph.query(query)][0][0].value
def getAll(ggraph,uri):
    query="SELECT ?o WHERE {{?s {} ?o}}".format(uri)
    return list(set([i[0].value for i in ggraph.query(query)]))

def B(abool):
   if abool:
       a=asdjkl
def detectEquivalent(strings):
    #ss=[s.replace("_","") for s in strings]
    ss=strings
    dists=[]
    eqs=[]
    count=0
    for s1 in ss:
        dists.append([])
        for s2 in ss[1+count:]:
            dist=k.metrics.edit_distance(*[i.replace("_","") for i in (s1,s2)])
            dists[-1].append(dist)
            if dist<=2:
                eqs.append((s1,s2))
        count+=1
    return eqs
#k.metrics.edit_distance("bebeaaa","brbaaaa")
#"Ã³" é ó
# Ã£ é ã
# Ã© é é
#.replace("Ã¡","á").replace(Ã©,é).replace(Ã£,ã).replace(Ã³,ó).replace(Ã§,ç).replace()
# 
strange="Ã¡","Ã ","Ã¢","Ã£","Ã¤","Ã©","Ã¨","Ãª","Ã«","Ã­","Ã¬","Ã®","Ã¯","Ã³","Ã²","Ã´","Ãµ","Ã¶","Ãº","Ã¹","Ã»","Ã¼","Ã§","Ã","Ã€","Ã‚","Ãƒ","Ã„","Ã‰","Ãˆ","ÃŠ","Ã‹","Ã","ÃŒ","ÃŽ","Ã","Ã“","Ã’","Ã”","Ã•","Ã–","Ãš","Ã™","Ã›","Ãœ","Ã‡","Ã"
correct="á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö", "ú", "ù", "û", "ü", "ç", "Á", "À", "Â", "Ã", "Ä", "É", "È", "Ê", "Ë", "Í", "Ì", "Î", "Ï", "Ó", "Ò", "Ô", "Õ", "Ö", "Ú", "Ù", "Û", "Ü", "Ç","Ú"
def utf8Fix(string):
    # https://berseck.wordpress.com/2010/09/28/transformar-utf-8-para-acentos-iso-com-php/
    for st, co in zip(strange,correct):
        string=string.replace(st,co)
    return string

def publishLog2(fdir,fpath,aname=None,scriptpath=None,created_at=None,channel_info="channel #labmarambira at Freenode",donated_by="labMacambira.sf.net",latin=False,utf8_fix=True,c8859=True):
    if not aname:
        name=aname=fdir.split("#")[-1]
    if not created_at:
        created_at=datetime.datetime.now()
    tg=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"IRC log linked data")
    tg2=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"RDF metadata IRC log")
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
                          P.rdf.ns.po.discoveryRDFFile,
                          P.rdf.ns.po.discoveryTTLFile,
                          P.rdf.ns.po.acquiredThrough,
                          P.rdf.ns.rdfs.comment,
                          ],
                          [created_at,
                           datetime.datetime.now(),
                           donated_by,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fdir.split("#")[-1]),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Lalenia supybot",
                                "The IRC log of {}".format(channel_info),
                           ])

#    with open(fname,"rb") as f:
#        t_=f.read()
#    if latin:
#        t=t_.decode("latin-1")
#    else:
#        t=t_.decode("utf-8",errors="ignore")
#    if utf8_fix:
#        t=utf8Fix(t)
    # get users, messages, times
    # ver se estamos jogando algo fora TTM
    count=1
    timestamps=set()
    mids=set()
    #for match in re.findall(exp,t):

    exp0=r"(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2})  \*\*\* (\S+) (.*)"
    # lista arquivos no dir
    arqs=os.listdir(fdir)
    # em cada arquivo, pega a data do nome, os horarios e as msgs do conteúdo
    exp1=r"(\d{4})(\d{2})(\d{2})" # date
    exp1_=r"(\d{4})(\d{2})" # date without day
    ex=r"\[(\d{2}):(\d{2}):(\d{2})\] \<(.*?)\>[ ]*(.*)" # message
    ex_=r"\[(\d{2}):(\d{2}):(\d{2})\] \* ([^ ?]*)[ ]*(.*)"
    nicks=[]
    for arq in arqs:
        date=arq.split(".")[0]
        if len(date)==8:
            year,month,day=re.findall(exp1,date)[0]
        elif len(date)==6:
            year,month=re.findall(exp1_,date)[0]
        else:
            raise ValueError("date string from filename have a different format")
        if not c8859:
            with open("{}/{}".format(fdir,arq),"r") as f:
                content=f.read()#.decode("utf-8",errors="ignore")
        else:
            with codecs.open("{}/{}".format(fdir,arq),"r",'iso-8859-1') as f:
                content=f.read()
        results=re.findall(ex_,content)
        nicks+=[Q(i[-2]) for i in results]
        for match in re.findall(ex_,content):
            hour,minute,second,nick,msg=match

            nick=Q(nick)
            nicks.append(nick)
            ind=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick))
            uris=[P.rdf.ns.irc.nick]
            data=[nick]
            P.rdf.link([tg],ind,nick,uris,data)

            dt=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute,second)])
            timestamp=dt.isoformat()
            while timestamp in timestamps:
                timestamp+='_r_%05x' % random.randrange(16**5)
            timestamps.update([timestamp])
            imsg=P.rdf.IC([tg],P.rdf.ns.irc.Message,"{}-{}".format(aname,timestamp))
            if msg:
                uris=[P.rdf.ns.irc.messageContent]
                data=[msg]
            else:
                uris=[P.rdf.ns.irc.empty]
                data=[True]
                msg="EMPTYMSG"
            uris+=[P.rdf.ns.irc.sentAt,P.rdf.ns.irc.indirectMessage]
            data+=[dt,True]
            P.rdf.link([tg],imsg,msg,uris,data)
            P.rdf.link_([tg],imsg,msg,[P.rdf.ns.irc.user],[ind])
            if (1+count)%1000==0:
                if Tbreak: break
                c("indirect msgs check 1000")
            count+=1


#    exp=r"(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2})  \<(.*?)\> (.*)"
    NICKS=set(nicks)
    for arq in arqs:
        date=arq.split(".")[0]
        if len(date)==8:
            year,month,day=re.findall(exp1,date)[0]
        elif len(date)==6:
            year,month=re.findall(exp1_,date)[0]
        else:
            raise ValueError("date string from filename have a different format")
        with open("{}/{}".format(fdir,arq),"r") as f:
            content=f.read()#.decode("utf-8",errors="ignore")
        results=re.findall(ex,content)
        for match in results:
            hour, minute, second, nick, msg=match

            nick=Q(nick)
            # achar direct message com virgula! TTM

            toks=k.word_tokenize(msg)
            toks=[i for i in toks if i not in set(string.punctuation)]
            nicks2=[] # for directed messages at
            nicks3=[] # for mentioned fellows
            direct=1
            for tok in toks:
                if tok not in NICKS:
                    direct=0
                else:
                    if direct:
                        nicks2+=[tok]
                    else:
                        nicks3+=[tok]
            if nicks2:
                msg_=msg[msg.index(nicks2[-1])+len(nicks2[-1])+1:].lstrip()
            # cria indivíduos: mensagem e usuarios para os nicks
            ind=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick))
            #if "discutir se a prioridade" in msg:
            #    wer=asd
            uris=[P.rdf.ns.irc.nick]
            data=[nick]
            P.rdf.link([tg],ind,nick,uris,data)
            # usuario se conecta com o nick (strings)
            #P.rdf.link([tg],ind,nick,uris,data)
            inds2=[]
            for nickfoo in nicks2:
                nickfoo=Q(nickfoo)
                ind2=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nickfoo))
                data =[nickfoo]
                uris =[P.rdf.ns.irc.nick]
                P.rdf.link([tg],ind2,nickfoo,uris,data)
                inds2+=[ind2]
            inds3=[]
            for nickfoo in nicks3:
                nickfoo=Q(nickfoo)
                ind3=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nickfoo))
                inds3+=[ind3]

            # mensagem se conecta com usuarios (URIS) e textos (strings)
            dt=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute,second)])
            timestamp=dt.isoformat()
            while timestamp in timestamps:
                timestamp+='_r_%05x' % random.randrange(16**5)
            timestamps.update([timestamp])
            imsg=P.rdf.IC([tg],P.rdf.ns.irc.Message,"{}-{}".format(aname,timestamp))
            if msg:
                uris=[P.rdf.ns.irc.messageContent]
                data=[msg]
                if nicks2:
                    uris+=[P.rdf.ns.irc.cleanedMessage]
                    data+=[msg_]
            else:
                uris=[P.rdf.ns.irc.empty]
                data=[True]
                msg="EMPTYMSG"
            uris+=[P.rdf.ns.irc.sentAt,P.rdf.ns.irc.systemMessage]
            data+=[dt,False]
            P.rdf.link([tg],imsg,msg,uris,data)
                # adiciona tripla da msg para empty message true

            uris=[P.rdf.ns.irc.author]
            uris2=[ind]
            for ind2 in inds2:
                uris+=[P.rdf.ns.irc.directedTo]
                uris2+=[ind2]
            uris3=[]
            for ind3 in inds3:
                uris+=[P.rdf.ns.irc.mentions]
                uris3+=[ind3]
            uris23=uris2+uris3

            P.rdf.link_([tg],imsg,msg,uris,uris23)

            if (1+count)%1000==0:
                if Tbreak: break
                c("check 1000")
            count+=1
    c("tudo em RDF")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}/{}/".format(fpath,aname)
#    return fpath_, tg_,exp,t,t_
#    return tg_
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)
    # copia o script que gera este codigo
    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    #shutil.copy(this_dir+"/../tests/rdfMyFNetwork2.py",fpath+"scripts/")
    shutil.copy(scriptpath,fpath_+"scripts/")
    # copia do base data
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copytree(fdir,fpath_+"base/all")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)
    # faz um README
    # make analysis from graph
    dates=[i for i in tg_[0].query(r"SELECT ?p WHERE {?s irc:sentAt ?p} ORDER BY ASC(?p)")]
    date1=dates[0][0].value
    date2=dates[-1][0].value
    #return tg_
    #nicks=queryMe(tg_[0],"SELECT ?s ?o WHERE {?s irc:nick ?o}")
    nnicks=countMe(tg_[0],"irc:nick")
    nicks=getAll(  tg_[0],"irc:nick")
    eq=detectEquivalent(nicks)
    ndnicks=len(nicks)-len(eq)

    #nnicks=len(nicks)
    ndirect=countMe(tg_[0],"irc:directedTo")
    nmsgs=countMe(  tg_[0],"irc:messageContent")
    ninds=countMe(  tg_[0],"irc:indirectMessage","true")
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the IRC Network {}
        collected around {}, with messages from {} to {}.
It has {} nicks (~{} different) with {} directed messages.
Total messages count {}
of which {} are indirect.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from lalenia (a Supybot) in data/\n
\nNICKS: {}\n
NICKS parecidos: {}""".format(
            channel_info,created_at,date1,date2,
            nnicks,ndnicks,ndirect,nmsgs,ninds,nicks,eq))
    return tg_


def publishLog(fname,fpath,aname=None,scriptpath=None,created_at=None,channel_info="channel #labmarambira at Freenode",donated_by="labMacambira.sf.net",latin=False,utf8_fix=True):
    if not aname:
        name=aname=fname.split(".")[0]
    if not created_at:
        created_at=datetime.datetime.now()
    tg=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"IRC log linked data")
    tg2=P.rdf.makeBasicGraph([["po","irc"],[P.rdf.ns.po,P.rdf.ns.irc]],"RDF metadata IRC log")
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
                          P.rdf.ns.po.discoveryRDFFile,
                          P.rdf.ns.po.discoveryTTLFile,
                          P.rdf.ns.po.acquiredThrough,
                          P.rdf.ns.rdfs.comment,
                          ],
                          [created_at,
                           datetime.datetime.now(),
                           donated_by,
                           "https://github.com/ttm/{}".format(aname),
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
    if utf8_fix:
        t=utf8Fix(t)
    # get users, messages, times
    # ver se estamos jogando algo fora TTM
    count=1
    timestamps=set()
    mids=set()
    #for match in re.findall(exp,t):

    exp0=r"(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2})  \*\*\* (\S+) (.*)"
    for match in re.findall(exp0,t):
        year, month, day, hour, minute, second, nick, msg=match
        nick=Q(nick)
        ind=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick))
        uris=[P.rdf.ns.irc.nick]
        data=[nick]
        P.rdf.link([tg],ind,nick,uris,data)


        dt=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute,second)])
        timestamp=dt.isoformat()
        while timestamp in timestamps:
            timestamp+='_r_%05x' % random.randrange(16**5)
        timestamps.update([timestamp])
        imsg=P.rdf.IC([tg],P.rdf.ns.irc.Message,"{}-{}".format(aname,timestamp))
        if msg:
            uris=[P.rdf.ns.irc.messageContent]
            data=[msg]
        else:
            uris=[P.rdf.ns.irc.empty]
            data=[True]
            msg="EMPTYMSG"
        uris+=[P.rdf.ns.irc.sentAt,P.rdf.ns.irc.systemMessage,P.rdf.ns.irc.impliedUser]
        data+=[dt,True]
        P.rdf.link([tg],imsg,msg,uris,data)
        P.rdf.link_([tg],imsg,msg,[P.rdf.ns.irc.impliedUser],[ind])
        if (1+count)%1000==0:
            if Tbreak: break
            c("operational msgs check 1000")
        count+=1


    exp=r"(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2})  \<(.*?)\> (.*)"
    results=re.findall(exp,t)
    NICKS=set([i[-2] for i in results])
    for match in results:
        year, month, day, hour, minute, second, nick, msg=match
        nick=Q(nick)
        # achar direct message com virgula! TTM

        toks=k.word_tokenize(msg)
        toks=[i for i in toks if i not in set(string.punctuation)]
        nicks2=[] # for directed messages at
        nicks3=[] # for mentioned fellows
        direct=1
        for tok in toks:
            if tok not in NICKS:
                direct=0
            else:
                if direct:
                    nicks2+=[tok]
                else:
                    nicks3+=[tok]
        if nicks2:
            msg_=msg[msg.index(nicks2[-1])+len(nicks2[-1])+1:].lstrip()
        # cria indivíduos: mensagem e usuarios para os nicks
        ind=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nick))
        #if "discutir se a prioridade" in msg:
        #    wer=asd
        uris=[P.rdf.ns.irc.nick]
        data=[nick]
        P.rdf.link([tg],ind,nick,uris,data)
        # usuario se conecta com o nick (strings)
        #P.rdf.link([tg],ind,nick,uris,data)
        inds2=[]
        for nickfoo in nicks2:
            nickfoo=Q(nickfoo)
            ind2=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nickfoo))
            data =[nickfoo]
            uris =[P.rdf.ns.irc.nick]
            P.rdf.link([tg],ind2,nickfoo,uris,data)
            inds2+=[ind2]
        inds3=[]
        for nickfoo in nicks3:
            nickfoo=Q(nickfoo)
            ind3=P.rdf.IC([tg],P.rdf.ns.irc.Participant,"{}-{}".format(aname,nickfoo))
            inds3+=[ind3]

        # mensagem se conecta com usuarios (URIS) e textos (strings)
        dt=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute,second)])
        timestamp=dt.isoformat()
        while timestamp in timestamps:
            timestamp+='_r_%05x' % random.randrange(16**5)
        timestamps.update([timestamp])
        imsg=P.rdf.IC([tg],P.rdf.ns.irc.Message,"{}-{}".format(aname,timestamp))
        if msg:
            uris=[P.rdf.ns.irc.messageContent]
            data=[msg]
            if nicks2:
                uris+=[P.rdf.ns.irc.cleanedMessage]
                data+=[msg_]
        else:
            uris=[P.rdf.ns.irc.empty]
            data=[True]
            msg="EMPTYMSG"
        uris+=[P.rdf.ns.irc.sentAt,P.rdf.ns.irc.systemMessage]
        data+=[dt,False]
        P.rdf.link([tg],imsg,msg,uris,data)
            # adiciona tripla da msg para empty message true

        uris=[P.rdf.ns.irc.author]
        uris2=[ind]
        for ind2 in inds2:
            uris+=[P.rdf.ns.irc.directedTo]
            uris2+=[ind2]
        uris3=[]
        for ind3 in inds3:
            uris+=[P.rdf.ns.irc.mentions]
            uris3+=[ind3]
        uris23=uris2+uris3

        P.rdf.link_([tg],imsg,msg,uris,uris23)

        if (1+count)%1000==0:
            if Tbreak: break
            c("check 1000")
        count+=1
    c("tudo em RDF")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}/{}/".format(fpath,aname)
#    return fpath_, tg_,exp,t,t_
#    return tg_
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
    # make analysis from graph
    dates=[i for i in tg_[0].query(r"SELECT ?p WHERE {?s irc:sentAt ?p} ORDER BY ASC(?p)")]
    date1=dates[0][0].value
    date2=dates[-1][0].value
    #return tg_
    #nicks=queryMe(tg_[0],"SELECT ?s ?o WHERE {?s irc:nick ?o}")
    nnicks=countMe(tg_[0],"irc:nick")
    nicks=getAll(  tg_[0],"irc:nick")
    eq=detectEquivalent(nicks)
    ndnicks=len(nicks)-len(eq)

    #nnicks=len(nicks)
    ndirect=countMe(tg_[0],"irc:directedTo")
    nmsgs=countMe(  tg_[0],"irc:messageContent")
    nops=countMe(  tg_[0],"irc:systemMessage","true")
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the IRC Network {}
        collected around {}, with messages from {} to {}.
It has {} nicks (~{} different) with {} directed messages.
Total messages count {}
of which {} are operational.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from lalenia (a Supybot) in data/\n
\nNICKS: {}\n
NICKS parecidos: {}""".format(
            channel_info,created_at,date1,date2,
            nnicks,ndnicks,ndirect,nmsgs,nops,nicks,eq))
    return tg_

#def detectInteractions(graph):
#    q="SELECT ?nick ?msg ?d WHERE { ?f irc:messageContent ?msg . ?f irc:author ?a . ?a irc:nick ?nick . ?f irc:sentAt ?d} ORDER BY ASC(?d)"
#    msgs=[i for i in graph.query(q)]
#    # ve se a mensagem é candidata por comecar frase e terminar com , ou :
#    # confirma se for nick
#
#    return 
