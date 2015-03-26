import social as S, os, gmane as g, numpy as n, networkx as x, pylab as p
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(S.utils)
#dreload(S)
os.environ["PATH"]=ENV

G=S.GDFgraph().G # graph should be on fg.G

class NetworkMeasures:
    pass
nm=NetworkMeasures()
nm.degrees=G.degree()
nm.nodes_= sorted(G.nodes(), key=lambda x : nm.degrees[x])
nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
nm.edges=     G.edges(data=True)
nm.E=G.number_of_edges()
nm.N=G.number_of_nodes()
np=g.NetworkPartitioning(nm,10,metric="g")

ri=100
rf=4
nturns=3
ii=n.linspace(0,3*2*n.pi,nm.N)
rr=n.linspace(ri,rf,nm.N)
xi=(rr*n.cos(ii))[::-1]
yi=(rr*n.sin(ii))[::-1]
# plota G com xi e yi dos mais conectados aos menos
A=x.to_agraph(G)
#A.graph_attr["size"]="9.5,12"
#A.graph_attr["size"]="10,7.5\!"
#A.graph_attr["dpi"]="200"
#A.graph_attr["viewport"]="100,100,2,450,300"
A.graph_attr["viewport"]="500,500,.03"
#A.graph_attr["bb"]="0,0,10,70"
nodes=A.nodes()
cm=p.cm.Reds(range(2**10)) # color table
clustering=x.clustering(G)
for node in nodes:
    n_=A.get_node(node)
    pos="{},{}".format(xi[nm.nodes_.index(node)],yi[nm.nodes_.index(node)])
    n_.attr["pos"]=pos
    n_.attr["pin"]=True
    color='#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
    n_.attr['fillcolor']= color

    n_.attr['fixedsize']=True
    n_.attr['width']=  abs(.1*(nm.degrees[n_]+  .5))
    n_.attr['height']= abs(.1*(nm.degrees[n_]+.5))
    n_.attr["label"]=""
edges=A.edges()
for e in edges:
    e.attr['penwidth']=3.4
    e.attr["arrowsize"]=1.5
    e.attr["arrowhead"]="lteeoldiamond"
    e.attr["style"]=""



base_dir="animation/"
os.system("mkdir {}".format(base_dir))
os.system("rm {}/*".format(base_dir))
A.draw("{}ff.png".format(base_dir),prog="neato")

A.node_attr['style']='filled'
for node in nodes:
    n_=A.get_node(node)
    pos="{},{}".format(xi[nm.nodes_.index(node)],yi[nm.nodes_.index(node)])
    n_.attr["pos"]=pos
    n_.attr["pin"]=True
    color='#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
    n_.attr['fillcolor']= color

    n_.attr['fixedsize']=True
    n_.attr['width']=  abs(.1*(nm.degrees[n_]+  .5))
    n_.attr['height']= abs(.1*(nm.degrees[n_]+.5))
    n_.attr["label"]=""
edges=A.edges()
for e in edges:
    e.attr['penwidth']=3.4
    e.attr["arrowsize"]=1.5
    e.attr["arrowhead"]="lteeoldiamond"
    e.attr["style"]=""



A.draw("{}ff2.png".format(base_dir),prog="neato")
# todo mundo invisivel
# quem estiver em cada setor, visivel
# as arestas que estiverem entre vertices visiveis, fica visivel

#A.edge_attr["style"]="invis"
#A.node_attr["style"]="invis"
for node in nodes:
    n_=A.get_node(node)
    pos="{},{}".format(xi[::-1][nm.nodes_.index(node)],yi[::-1][nm.nodes_.index(node)])
    n_.attr["pos"]=pos
    n_.attr["pin"]=True
    color='#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
    n_.attr['fillcolor']= color

    n_.attr['fixedsize']=True
    n_.attr['width']=  abs(.1*(nm.degrees[n_]+  .5))
    n_.attr['height']= abs(.1*(nm.degrees[n_]+.5))
    n_.attr["label"]=""
    if node not in np.sectorialized_agents__[0]:
        n_.attr["style"]="invis"
edges=A.edges()
for e in edges:
    e.attr['penwidth']=3.4
    e.attr["arrowsize"]=1.5
    e.attr["arrowhead"]="lteeoldiamond"
    if sum([i in np.sectorialized_agents__[0] for i in (e[0],e[1])])==2:
        e.attr["style"]=""
    else:
        e.attr["style"]="invis"

A.draw("{}ff3.png".format(base_dir),prog="neato")

#A.edge_attr["style"]="invis"
A.node_attr['style']='filled'
#A.node_attr["style"]="invis"
for node in nodes:
    n_=A.get_node(node)
    pos="{},{}".format(xi[::-1][nm.nodes_.index(node)],yi[::-1][nm.nodes_.index(node)])
    n_.attr["pos"]=pos
    n_.attr["pin"]=True
    color='#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
    n_.attr['fillcolor']= color

    n_.attr['fixedsize']=True
    n_.attr['width']=  abs(.1*(nm.degrees[n_]+  .5))
    n_.attr['height']= abs(.1*(nm.degrees[n_]+.5))
    n_.attr["label"]=""
    if node not in np.sectorialized_agents__[1]:
        n_.attr["style"]="invis"
    else:
        n_.attr["style"]="filled"
edges=A.edges()
for e in edges:
    e.attr['penwidth']=3.4
    e.attr["arrowsize"]=1.5
    e.attr["arrowhead"]="lteeoldiamond"
    if sum([i in np.sectorialized_agents__[1] for i in (e[0],e[1])])==2:
        e.attr["style"]=""
    else:
        e.attr["style"]="invis"

A.draw("{}ff4.png".format(base_dir),prog="neato")

#A.edge_attr["style"]="invis"
A.node_attr['style']='filled'
#A.node_attr["style"]="invis"
for node in nodes:
    n_=A.get_node(node)
    pos="{},{}".format(xi[::-1][nm.nodes_.index(node)],yi[::-1][nm.nodes_.index(node)])
    n_.attr["pos"]=pos
    n_.attr["pin"]=True
    color='#%02x%02x%02x' % tuple([255*i for i in cm[int(clustering[n_]*255)][:-1]])
    n_.attr['fillcolor']= color

    n_.attr['fixedsize']=True
    n_.attr['width']=  abs(.1*(nm.degrees[n_]+  .5))
    n_.attr['height']= abs(.1*(nm.degrees[n_]+.5))
    n_.attr["label"]=""
    if node not in np.sectorialized_agents__[2]:
        n_.attr["style"]="invis"
    else:
        n_.attr["style"]="filled"
edges=A.edges()
for e in edges:
    e.attr['penwidth']=3.4
    e.attr["arrowsize"]=1.5
    e.attr["arrowhead"]="lteeoldiamond"


    if sum([i in np.sectorialized_agents__[2] for i in (e[0],e[1])])==2:
        e.attr["style"]=""
    else:
        e.attr["style"]="invis"


A.draw("{}ff5.png".format(base_dir),prog="neato")




# draw each sector in different imgs.
# draw each node in a different img from lower degrees on

# draw nodes from each gender
# draw nodes from each location

# start coloring and moving nodes around

# start to make polifonic rithms with nodes

#la=S.Layout(G)
#
#S.Animate(G)

