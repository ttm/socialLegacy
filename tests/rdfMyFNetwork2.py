import social as S, percolation as P
import  importlib
importlib.reload(S.fb)
importlib.reload(P.rdf)
fname="../data/fb/gdf/RenatoFabbri06022014.gdf"
#fpath="/home/r/repos/linkedRFabbri/"
fpath="./publishing/fb/"
aname=fname.split("/")[-1].split(".")[0]
print(aname)
S.fb.triplifyFriendshipNetwork(fname,fpath,aname)
# after execution of these commands,
# the fpath should have de files
# for using my fb data as linked data

#e.g.:
# tg=rdflib.load(fpath+"rdf/"+aname)
# q=tg.query("SELECT ?sname ?oname WHERE {?s fb:friend ?o . ?s fb:name ?fname . ?o fb:name ?oname .}")
# friends = [i for i in query]

# further versions should write
# smaller files and analysis
# of derived structures

# please check the
# Social and Percolation Python PyPI Packages
# for further analysing, linking or making media with
# these resources

