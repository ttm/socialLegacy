import percolation as P, social as S, rdflib as r, builtins as B, re, datetime, os, shutil
c=P.utils.check

def triplifyGDF(dpath="../data/fb/",fname="foo.gdf",fnamei="foo_interaction.gdf",
        fpath="./fb/",scriptpath=None,uid=None,sid=None,fb_link=None,ego=True):
    """Produce a linked data publication tree from a standard GDF file.

    INPUTS:
    ======
    => the data directory path
    => the file name (fname) of the friendship network
    => the file name (fnamei) of the interaction network
    => the final path (fpath) for the tree of files to be created
    => a path to the script that is calling this function (scriptpath)
    => the numeric id (uid) of the facebook user or group of the network(s)
    => the numeric id (sid) of the facebook user or group of the network (s)
    => the facebook link (fb_link) of the user or group
    => the network is from a user (ego==True) or a group (ego==False)

    OUTPUTS:
    =======
    the tree in the directory fpath."""

    day,month,year=re.findall(r".*(\d\d)(\d\d)(\d\d\d\d).gdf",fname)[0]
    B.datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)])
    B.datetime_snapshot_=datetime_snapshot.isoformat().split("T")[0]
    B.fname=fname
    B.name=fname[:-4]
    B.ego=ego
    B.friendship=bool(fname)
    B.interaction=bool(fname)
    B.sid=sid
    B.uid=uid
    B.scriptpath=scriptpath
    B.fb_link=fb_link
    B.dpath=dpath
    B.fpath=fpath

    fnet=S.fb.readGDF(dpath+fname)     # return networkx graph
    fnet_=rdfFriendshipNetwork(fnet)   # return rdflib graph
    inet=S.fb.readGDF(dpath+fnamei)    # return networkx graph
    inet_=rdfInteractionNetwork(inet)      # return rdflib graph
    meta=makeMetadata(fnet_,inet_)     # return rdflib graph with metadata about the structure
    writeAllFB(fnet_,inet_,meta)  # write linked data tree

def trans(tkey):
    if tkey=="name":
        return "uid"
    if tkey=="label":
        return "name"
    return tkey

def rdfInteractionNetwork(fnet):
    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"Facebook interaction network from {} . Ego: {}".format(B.name,B.ego))
    tkeys=list(fnet["individuals"].keys())
    if sum([("user" in i) for i in fnet["individuals"]["label"]])==len(fnet["individuals"]["label"]):
        # nomes falsos, ids espurios
        anonymized=True
    else:
        anonymized=False
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
        foo["vals"]+=[fnet["individuals"][tkey]]
    iname= tkeys.index("name")
    ilabel=tkeys.index("label")
    icount=0
    uid_names={}
    for vals_ in zip(*foo["vals"]):
        vals_=list(vals_)
        #name,label=[foo["vals"][i][icount] for i in ("name","label")]
        cid=vals_[iname]
        foo_=foo["uris"][:]
        if anonymized:
            name_="{}-{}-{}".format(B.name,B.groupid,B.datetime_snapshot_)
            uid_names[cid]=name_
            # remove name and label from vals_ and foo["uris"]
            vals_.pop(ilabel)
            vals_.pop(iname-1)
            foo_.pop(ilabel)
            foo_.pop(iname-1)
        elif not label:
            name_="po:noname-{}-{}-{}".format(cid,B.groupid,B.datetime_snapshot)
            vals_=list(vals_)
            vals_[ilabel]=name_
        else:
            name_,label=[foo["vals"][i][icount] for i in (iname,ilabel)]
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,name_)
        P.rdf.link([tg],ind,None,foo_,
                        vals_)
        icount+=1

    interactions_=[fnet["relations"][i] for i in ("node1","node2","weight")]
    c("escritos participantes")
    i=1
    for uid1,uid2,weight in zip(*interactions_):
        weight_=int(weight)
        if weight_-weight != 0:
            raise ValueError("float weights in fb interaction networks?")
        if anonymized:
            uid1=uid_names[uid1]
            uid2=uid_names[uid2]
            flabel="{}-{}".format(uid1,uid2)
        else:
            flabel="{}-{}-{}-{}".format(fname,datetime_,uid1,uid2)
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Interaction,flabel)
        uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
        P.rdf.link_([tg],ind,None,[P.rdf.ns.fb.iFrom,P.rdf.ns.fb.iTo],
                                  uids,draw=False)
        P.rdf.link([tg],ind,None,[P.rdf.ns.fb.weight],
                                  [weight_],draw=False)
        if (i%1000)==0:
            c(i)
        i+=1
    c("escritas amizades")
    return tg

def rdfFriendshipNetwork(fnet):
    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"Facebook friendship network from {} . Ego: {}".format(B.name,B.ego))
    tkeys=list(fnet["individuals"].keys())
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        if tkey != "groupid":
            foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
            foo["vals"]+=[fnet["individuals"][tkey]]
    if "groupid" in tkeys:
        B.groupid=fnet["individuals"][tkey][0]
        tkeys.remove("groupid")
    else:
        B.groupid=None
    iname= tkeys.index("name")
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

    friendships_=[fnet["relations"][i] for i in ("node1","node2")]
    c("escritos participantes")
    i=1
    for uid1,uid2 in zip(*friendships_):
        ind1=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid1)
        ind2=P.rdf.IC(None,P.rdf.ns.fb.Participant,uid2)
        uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
        P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
        if (i%1000)==0:
            c(i)
        i+=1
    P.rdf.G(tg[0],P.rdf.ns.fb.friend,
            P.rdf.ns.rdf.type,
            P.rdf.ns.owl.SymmetricProperty)
    c("escritas amizades")
    return tg

def makeMetadata(fnet,inet):
    desc="facebook network from {} . Ego: {}. Friendship: {}. Interaction: {}.".format(B.name,B.ego,B.friendship,B.interaction)
    tg2=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"Metadata for the "+desc)
    aname=B.name+"_fb"
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))
    P.rdf.link([tg2],ind,"Snapshot {}".format(B.name),
                [P.rdf.ns.po.groupId,],
                [B.groupid])
    # com e sem interaction no final
    datetime_snapshot_=datetime_snapshot.isoformat().split("T")[0]
    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]], ) # drop de agraph
    tg2=P.rdf.makeBasicGraph([["po"],[P.rdf.ns.per]],     "Metadata for the "+desc) # drop de agraph
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))

    foo={"uris":[],"vals":[]}
    if B.sid:
        foo["uris"].append(P.rdf.ns.fb.sid)
        foo["vals"].append(B.sid)
    if B.uid:
        foo["uris"].append(P.rdf.ns.fb.uid)
        foo["vals"].append(B.uid)
    if B.fb_link:
        foo["uris"].append(P.rdf.ns.fb.fbLink)
        foo["vals"].append(B.fb_link)
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
                           B.name,
                           "https://github.com/ttm/{}".format(aname),
                           "https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/base/{}".format(aname,B.fname),
                           "https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                           "https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Meta.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Netvizz",
                                desc,
                           ]+foo["vals"])
    #for friend_attr in fg2["friends"]:
    return tg2
def writeAllFB(fnet,inet,mnet):
    aname=B.name+"_fb"
    fpath_="{}{}/".format(B.fpath,B.name)
    if B.friendship:
        P.rdf.writeAll(fnet,aname+"Friendship",fpath_,False,1)
    if B.interaction:
        P.rdf.writeAll(inet,aname+"Interaction",fpath_)
    # copia o script que gera este codigo
    if not os.path.isdir(fpath_+"scripts"):
        os.mkdir(fpath_+"scripts")
    shutil.copy(scriptpath,fpath_+"scripts/")
    # copia do base data
    if not os.path.isdir(fpath_+"base"):
        os.mkdir(fpath_+"base")
    shutil.copy(B.dpath+fname,fpath_+"base/")
    P.rdf.writeAll(mnet,aname+"Meta",fpath_,1)
    # faz um README
    with open(fpath_+"README","w") as f:
        f.write("""This repo delivers RDF data from the facebook
friendship network of {} collected at {}.
It has {} friends with metadata {};
and {} friendships.
The linked data is available at rdf/ dir and was
generated by the routine in the script/ directory.
Original data from Netvizz in data/\n""".format(
            B.name,datetime_snapshot,
            B.name,B.datetime_snapshot_,"x friends",
                    "X facebook numeric id, name, locale, sex and agerank",
                    "x friendships"
                    ))

