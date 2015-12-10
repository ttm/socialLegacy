import social as S, percolation as P, os
import  importlib
importlib.reload(P.rdf)
importlib.reload(S.fb)
importlib.reload(S.fb.gdf2rdf)
importlib.reload(S.fb.gdf2rdf)
c=P.utils.check
fnames_=[("AdornoNaoEhEnfeite29032013.gdf","AdornoNaoEhEnfeite29032013_interacoes.gdf","265217103529531",0,"https://www.facebook.com/groups/265217103529531/permalink/525654127485826/"),
("PartidoPirata23032013.gdf","PartidoPirata23032013_interactions.gdf",0,"partidopiratabrasil","https://www.facebook.com/groups/partidopiratabrasil/permalink/10151409024509317/"),
("DemocraciaPura06042013.gdf","DemocraciaPura06042013_interactions.gdf",0,"democraciapura","https://www.facebook.com/groups/democraciapura/permalink/310907215704321/"),
("ComputerArt10032013.gdf","ComputerArt10032013_interactions.gdf",0,"computerart","https://www.facebook.com/groups/computerart/permalink/259389137529870/"),
("RedeTranzmidias02032013.gdf","RedeTranzmidias02032013_interactions.gdf","318333384951196",0,"https://www.facebook.com/groups/318333384951196/permalink/346658712118663/"),
("AtivistasDaInclusaoDigital09032013.gdf","AtivistasDaInclusaoDigital09032013_interactions.gdf","423602557691243",0,"https://www.facebook.com/groups/423602557691243/permalink/525201037531394/"),
("Coolmeia06032013.gdf","Coolmeia06032013_interacoes.gdf", 0,"coolmeia",["https://www.facebook.com/groups/coolmeia/permalink/380091142098291/","https://www.facebook.com/groups/coolmeia/permalink/489757754464962/"]),
("Economia14042013.gdf","Economia14042013_interactions.gdf",0,"economa1","https://www.facebook.com/groups/economa1/permalink/586007714743535/"),
("DemocraciaDiretaJa14032013.gdf","DemocraciaDiretaJa14032013_interacoes.gdf",0,"ddjbrasil","https://www.facebook.com/groups/ddjbrasil/permalink/347023325397298/"),
("EconomiaCriativaDigital03032013.gdf","EconomiaCriativaDigital03032013_interactions.gdf",0,"economiacriativadigital","https://www.facebook.com/groups/economiacriativadigital/permalink/438313682916103/"),
("PoliticasCulturasBrasileiras08032013.gdf","PoliticasCulturasBrasileiras08032013_interacoes.gdf",0,"pcult","https://www.facebook.com/groups/pcult/permalink/519626544747423/"),
("Auricultura10042013.gdf","Auricultura10042013_interactions.gdf","373029202732392",0,0),
("CienciasComFronteiras29032013.gdf","CienciasComFronteiras29032013_interacoes.gdf",0,"contraaexclusao","https://www.facebook.com/groups/contraaexclusao/permalink/269103356558439/"),
("LivingBridgesPlanet29032013.gdf","LivingBridgesPlanet29032013_interactions.gdf",0,"livingbridgesplanet","https://www.facebook.com/groups/livingbridgesplanet/permalink/352950408144951/"),
("MobilizacoesCulturaisInteriorSP13032013.gdf","MobilizacoesCulturaisInteriorSP13032013_interacoes.gdf","131639147005593",0,"https://www.facebook.com/groups/131639147005593/permalink/144204529082388/"),
("PracaPopular16032013.gdf","PracaPopular16032013_interactions.gdf","215924991863921",0,"https://www.facebook.com/groups/215924991863921/permalink/319279541528465/"),
("SolidarityEconomy12042013.gdf","SolidarityEconomy12042013_interactions.gdf","9149038282",0,"https://www.facebook.com/groups/9149038282/permalink/10151461945623283/"),
("StudyGroupSNA05042013.gdf","StudyGroupSNA05042013_interactions.gdf","140630009439814",0,"https://www.facebook.com/groups/140630009439814/permalink/151470598355755/"),
("THackDay26032013.gdf","THackDay26032013_interacoes.gdf",0,"thackday",0)]



dpath="../data/fb/gdf/"
fpath="./publishing/fb2/"
umbrella_dir="fbGroups/"
scriptpath=os.path.realpath(__file__)
for fnames in fnames_:
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



