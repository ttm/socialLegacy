import social as S, percolation as P, os
import  importlib
importlib.reload(P.rdf)
importlib.reload(S.fb)
importlib.reload(S.fb.gdf2rdf)
c=P.utils.check
umbrella_dir="fbEgo/"
fpath="./publishing/fb3/"
scriptpath=os.path.realpath(__file__)
fnames_=[
        ("RenatoFabbri19112014.gdf",None,"781909429","renato.fabbri"),
        ("PedroPauloRocha10032013.gdf",None,"836944624","dpedropaulorocha"),
        ("MarceloSaldanha19112014.gdf",None,"100000028547604","IBEBrasil"),
("MariliaPisani06052014.gdf",None,"100000812625301","marilia.pisani"),
("RafaelReinehr09042013.gdf",None,"814059950","reinehr"),
("VJPixel23052014.gdf",      None,"614664810",None),
("MassimoCanevacci19062013.gdf",     None,"1327838394","massimo.canevacci"),
        ]
dpath="../data/fb/gdf/ego/"
ff=[(fnames_,dpath)]
fnames_=[
        ("AnaCelia18032014.gdf",None,"1450596979",0),
        ("FabiBorges08032014.gdf",None,"598339469","antennarush"),
        ("RicardoPoppi18032014.gdf",None,"100000099352333","ricardopoppi"),
        ("ElenaGarnelo04032014.gdf",None,"1361932044","elena.garnelo"),
        ("GeorgeSanders08032014.gdf",None,"1347483608","george.sander"),
        ("GraziMachado18032014.gdf",None,"1847090892","GrazielleMachado"),
        ("RenatoFabbri19032014.gdf",None,"781909429","renato.fabbri")
        ]
dpath="../data/fb/gdf/posAvlab/"
ff+=[(fnames_,dpath)]
fnames_=[
("CalebLuporini25022014.gdf",     None,"1110305437","calebml"),
("DanielGonzales23022014.gdf",    None,"100002080034739","daniel.gonzalezxavier"),
("JoaoMekitarian23022014.gdf",    None,"100002080034739","joaopaulo.mekitarian"),
("MariliaPisani25022014.gdf",     None,"100000812625301","marilia.pisani"),
("RenatoFabbri22022014.gdf",      None,"781909429","renato.fabbri"),
("FelipeBrait23022014.gdf",       None,"1420435978","felipe.brait"),
("JulianaSouza23022014.gdf",      None,"520322516","juliana.desouza2"),
("NatachaRena22022014.gdf",       None,"665770837","natacha.rena"),
("SarahLuporini25022014.gdf",     None,"1528620900","sarah.cura"),
("CamilaBatista23022014.gdf",     None,"100001707143512","camila.batista.3382"),
("KarinaGomes22022014.gdf",       None,"100000176551181","karina.gomes.71"),
("OrlandoCoelho22022014.gdf",     None,"1060234340","orlando.coelho.98"),
("SatoBrasil25022014.gdf",        None,"1060234340","sato.dobrasil"),
("CarlosDiego25022014.gdf",       None,"689266676","cdiegosr"),
("PalomaKliss25022014.gdf",       None,"100008456088732",0),
("CristinaMekitarian23022014.gdf",None,"1771691370","cristina.mekitarian"),
("MarcelaLucatelli25022014.gdf",  None,"520656478","justinamoira"),
("PedroRocha25022014.gdf",None,"836944624","dpedropaulorocha"),
("JoaoMeirelles25022014.gdf",     None,"1194439813","joao.meirelles.10"),
("LucasOliveira26022014.gdf",     None,"1060987164",0),
]
#("FideoFuturalista22022014.gdf",  None,0,0),
dpath="../data/fb/gdf/avlab/"
ff+=[(fnames_,dpath)]

for fnames_,dpath in ff[:1]:
    for fnames in fnames_[-1:]:
        S.fb.triplifyGDF(dpath=dpath,
                         fname=fnames[0],
                         fnamei=None,
                         fpath=fpath,
                         scriptpath=scriptpath,
                         uid=fnames[2],
                         sid=fnames[3],
                         fb_link=None,
                         ego=True,
                         umbrella_dir=umbrella_dir)

