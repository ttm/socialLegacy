import social as S
import  importlib
importlib.reload(S.fb)
c=P.utils.check
fnames=[ ("AdornoNaoEhEnfeite29032013.gdf",
"AdornoNaoEhEnfeite29032013_interacoes.gdf",
"265217103529531",
0,
"https://www.facebook.com/groups/265217103529531/permalink/525654127485826/") ]
for dataset in fnames_[:1]:
    S.fb.triplifyGDF()
dpath="../data/fb/gdf/"
fpath="./publishing/fb2/"
scriptpath=os.path.realpath(__file__)
S.fb.triplifyGDF(dpath=dpath,
                 fname=fnames[0],
                 fnamei=fnames[1],
                 fpath=fpath,
                 scriptpath=scriptpath,
                 uid=fnames[2],
                 sid=fnames[3],
                 fb_link=fnames[4],
                 ego=False)
