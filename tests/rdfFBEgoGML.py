import social as S, percolation as P, os
import  importlib
#importlib.reload(P.rdf)
importlib.reload(S)
importlib.reload(S.fb)
importlib.reload(S.fb.read)
importlib.reload(S.fb.gml2rdf)
c=P.utils.check
umbrella_dir="fbEgoGML/"
fpath="./publishing/fb4/"
dpath="../data/fb/gml/"
scriptpath=os.path.realpath(__file__)
fnames_=[
        ("AntonioAnzoategui18022013_182134.gml",None,"100003608428288","antonio.anzoateguifabbri"),
        ("BrunoMialich31012013_2126.gml",None,"10000045475708","bruno.mialich"),
        ("CalebLuporini13042013.gml",None,"1110305437","calebml"),
        ("CalebLuporini19022013.gml",None,"1110305437","calebml"),
        ("CamilaBatista23022014.gml",None,"100001707143512","camila.batista.3382"),
        ("DanielPenalva18022013.gml",None,"100000077490764","barthor.la.zule"),
        ("GabiThume19022013_0440.gml",None,"100002011676407","gabithume"),
        ("GrahamForrest28012013.gml",None,0,0),
        ("LailaManuelle17012013_0258.gml",None,"1713144485","laila.manuelle"),
        ("LarissaAnzoategui20022013_0207.gml",None,"1760577842","larissa.chogui"),
        ("LuisCirne07032013.gml",None,"717903828","lufcirne"),
        ("MariliaMelloPisani10042013_0255.gml",None,"100000812625301","marilia.pisani"),
        ("Mirtes16052013.gml",None,0,0),
        ("PedroPauloRocha10032013.gml",None,"836944624","dpedropaulorocha"),
        ("PeterForrest28012013_1602.gml",None,"770029747","peter.forrest.18"), # ateh aqui ok
        ("RafaelReinehr09042013_1148.gml",None,"814059950","reinehr"), #gml better
        ("RamiroGiroldo20022013_0149.gml",None,"100001810878626","ramiro.giroldo"),
        ("RenatoFabbri03032013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri11072013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri18042013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri20012013.gml",None,"781909429","renato.fabbri"),
        ("RenatoFabbri29112012_0521.gml",None,"781909429","renato.fabbri"),
        ("RicardoFabbri18022013_2257.gml",None,"1011765","ricardofabbri"),
        ("RitaWu08042013.gml",None,"100009639240215",0),
        ("RonaldCosta12062013.gml",None,"1457302032","scherolt"),
        ("ThaisTeixeira19022013_062820.gml",None,"100001089120349","thais.t.fabbri"),
        ("VilsonVieira18022013.gml",None,"529899682","aut0mata"),
        ("ViniciusSampaio18022013_2050.gml",None,"529899682","sampaio.vinicius"),
        ]
c("largou")
for fnames in fnames_[22:]:
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


