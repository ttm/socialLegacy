import time, os, pickle, shutil, datetime, re
import networkx as x, rdflib as r
from splinter import Browser
from bs4 import BeautifulSoup
import percolation as P
c=P.utils.check
this_dir = os.path.split(__file__)[0]

def triplifyGML(fname="foo.gml",fpath="./fb/",scriptpath=None,uid=None,sid=None):
    """Produce a linked data publication tree from a standard GML file.

    INPUTS:
    => the file name (fname, with path) where the gdf file
    of the friendship network is.

    => the final path (fpath) for the tree of files to be created.
    
    => a path to the script that is calling this function (scriptpath).

    => the numeric id (uid) of the facebook user of which fname holds a friendship network 
    
    => the numeric id (sid) of the facebook user of which fname holds a friendship network 

    OUTPUTS:
    the tree in the directory fpath."""

#    aname=fname.split("/")[-1].split(".")[0]
    aname=fname.split("/")[-1].split(".")[0]
    if "RonaldCosta" in fname:
        aname=fname.split("/")[-1].split(".")[0]
        name,day,month,year=re.findall(".*/([a-zA-Z]*)(\d\d)(\d\d)(\d\d\d\d).gml",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)]).isoformat().split("T")[0]
        name_="Ronald Scherolt Costa"
    elif "AntonioAnzoategui" in fname:
        aname=re.findall(".*/([a-zA-Z]*\d*)",fname)[0]
        name,year,month,day,hour,minute=re.findall(r".*/([a-zA-Z]*).*_(\d+)_(\d*)_(\d*)_(\d*)_(\d*)_.*",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute)]).isoformat()[:-3]
        name_="Antônio Anzoategui Fabbri"
    elif re.findall(".*/[a-zA-Z]*(\d)",fname):
        name,day,month,year=re.findall(".*/([a-zA-Z]*)(\d\d)(\d\d)(\d\d\d\d).*.gml",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    elif re.findall("[a-zA-Z]*_",fname):
        name,year,month,day,hour,minute=re.findall(".*/([a-zA-Z]*).*(\d\d\d\d)_(\d\d)_(\d\d)_(\d\d)_(\d\d).*.gml",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    else:
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"My facebook ego friendship network")
    tg2=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"RDF metadata for the facebook friendship network of my son")
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))
    c("snapshot")
    aname+="_fb"
    name+="_fb"
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
                          P.rdf.ns.fb.uid,
                          P.rdf.ns.fb.sid
                          ],
                          [datetime_snapshot,
                           datetime.datetime.now(),
                           name,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")[-1]),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Netvizz",
                                "The facebook friendship network from {}".format(name_),
                                uid,
                                sid
                           ])
    #for friend_attr in fg2["friends"]:
    c((aname,name_,datetime_snapshot))
    fg2=x.read_gml(fname)
    c("read gml")
    for uid in fg2:
        c(uid)
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,"{}-{}".format(aname,uid))
        if "locale" in fg2.node[uid].keys():
            data=[fg2.node[uid][attr] for attr in ("id","label","locale","sex","agerank","wallcount")]
            uris=[P.rdf.ns.fb.gid, P.rdf.ns.fb.name,
                        P.rdf.ns.fb.locale, P.rdf.ns.fb.sex,
                        P.rdf.ns.fb.agerank,P.rdf.ns.fb.wallcount]
        else:
            data=[fg2.node[uid][attr] for attr in ("id","label","sex","agerank","wallcount")]
            uris=[P.rdf.ns.fb.gid, P.rdf.ns.fb.name,
                        P.rdf.ns.fb.sex,
                        P.rdf.ns.fb.agerank,P.rdf.ns.fb.wallcount]
        P.rdf.link([tg],ind,data[1],uris,data,draw=False)


    #friends_=[fg2["friends"][i] for i in ("name","label","locale","sex","agerank")]
    #for name,label,locale,sex,agerank in zip(*friends_):
    #    ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,name,label)
    #    P.rdf.link([tg],ind,label,[P.rdf.ns.fb.uid,P.rdf.ns.fb.name,
    #                    P.rdf.ns.fb.locale,P.rdf.ns.fb.sex,
    #                    P.rdf.ns.fb.agerank],
    #                    [name,label,locale,sex,agerank])

    c("escritos participantes")
    #friendships_=[fg2["friendships"][i] for i in ("node1","node2")]
    i=1
    for uid1,uid2 in fg2.edges():
        flabel="{}-{}-{}".format(aname,uid1,uid2)
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Friendship,
                flabel)
#                flabel,"Friendship "+flabel)
#        ind1=P.rdf.IC([tg],P.rdf.ns.fb.Friendship,uid1,"")
#        ind2=P.rdf.IC([tg],P.rdf.ns.fb.Friendship,uid2,"")
#        uids=[P.rdf.IC(None,P.rdf.ns.fb.Participant,i) for i in (uid1,uid2)]
        uids=[P.rdf.IC(None,P.rdf.ns.fb.Participant,"{}-{}".format(aname,i)) for i in (uid1,uid2)]
        #uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
        P.rdf.link_([tg],ind,flabel,[P.rdf.ns.fb.member]*2, uids,draw=False)
        P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
        if (i%1000)==0:
            c(i)
        i+=1
    P.rdf.G(tg[0],P.rdf.ns.fb.friend,
            P.rdf.ns.rdf.type,
            P.rdf.ns.owl.SymmetricProperty)
    c("escritas amizades")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}/{}/".format(fpath,aname)
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
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,False)
    # faz um README
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the facebook
friendship network of {} collected at {}.
It has {} friends with metadata {};
and {} friendships.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from Netvizz in data/\n""".format(
            name_,datetime_snapshot,
            fg2.number_of_nodes(),
                    "name, locale (maybe), sex, agerank and wallcount",
                    fg2.number_of_edges()))


def triplifyGDFInteraction(fname="foo.gdf",fpath="./fb/",scriptpath=None,uid=None,sid=None,dlink=None):
    """Produce a linked data publication tree from GDF files of a Facebook interaction network.

    INPUTS:
    => the file name (fname, with path) where the gdf file
    of the friendship network is.

    => the final path (fpath) for the tree of files to be created.
    
    => a path to the script that is calling this function (scriptpath).

    => the numeric id (uid) of the facebook group
    
    => the string id (sid) of the facebook group of which fname holds a friendship network 

    OUTPUTS:
    the tree in the directory fpath."""
    #aname=fname.split("/")[-1].split(".")[0]+"_fb"
    aname=fname.split("/")[-1].split(".")[0]
    if re.findall("[a-zA-Z]*_[0-9]",fname):
        name,year,month,day,hour,minute=re.findall(".*/([a-zA-Z]*).*(\d\d\d\d)_(\d\d)_(\d\d)_(\d\d)_(\d\d).*.gdf",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    elif re.findall("(\d)",fname):
        name,day,month,year=re.findall(".*/([a-zA-Z]*)(\d\d)(\d\d)(\d\d\d\d).*.gdf",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    else:
        datetime_snapshot=datetime.datetime(2013,3,15).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",aname))
    aname+="_fb"
    name=aname


    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"The facebook interaction network from the {} file".format(fname)) # drop de agraph
    tg2=P.rdf.makeBasicGraph([["po"],[P.rdf.ns.per]],"Metadata for my facebook ego friendship network RDF files") # drop de agraph
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))

    foo={"uris":[],"vals":[]}
    if sid:
        foo["uris"].append(P.rdf.ns.fb.sid)
        foo["vals"].append(sid)
    if uid:
        foo["uris"].append(P.rdf.ns.fb.uid)
        foo["vals"].append(uid)
    if dlink:
        foo["uris"].append(P.rdf.ns.fb.link)
        foo["vals"].append(dlink)
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
                          ]+foo["uris"],
                          [datetime_snapshot,
                           datetime.datetime.now(),
                           name,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Netvizz",
                                "The facebook friendship network from {}".format(name_),
                           ]+foo["vals"])
    #for friend_attr in fg2["friends"]:
    fg2=readGDF(fname)
    tkeys=list(fg2["friends"].keys())
    def trans(tkey):
        if tkey=="name":
            return "uid"
        if tkey=="label":
            return "name"
        return tkey
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        if tkey=="groupid":
            P.rdf.link([tg2],ind,"Snapshot {}".format(aname),
                        [P.rdf.ns.po.uid,],
                        [fg2["friends"][tkey][0]])
        if tkey:
            foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
            foo["vals"]+=[fg2["friends"][tkey]]
    print(tkeys)
    iname=tkeys.index("name")
    ilabel=tkeys.index("label")
    icount=0
    name_label={}
    for vals_ in zip(*foo["vals"]):
        name,label=[foo["vals"][i][icount] for i in (iname,ilabel)]
        if not label:
            label="po:noname"
            vals_=list(vals_)
            vals_[ilabel]=label
        name_label[name]=label
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,name,label)
        P.rdf.link([tg],ind,label,foo["uris"],
                        vals_,draw=False)
        icount+=1

    friendships_=[fg2["friendships"][i] for i in ("node1","node2")]
    c("escritos participantes")
    i=1
    for uid1,uid2 in zip(*friendships_):
        flabel="{}-{}".format(uid1,uid2)
        labels=[name_label[uu] for uu in (uid1,uid2)]
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Friendship,
                flabel)
                #flabel,"Friendship "+flabel)
        ind1=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid1)
        ind2=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid2)
        uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
        P.rdf.link_([tg],ind,"Friendship "+flabel,[P.rdf.ns.fb.member]*2,
                            uids,labels,draw=False)
        P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
        if (i%1000)==0:
            c(i)
        i+=1
    P.rdf.G(tg[0],P.rdf.ns.fb.friend,
            P.rdf.ns.rdf.type,
            P.rdf.ns.owl.SymmetricProperty)
    c("escritas amizades")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}{}/".format(fpath,aname)
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)
    # copia o script que gera este codigo
    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")
    # copia do base data
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copy(fname,fpath_+"base/")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)
    # faz um README
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the facebook
friendship network of {} collected at {}.
It has {} friends with metadata {};
and {} friendships.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from Netvizz in data/\n""".format(
            name_,datetime_snapshot,
            len(fg2["friends"]["name"]),
                    "facebook numeric id, name, locale, sex and agerank",
                    len(fg2["friendships"]["node1"])
                    ))


def triplifyGDF(fname="foo.gdf",fpath="./fb/",scriptpath=None,uid=None,sid=None,dlink=None):
    """Produce a linked data publication tree from a standard GDF file.

    INPUTS:
    => the file name (fname, with path) where the gdf file
    of the friendship network is.

    => the final path (fpath) for the tree of files to be created.
    
    => a path to the script that is calling this function (scriptpath).

    => the numeric id (uid) of the facebook user of which fname holds a friendship network 
    
    => the numeric id (sid) of the facebook user of which fname holds a friendship network 

    OUTPUTS:
    the tree in the directory fpath."""
    #aname=fname.split("/")[-1].split(".")[0]+"_fb"
    aname=fname.split("/")[-1].split(".")[0]
    if re.findall("[a-zA-Z]*_[0-9]",fname):
        name,year,month,day,hour,minute=re.findall(".*/([a-zA-Z]*).*(\d\d\d\d)_(\d\d)_(\d\d)_(\d\d)_(\d\d).*.gdf",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    elif re.findall("(\d)",fname):
        name,day,month,year=re.findall(".*/([a-zA-Z]*)(\d\d)(\d\d)(\d\d\d\d).*.gdf",fname)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)]).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",name))
    else:
        datetime_snapshot=datetime.datetime(2013,3,15).isoformat().split("T")[0]
        name_=" ".join(re.findall("[A-Z][^A-Z]*",aname))
    aname+="_fb"
    name=aname


    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"My facebook ego friendship network") # drop de agraph
    tg2=P.rdf.makeBasicGraph([["po"],[P.rdf.ns.per]],"Metadata for my facebook ego friendship network RDF files") # drop de agraph
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))

    foo={"uris":[],"vals":[]}
    if sid:
        foo["uris"].append(P.rdf.ns.fb.sid)
        foo["vals"].append(sid)
    if uid:
        foo["uris"].append(P.rdf.ns.fb.uid)
        foo["vals"].append(uid)
    if dlink:
        foo["uris"].append(P.rdf.ns.fb.link)
        foo["vals"].append(dlink)
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
                          ]+foo["uris"],
                          [datetime_snapshot,
                           datetime.datetime.now(),
                           name,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname.split("/")),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Netvizz",
                                "The facebook friendship network from {}".format(name_),
                           ]+foo["vals"])
    #for friend_attr in fg2["friends"]:
    fg2=readGDF(fname)
    tkeys=list(fg2["friends"].keys())
    def trans(tkey):
        if tkey=="name":
            return "uid"
        if tkey=="label":
            return "name"
        return tkey
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        if tkey=="groupid":
            P.rdf.link([tg2],ind,"Snapshot {}".format(aname),
                        [P.rdf.ns.po.uid,],
                        [fg2["friends"][tkey][0]])
        if tkey:
            foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
            foo["vals"]+=[fg2["friends"][tkey]]
    print(tkeys)
    iname=tkeys.index("name")
    ilabel=tkeys.index("label")
    icount=0
    name_label={}
    for vals_ in zip(*foo["vals"]):
        name,label=[foo["vals"][i][icount] for i in (iname,ilabel)]
        if not label:
            label="po:noname"
            vals_=list(vals_)
            vals_[ilabel]=label
        name_label[name]=label
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,name,label)
        P.rdf.link([tg],ind,label,foo["uris"],
                        vals_,draw=False)
        icount+=1

    friendships_=[fg2["friendships"][i] for i in ("node1","node2")]
    c("escritos participantes")
    i=1
    for uid1,uid2 in zip(*friendships_):
        flabel="{}-{}".format(uid1,uid2)
        labels=[name_label[uu] for uu in (uid1,uid2)]
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Friendship,
                flabel)
                #flabel,"Friendship "+flabel)
        ind1=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid1)
        ind2=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid2)
        uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
        P.rdf.link_([tg],ind,"Friendship "+flabel,[P.rdf.ns.fb.member]*2,
                            uids,labels,draw=False)
        P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
        if (i%1000)==0:
            c(i)
        i+=1
    P.rdf.G(tg[0],P.rdf.ns.fb.friend,
            P.rdf.ns.rdf.type,
            P.rdf.ns.owl.SymmetricProperty)
    c("escritas amizades")
    tg_=[tg[0]+tg2[0],tg[1]]
    fpath_="{}{}/".format(fpath,aname)
    P.rdf.writeAll(tg_,aname+"Translate",fpath_,False,1)
    # copia o script que gera este codigo
    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")
    # copia do base data
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copy(fname,fpath_+"base/")
    P.rdf.writeAll(tg2,aname+"Meta",fpath_,1)
    # faz um README
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the facebook
friendship network of {} collected at {}.
It has {} friends with metadata {};
and {} friendships.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from Netvizz in data/\n""".format(
            name_,datetime_snapshot,
            len(fg2["friends"]["name"]),
                    "facebook numeric id, name, locale, sex and agerank",
                    len(fg2["friendships"]["node1"])
                    ))

def makeRDF(readgdf_dict,fdir="../data/rdf/"):
    # return rdflib graph from the data
    rd=readgdf_dict
#    ns=namespaces=pe.namespaces(["rdf","rdfs","xsd", # basic namespaces
#        ])
#    for friend in range(len(rd["friends"]["name"])):
#        pass

def readGDF(filename="../data/RenatoFabbri06022014.gdf"):
    """Made to work with my own network. Check file to ease adaptation"""
    with open(filename,"r") as f:
        data=f.read()
    lines=data.split("\n")
    columns=lines[0].split(">")[1].split(",")
    column_names=[i.split(" ")[0] for i in columns]
    data_friends={cn:[] for cn in column_names}
    for line in lines[1:]:
        if not line:
            break
        if ">" in line:
            columns=line.split(">")[1].split(",")
            column_names2=[i.split(" ")[0] for i in columns]
            data_friendships={cn:[] for cn in column_names2}
            continue
        fields=line.split(",")
        if "column_names2" not in locals():
            for i, field in enumerate(fields):
                if field.isdigit(): field=int(field)
                data_friends[column_names[i]].append(field)
        else:
            for i, field in enumerate(fields):
                if field.isdigit(): field=int(field)
                data_friendships[column_names2[i]].append(field)
    return {"friendships":data_friendships,
            "friends":data_friends}
    #self.makeNetwork()

class GDFgraph:
    """Read GDF graph into networkX"""
    def __init__(self,filename="../data/RenatoFabbri06022014.gdf"):
        with open(filename,"r") as f:
            self.data=f.read()
        self.lines=self.data.split("\n")
        columns=self.lines[0].split(">")[1].split(",")
        column_names=[i.split(" ")[0] for i in columns]
        data_friends={cn:[] for cn in column_names}
        for line in self.lines[1:]:
            if not line:
                break
            if ">" in line:
                columns=line.split(">")[1].split(",")
                column_names2=[i.split(" ")[0] for i in columns]
                data_friendships={cn:[] for cn in column_names2}
                continue
            fields=line.split(",")
            if "column_names2" not in locals():
                for i, field in enumerate(fields):
                    if field.isdigit(): field=int(field)
                    data_friends[column_names[i]].append(field)
            else:
                for i, field in enumerate(fields):
                    if field.isdigit(): field=int(field)
                    data_friendships[column_names2[i]].append(field)
        self.data_friendships=data_friendships
        self.data_friends=data_friends
        self.n_friends=len(data_friends[column_names[0]])
        self.n_friendships=len(data_friendships[column_names2[0]])
        self.makeNetwork()
    def makeNetwork(self):
        """Makes graph object from .gdf loaded data"""
        if "weight" in self.data_friendships.keys():
            self.G=G=x.DiGraph()
        else:
            self.G=G=x.Graph()
        F=self.data_friends
        for friendn in range(self.n_friends):
            if "posts" in F.keys():
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             posts=F["posts"][friendn])
            elif "agerank" in F.keys():
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             gender=F["sex"][friendn],
                             locale=F["locale"][friendn], 
                             agerank=F["agerank"][friendn])
            else:
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             gender=F["sex"][friendn],
                             locale=F["locale"][friendn])
        F=self.data_friendships
        for friendshipn in range(self.n_friendships):
            if "weight" in F.keys():
                G.add_edge(F["node1"][friendshipn],F["node2"][friendshipn],weight=F["weight"][friendshipn])
            else:
                G.add_edge(F["node1"][friendshipn],F["node2"][friendshipn])

def readFBPost(fpath=""):
    """Extract information from HTML page with a Facebook post"""
    html=open(fpath,"rb")
    soup = BeautifulSoup(html, "lxml")
    return soup


class ScrapyBrowser:
    """Opens a browser for user to login to facebook.

    Such browser pulls data as requested by user."""
    def __init__(self,user_email=None, user_password=None,basedir="~/.social/"):
        self._BASE_DIR=basedir.replace("~",os.path.expanduser("~"))
        if not os.path.isdir(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)
        print("Opening *Scrappy* firefox browser. Please wait.")
        self.browser=browser=Browser(wait_time=2)
        url="http://facebook.com"
        browser.visit(url)
        if (not user_email) or (not user_password):
            input("\n\n==> Input user and password and login, please.\
                    and then press <enter>")
        else:
            browser.fill("email",user_email)
            browser.fill("pass",user_password)
            browser.find_by_value("Log In").click()
    def getFriends(self,user_id="astronauta.mecanico",write=True):
        """Returns user_ids (that you have access) of the friends of your friend with user_ids"""
        while user_id not in self.browser.url:
            self.browser.visit("http://www.facebook.com/{}/friends".format(user_id), wait_time=3)
        #self.go("http://www.facebook.com/{}/friends".format(user_id))
        T=time.time()
        while 1:
            h1=self.browser.evaluate_script("document.body.scrollHeight")
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            h2=self.browser.evaluate_script("document.body.scrollHeight")
            if h1 != h2:
                T=time.time()
            elif time.time()-T>10:
                break
        #links=self.browser.find_link_by_partial_href("hc_location=friends_tab")
        links=self.browser.find_by_css(".fcb")
        friends=[]
        for link in links:
            name=link.value
            user_id_=link.find_by_tag("a")["href"].split("/")[-1].split("?")[0]
            friends.append((user_id_,name))
        tdict={}
        tdict["name"]=self.browser.find_by_id("fb-timeline-cover-name").value
        tdict["user_id"]=user_id
        tdict["friends"]=friends
        infos=self.browser.find_by_css("._3c_")
        mutual=0
        for info in infos:
            if info.value=="Mutual Friends":
                if info.find_by_css("._3d0").value:
                    tdict["n_mutual"]=info.find_by_css("._3d0").value
                    mutual=1
            if info.value=="All Friends":
                    tdict["n_friends"]=info.find_by_css("._3d0").value
        if mutual==0:
            links=self.browser.find_by_css("._gs6")
            if "Mutual" in links.value:
                tdict["n_mutual"]=links.value.split(" ")[0]
        if write:
            if not os.path.isdir("{}/fb_ids/".format(self._BASE_DIR)):
                os.mkdir("{}/fb_ids/".format(self._BASE_DIR))
            with open("{}fb_ids/{}.pickle".format(self._BASE_DIR,user_id),"wb") as f:
                pickle.dump(tdict,f)
        self.tdict=tdict
        return tdict
