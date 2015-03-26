import gmane as g, networkx as x, pylab as p, numpy as n, os
import moviepy.editor as mpy, mass as m
UT=m.Utils()
bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()
sy.adsrSetup(A=20,D=20,R=10)

class FSong:
    """Create song from undirected (friendship) network
    """
    def __init__(self, network,basedir="fsong/",clean=False,render_images=False):
        os.system("mkdir {}".format(basedir))
        if clean:
            os.system("rm {}*".format(basedir))
        self.basedir=basedir
        self.network=network
        self.makePartitions()
        if render_images:
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
            self.plotGraph("plain",   sector,"sector{:02}.png".format(i))
            self.plotGraph("reversed",sector,"sector{:02}R.png".format(i))
            self.plotGraph("plain", n.setdiff1d(agents,sector),"sector{:02}N.png".format(i))
            self.plotGraph("reversed",n.setdiff1d(agents,sector),"sector{:02}RN.png".format(i))
        for i, node in enumerate(self.nm.nodes_):
            self.plotGraph("plain",   [node],"lonely{:09}.png".format(i))
            self.plotGraph("reversed",[node],"lonely{:09}R.png".format(i))
            self.plotGraph("plain",   self.nm.nodes_[:i],"stair{:09}.png".format(i))
            self.plotGraph("reversed",self.nm.nodes_[:i],"stair{:09}R.png".format(i))
        # plotar novamente usando somente vertices e depois somente arestas

    def plotGraph(self,mode="plain",nodes=None,filename="tgraph.png"):
        """Plot graph with nodes (iterable) into filename
        """
        if nodes==None:
            nodes=self.nodes
        else:
            nodes=[i for i in self.nodes if i in nodes]
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
        self.files=os.listdir(self.basedir)
        self.stairs=[i for i in self.files if ("stair" in i) and ("R" in i)]
        self.sectors=[i for i in self.files if "sector" in i]
        self.stairs.sort()
        self.sectors.sort()
        filenames=[self.basedir+i for i in self.sectors[:4]]
        self.iS=mpy.ImageSequenceClip(filenames,durations=[1.5,2.5,.5,1.5])
        # Clip with three first images3
        # each sector a sound
        # sweep from periphery to center
        # all, all inverted
        # sectors with inversions
    def makeAudibleSong(self):
        """Use mass to render wav soundtrack.
        """
        sound=n.hstack((sy.render(220,d=1.5),
                        sy.render(220*(2**(7/12)),d=2.5),
                        sy.render(220*(2**(-5/12)),d=.5),
                        sy.render(220*(2**(0/12)),d=1.5),
                        ))
        UT.write(sound,"sound.wav")
    def Animation(self):
        """Use pymovie to render (visual+audio)+text overlays.
        """
        aclip=mpy.AudioFileClip("sound.wav")
        self.iS=self.iS.set_audio(aclip)
        self.iS.write_videofile("aquiLL.webm",15,audio=True)
