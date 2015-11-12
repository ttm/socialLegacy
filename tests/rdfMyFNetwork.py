import social as S, percolation as P, os, rdflib as r
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(S.fb)
importlib.reload(P.rdf)
importlib.reload(P.utils)
#importlib.reload(pe)
#dreload(S)
#os.environ["PATH"]=ENV
c=P.utils.check
standalone=0

fg=S.fb.GDFgraph() # graph should be on fg.G
fg2=S.fb.readGDF() # returns a dictionary with the variables

# if standalone, the final rdf does not require a reasoner

tg=P.rdf.makeBasicGraph([["per","fb"],[P.rdf.ns.per,P.rdf.ns.fb]],"My facebook ego friendship network") # drop de agraph
#for friend_attr in fg2["friends"]:
friends_=[fg2["friends"][i] for i in ("name","label","locale","sex","agerank")]
for name,label,locale,sex,agerank in zip(*friends_):
    ind=P.rdf.I([tg],P.rdf.ns.fb.Participant,name,label)
    P.rdf.link([tg],ind,label,[P.rdf.ns.fb.uid,P.rdf.ns.fb.name,
                    P.rdf.ns.fb.locale,P.rdf.ns.fb.sex,
                    P.rdf.ns.fb.agerank],
                    [name,label,locale,sex,agerank])

friendships_=[fg2["friendships"][i] for i in ("node1","node2")]
c("escritos participantes")
i=1
for uid1,uid2 in zip(*friendships_):
    flabel="{}-{}".format(uid1,uid2)
    ind=P.rdf.I([tg],P.rdf.ns.fb.Friendship,
            flabel,"FS"+flabel)
    ind1=P.rdf.I([tg],P.rdf.ns.fb.Friendship,uid1,"")
    ind2=P.rdf.I([tg],P.rdf.ns.fb.Friendship,uid2,"")
    uids=[r.URIRef(P.rdf.ns.fb.Participant+"#"+str(i)) for i in (uid1,uid2)]
    P.rdf.link_([tg],ind,flabel,[P.rdf.ns.fb.member]*2,
                        uids)
    P.rdf.L_([tg],uids[0],P.rdf.ns.fb.friend,uids[1])
    if (i%1000)==0:
        break
        c(i)
    i+=1
P.rdf.G(tg[0],P.rdf.ns.fb.friend,
        P.rdf.ns.rdf.type,
        P.rdf.ns.owl.SymmetricProperty)
c("escritas amizades")

if standalone:
    for uid1,uid2 in zip(*friendships_):
        P.rdf.L(ind2,P.rdf.ns.fb.friend,ind1)
    # put the inferreble triples from the friends relation

# write a network structure
# sequence of nodes
# or the correct sparql query to get network structure
# write python binary of network structure

P.rdf.writeAll(tg,"rfabbri","fb/","circo")

#P.rdf.C([tg],P.rdf.ns.per.Dataset,"Dataset",
#                comment="A collection of data typically in a computer readable format.",
#                        label_pt="Dataset")


#fg.fb.makeRDF(fg2)
