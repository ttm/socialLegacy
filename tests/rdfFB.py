import social as S, percolation as P, os
import  importlib
importlib.reload(S.fb)
importlib.reload(S.fb.gdf2rdf)
c=P.utils.check
#fnames=("AdornoNaoEhEnfeite29032013.gdf","AdornoNaoEhEnfeite29032013_interacoes.gdf","265217103529531",0,"https://www.facebook.com/groups/265217103529531/permalink/525654127485826/")
fnames=    ("PartidoPirata23032013.gdf","PartidoPirata23032013_interactions.gdf",0,"partidopiratabrasil","https://www.facebook.com/groups/partidopiratabrasil/permalink/10151409024509317/")
dpath="../data/fb/gdf/"
fpath="./publishing/fb2/"
umbrella_dir="fbGroups/"
scriptpath=os.path.realpath(__file__)
S.fb.triplifyGDF(dpath=dpath,
                 fname=fnames[0],
                 fnamei=fnames[1],
                 fpath=fpath,
                 scriptpath=scriptpath,
                 uid=fnames[2],
                 sid=fnames[3],
                 fb_link=fnames[4],
                 ego=False,
                 umbrella_dir=umbrella_dir)
#eurl="http://200.144.255.210:8082/dsfoo"
#path="./publishing/fb2/{}_fb/rdf/".format(fnames[0].split(".")[0])
#P.utils.testRdfs(path,eurl)
# write to the info, meta or discovery graph about the graphs created
# access this point to retrieve info from other graphs
# in percolation/tests/makeBasicStructs2.py



