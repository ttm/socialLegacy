import percolation as P, builtins as B

def triplifyGDF(dpath="../data/fb/",fname="foo.gdf",fnamei="foo_interaction.gdf",fpath="./fb/",scriptpath=None,uid=None,sid=None,fb_link=None,ego=True):
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
    B.name=fname[:-4]

    fnet=S.fb.readGDF(dpath+fname)     # return networkx graph
    fnet_=rdfFriendshipNetwork(fnet)   # return rdflib graph
    inet=S.fb.readGDF(dpath+fnamei)    # return networkx graph
    inet_=rdfInteractionGDF(inet)      # return rdflib graph
    meta=makeMetadata(fnet_,inet_)     # return rdflib graph with metadata about the structure
    writeAll(fnet_,inet_,meta_,fpath)  # write linked data tree

def trans(tkey):
    if tkey=="name":
        return "uid"
    if tkey=="label":
        return "name"
    return tkey

def rdfInteractionNetwork(fnet):
    tkeys=list(fnet["individuals"].keys())
    iname=tkeys.index("name")
    ilabel=tkeys.index("label")
    if sum([("user" in i) for i in fnet["individuals"][ilabel]])==len(fnet["individuals"][0]):
        # nomes falsos, ids espurios
        anonymized=True
    else:
        anonymized=False
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        if not anonymized:
            foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
            foo["vals"]+=[fnet["individuals"][tkey]]
        else:
            if tkey not in ("name","label"):
                foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
                foo["vals"]+=[fnet["individuals"][tkey]]
    icount=0
    uid_names={}
    for vals_ in zip(*foo["vals"]):
        name,label=[foo["vals"][i][icount] for i in (iname,ilabel)]
        if anonymized:
            name_="{}-{}-{}".format(label,B.groupid,datetime_)
            uid_names[name]=name_
        elif not label:
            label="po:noname-{}-{}-{}".format(label,B.groupid,datetime_)
            vals_=list(vals_)
            vals_[ilabel]=label
        else:
        ind=P.rdf.IC([tg],P.rdf.ns.fb.Participant,name)
        P.rdf.link([tg],ind,label,foo["uris"],
                        vals_,draw=False)
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
        P.rdf.link_([tg],ind,None,[P.rdf.ns.fb.from,P.rdf.ns.fb.to],
                                  uids,draw=False)
        P.rdf.link([tg],ind,None,[P.rdf.ns.fb.weight],
                                  [weight_],draw=False)
        if (i%1000)==0:
            c(i)
        i+=1
    c("escritas amizades")
    return tg

def rdfFriendshipNetwork(fnet):
    tkeys=list(fnet["individuals"].keys())
    foo={"uris":[],"vals":[]}
    for tkey in tkeys:
        if tkey != "groupid":
            foo["uris"]+=[eval("P.rdf.ns.fb."+trans(tkey))]
            foo["vals"]+=[fnet["individuals"][tkey]]
    if "groupid" in tkeys:
        B.groupid=fnet["individuals"][tkey][0]
    else:
        B.groupid=None
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
    P.rdf.link([tg2],ind,"Snapshot {}".format(B.name),
                [P.rdf.ns.po.groupId,],
                [groupid])
    fname_=fname.split(".")[0]
    # com e sem interaction no final
    fname__=fname_.split("_interaction")[0]
    ccount=fname__.count("_")
    if ccount>2: # data com _ de separacao
        name,year,month,day,hour,minute=re.findall("([a-zA-Z]*).*(\d\d\d\d)_(\d\d)_(\d\d)_(\d\d)_(\d\d).*",fname__)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day,hour,minute)]).isoformat().split("T")[0]
    elif not any(char.isdigit() for char in fname__):
        name=fname__
        datetime_snapshot=datetime.datetime(2013,02)
    else: # data tudo junto
        name,day,month,year=re.findall("([a-zA-Z]*)(\d\d)(\d\d)(\d\d\d\d).*",fname__)[0]
        datetime_snapshot=datetime.datetime(*[int(i) for i in (year,month,day)])
    aname=name+"_fb"
    datetime_snapshot_=datetime_snapshot.isoformat().split("T")[0]
    quality=("interaction","friendship")[interaction in fname_]
    provenance=("ego","group")[ego]
    acomment="facebook {} {} network in linked data form the {} orifinal file".format(provenance,quality,fname)
    tg=P.rdf.makeBasicGraph([["po","fb"],[P.rdf.ns.per,P.rdf.ns.fb]], ) # drop de agraph
    tg2=P.rdf.makeBasicGraph([["po"],[P.rdf.ns.per]],     "Metadata for the facebook {} {} network RDF files form the {} orifinal file".format(provenance,quality,fname) # drop de agraph
    ind=P.rdf.IC([tg2],P.rdf.ns.po.Snapshot,
            aname,"Snapshot {}".format(aname))

    foo={"uris":[],"vals":[]}
    if sid:
        foo["uris"].append(P.rdf.ns.fb.sid)
        foo["vals"].append(sid)
    if uid:
        foo["uris"].append(P.rdf.ns.fb.uid)
        foo["vals"].append(uid)
    if fb_link:
        foo["uris"].append(P.rdf.ns.fb.fbLink)
        foo["vals"].append(fb_link)
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
                           "https://raw.githubusercontent.com/ttm/{}/master/base/{}".format(aname,fname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.owl".format(aname,aname),
                           "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Translate.ttl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.owl".format(aname,aname),
                                "https://raw.githubusercontent.com/ttm/{}/master/rdf/{}Meta.ttl".format(aname,aname),
                           "Netvizz",
                                acomment,
                           ]+foo["vals"])
    #for friend_attr in fg2["friends"]:
    fg2=readGDF(fname)
    fg2=readGDF(fnamei)
    tkeys=list(fg2["individuals"].keys())
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
    c("escritos participantes")
    friendships_=[fg2["friendships"][i] for i in ("node1","node2")]
    i=1
    for uid1,uid2 in zip(*friendships_):
        P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
        if (i%1000)==0:
            c("friendships {}".format(i))
        i+=1
    P.rdf.G(tg[0],P.rdf.ns.fb.friend,
            P.rdf.ns.rdf.type,
            P.rdf.ns.owl.SymmetricProperty)
    c("escritas amizades")
    return tg

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

