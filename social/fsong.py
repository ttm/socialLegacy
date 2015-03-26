import gmane as g, networkx as x, pylab as p, numpy as n, os
class FSong:
    """Create song from undirected (friendship) network
    """
    def __init__(self, network,basedir="fsong/",clean=True):
        os.system("mkdir {}".format(basedir))
        if clean:
            os.system("rm {}*".format(basedir))
        self.basedir=basedir
        self.network=network
        self.makePartitions()
        self.makeImages()
        self.makeSong()
    def makePartitions(self):
        """Make partitions with gmane help.
        """
        class NetworkMeasures:
            pass
        self.nm=nm=NetworkMeasures()
        nm.degrees=self.network.degree()
        nm.nodes_= sorted(self.network.nodes(), key=lambda x : nm.degrees[x])
        nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
        nm.edges=     self.network.edges(data=True)
        nm.E=self.network.number_of_edges()
        nm.N=self.network.number_of_nodes()
        self.np=g.NetworkPartitioning(nm,10,metric="g")
    def makeImages(self):
        """Make spiral images in sectors and steps.

        Plain, reversed,
        sectorialized, negative sectorialized
        outline, outline reversed, lonely
        only nodes, only edges, both
        """
        # make layout
        self.makeLayout()
        self.setAgraph()
        # make function that accepts a mode, a sector
        # and nodes and edges True and False
        self.plotGraph()
        self.plotGraph("reversed",filename="tgraphR")
        agents=n.concatenate(self.np.sectorialized_agents__)
        for i, sector in enumerate(self.np.sectorialized_agents__):
            self.plotGraph("plain",   sector,"sector{}.png".format(i))
            self.plotGraph("reversed",sector,"sector{}R.png".format(i))
            self.plotGraph("plain", n.setdiff1d(agents,sector),"sector{}N.png".format(i))
            self.plotGraph("reversed",n.setdiff1d(agents,sector),"sector{}RN.png".format(i))
        for i, node in enumerate(self.nodes):
            self.plotGraph("plain",   [node],"lonely{}.png".format(i))
            self.plotGraph("reversed",[node],"lonely{}R.png".format(i))
            self.plotGraph("plain",   self.nm.nodes_[:i],"stair{}.png".format(i))
            self.plotGraph("reversed",self.nm.nodes_[:i],"stair{}R.png".format(i))
        # plotar novamente usando somente vertices e depois somente arestas

    def plotGraph(self,mode="plain",nodes=None,filename="tgraph.png"):
        """Plot graph with nodes (iterable) into filename
        """
        if nodes==None:
            nodes=self.A.nodes()
        for node in self.nodes:
            n_=self.A.get_node(node)
            if mode=="plain":
                nmode=1
            else:
                nmode=-1
            pos="{},{}".format(self.xi[::nmode][self.nm.nodes_.index(node)],self.yi[::nmode][self.nm.nodes_.index(node)])
            n_.attr["pos"]=pos
            n_.attr["pin"]=True
            color='#%02x%02x%02x' % tuple([255*i for i in self.cm[int(self.clustering[n_]*255)][:-1]])
            n_.attr['fillcolor']= color
            n_.attr['fixedsize']=True
            n_.attr['width']=  abs(.1*(self.nm.degrees[n_]+  .5))
            n_.attr['height']= abs(.1*(self.nm.degrees[n_]+.5))
            n_.attr["label"]=""
            if node not in nodes:
                n_.attr["style"]="invis"
            else:
                n_.attr["style"]="filled"
        for e in self.edges:
            e.attr['penwidth']=3.4
            e.attr["arrowsize"]=1.5
            e.attr["arrowhead"]="lteeoldiamond"
            e.attr["style"]=""
            if sum([i in nodes for i in (e[0],e[1])])==2:
                e.attr["style"]=""
            else:
                e.attr["style"]="invis"
        tname="{}{}".format(self.basedir,filename)
        print(tname)
        self.A.draw(tname,prog="neato")

    def setAgraph(self):
        self.A=x.to_agraph(self.network)
        self.A.graph_attr["viewport"]="500,500,.03"
        self.edges=self.A.edges()
        self.nodes=self.A.nodes()
        self.cm=p.cm.Reds(range(2**10)) # color table
        self.clustering=x.clustering(self.network)
    def makeLayout(self):
        ri=4
        rf=100
        nturns=3
        ii=n.linspace(0,nturns*2*n.pi,self.nm.N)
        rr=n.linspace(ri,rf,self.nm.N)
        self.xi=(rr*n.cos(ii))
        self.yi=(rr*n.sin(ii))

    def makeSong(self):
        """Render abstract animation
        """
        self.makeVisualSong()
        self.makeAudibleSong()
        self.Animation()
    def makeVisualSong(self):
        """Return a sequence of images and durations.
        """
        pass
    def makeAudibleSong(self):
        """Use mass to render wav soundtrack.
        """
        pass
    def Animation(self):
        """Use pymovie to render (visual+audio)+text overlays.
        """
        pass

