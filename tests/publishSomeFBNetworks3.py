import social as S, percolation as P, os, re
import  importlib
importlib.reload(S.fb)
importlib.reload(P.rdf)
importlib.reload(P.utils)
c=P.utils.check
#fnames=("../data/Antonio.gdf",thata,ricardo,marilia,debora,rita,massimo,vilson,penalva,grupos)
#fnames="RenatoFabbri06022014.gdf","AntonioAnzoategui18022013huge_100003608428288_2013_02_18_21_34_f74ca978ec921548c0b7caf3287f2335.gml","RonaldCosta12062013.gml"

#    "LeiCulturaViva50.gdf", acho que é página
fnames=[
    ("AdornoNaoEhEnfeite.gdf","265217103529531",0,"https://www.facebook.com/groups/265217103529531/permalink/525654127485826/"), #ok
    ("DemocraciaPura06042013.gdf",0,"democraciapura","https://www.facebook.com/groups/democraciapura/permalink/310907215704321/"), #ok
    ("RedeTranzmidias.gdf","318333384951196",0,"https://www.facebook.com/groups/318333384951196/permalink/346658712118663/"), #ok
    ("AtivistasDaInclusaoDigital.gdf","423602557691243",0,"https://www.facebook.com/groups/423602557691243/permalink/525201037531394/"), #ok
    ("ComputerArt10032013.gdf",0,"computerart","https://www.facebook.com/groups/computerart/permalink/259389137529870/"), #ok
    ("CoolmeiaAmizades06032013.gdf", 0,"coolmeia","https://www.facebook.com/groups/coolmeia/permalink/489757754464962/"), #ok
    ("Economia14042013.gdf",0,"economa1","https://www.facebook.com/groups/economa1/permalink/586007714743535/"),
    ("PartidoPirata23032013.gdf",0,"partidopiratabrasil","https://www.facebook.com/groups/partidopiratabrasil/permalink/10151409024509317/"), #ok
    ("DemocraciaDiretaJa14032013.gdf",0,"ddjbrasil","https://www.facebook.com/groups/ddjbrasil/permalink/347023325397298/"),
    ("EconomiaCriativaDigital03032013.gdf",0,"economiacriativadigital","https://www.facebook.com/groups/economiacriativadigital/permalink/438313682916103/"),
    ("PoliticasCulturasBrasileiras08032013.gdf",0,"pcult","https://www.facebook.com/groups/pcult/permalink/519626544747423/"),
    ]
#fnames2=[("DanielPenalva18022013.gml","100006319395678","barthor.la.zule"),
#        ("CalebLuporini19022013.gml","1110305437","calebml"),
#        ("VilsonVieira18022013.gml","529899682","aut0mata"),
fnames2=[
        ("ThaisTeixeiraFabbri_huge_100001089120349_2013_02_19_06_28_20b14681423b224363cad7233f074f38.gml","100001089120349","thais.t.fabbri"),
        ("RitaWu08042013.gml","100009639240215",0),
        ("RicardoFabbri_huge_1011765_2013_02_18_22_57_04c1993168b2d37f24e2ed2838af151e.gml","1011765","ricardofabbri"),
        ("RenatoFabbri03032013.gml","781909429","renato.fabbri"),
        ("RafaelReinehr_huge_814059950_2013_04_09_11_48_df060d634d2332e8070b6a9f1fb58124.gml","814059950","reinehr"),
        ("PedroPauloRocha10032013.gml","836944624","dpedropaulorocha"),
        ("PeterForrest_770029747_2013_01_28_16_02_c35e1a1dd757fdc412883b9e9698d154.gml","770029747","peter.forrest.18"),
        ("MariliaMelloPisani_huge_100000812625301_2013_04_10_02_55_f5180b675e47066391deda07c3970ec2.gml","100000812625301","marilia.pisani"),
        ("LuisCirne07032013.gml","717903828","lufcirne"),
        ("LailaManuelle_1713144485_2013_01_17_02_58_7ef03eec79f843f1e6834acd13f077bf.gml","1713144485","laila.manuelle")]
fnames3=[
        ("LailaManuelle_1713144485_2013_01_17_02_58_7ef03eec79f843f1e6834acd13f077bf.gdf","1713144485","laila.manuelle"),
        ("RafaelReinehr_huge_814059950_2013_04_09_11_48_df060d634d2332e8070b6a9f1fb58124.gdf","814059950","reinehr"),
        ("PedroPauloRocha10032013.gdf","836944624","dpedropaulorocha"),
        ]
# para achar o id numerico, visito a página e procuro
# pela tag 5h60. O profile_owner tem o id correto.
# jah o id string nao consegui achar no caso da rita
fnames_=fnames+fnames2+fnames3
#fnames_=fnames2[7:-1]
#fnames_=fnames3[1:][::-1]
# achar as redes de interacoes, publicar todo mundo
# aos pares

tdir="../data/fb/{}/"
fpath="./publishing/fb2/"
scriptpath=os.path.realpath(__file__)
# idealmente todos os arquivos gdf e gml no data/fb/
for dataset in fnames_[:1]:
    fname=dataset[0]
    c(fname)
    if fname[-3:]=="gdf":
        fname_=tdir.format("gdf")+fname
        if len(dataset)==4:
            uid,sid,dlink=dataset[1:]
        else:
            uid,sid=dataset[1:]
            dlink=None
        S.fb.triplifyGDF(fname_,fpath,scriptpath,uid,sid,dlink)
        tnameF=re.findall("([a-zA-Z]*)\d*.gdf",fname)[0]
        tfiles=[i for i in os.listdir(tdir.format("gdf")) if (tnameF in i) and ("ntera" in i)]
        if len(tfiles)>2:
            c(tfiles)
        if len(tfiles):
            tfile=tfiles[0]
            fname_=tdir.format("gdf")+tfile
            S.fb.triplifyGDF(fname_,fpath,scriptpath,uid,sid,dlink)
    elif fname[-3:]=="gml":
        fname_=tdir.format("gml")+fname
        uid,sid=dataset[1:]
        S.fb.triplifyGML(fname_,fpath,scriptpath,uid,sid)
    else:
        c("file format not recognized")
eurl="http://200.144.255.210:8082/dsfoo"
path="./publishing/fb2/AdornoNaoEhEnfeite_fb/rdf/"
eurl="http://200.144.255.210:8082/dsfoo"
path2="./publishing/fb2/AdornoNaoEhEnfeite_interacoes_fb/rdf/"
