import social as S, percolation as P, os
import  importlib
#importlib.reload(P.rdf)
importlib.reload(S)
importlib.reload(S.fb)
importlib.reload(S.fb.read)
importlib.reload(S.fb.gml2rdf)
c=P.utils.check
umbrella_dir="fbEgo/"
fpath="./publishing/fb4/"
dpath="../data/fb/gml/"
scriptpath=os.path.realpath(__file__)
fnames_=[
        ("AntonioAnzoategui18022013_182134.gml",None,"100003608428288","antonio.anzoateguifabbri"),
        ("RenatoFabbri03032013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri11072013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri18042013.gml",None,"781909429","renato.fabbri"),
        ]
for fnames in fnames_[1:]:
   aa=S.fb.triplifyGML(dpath=dpath,
                    fname=fnames[0],
                    fnamei=None,
                    fpath=fpath,
                    scriptpath=scriptpath,
                    uid=fnames[2],
                    sid=fnames[3],
                    fb_link=None,
                    ego=True,
                    umbrella_dir=umbrella_dir)


