import networkx as x
def makeRetweetNetwork(tweets):
    """Receives tweets, returns directed retweet networks.
    
    Without and with isolated nodes.
    """
    G=x.DiGraph()
    G_=x.DiGraph()
    for tweet in tweets:
        text=tweet["text"]
        us=tweet["user"]["screen_name"]
        if text.startswith("RT @"):
            prev_us=text.split(":")[0].split("@")[1]
            #print(us,prev_us,text)
            if G.has_edge(prev_us,us):
                G[prev_us][us]["weight"]+=1
                G_[prev_us][us]["weight"]+=1
            else:
                G.add_edge(prev_us, us, weight=1.)
                G_.add_edge(prev_us, us, weight=1.)
        if us not in G_.nodes():
            G_.add_node(us)
    return G,G_


class GDFgraph:
    """Read GDF graph into networkX"""
    def __init__(self,filename="../data/RenatoFabbri06022014.gdf"):
        with open(filename,"r") as f:
            self.data=f.read()
        self.lines=self.data.split("\n")
        columns=self.lines[0].split(">")[1].split(",")
        column_names=[i.split(" ")[0] for i in columns]
        data_friends={cn:[] for cn in column_names}
        for line in self.lines[1:]:
            if not line:
                break
            if ">" in line:
                columns=line.split(">")[1].split(",")
                column_names2=[i.split(" ")[0] for i in columns]
                data_friendships={cn:[] for cn in column_names2}
                continue
            fields=line.split(",")
            if "column_names2" not in locals():
                for i, field in enumerate(fields):
                    if field.isdigit(): field=int(field)
                    data_friends[column_names[i]].append(field)
            else:
                for i, field in enumerate(fields):
                    if field.isdigit(): field=int(field)
                    data_friendships[column_names2[i]].append(field)
        self.data_friendships=data_friendships
        self.data_friends=data_friends
        self.n_friends=len(data_friends[column_names[0]])
        self.n_friendships=len(data_friendships[column_names2[0]])
        self.makeNetwork()
    def makeNetwork(self):
        """Makes graph object from .gdf loaded data"""
        if "weight" in self.data_friendships.keys():
            self.G=G=x.DiGraph()
        else:
            self.G=G=x.Graph()
        F=self.data_friends
        for friendn in range(self.n_friends):
            if "posts" in F.keys():
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             posts=F["posts"][friendn])
            elif "agerank" in F.keys():
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             gender=F["sex"][friendn],
                             locale=F["locale"][friendn], 
                             agerank=F["agerank"][friendn])
            else:
                G.add_node(F["name"][friendn],
                             label=F["label"][friendn],
                             gender=F["sex"][friendn],
                             locale=F["locale"][friendn])
        F=self.data_friendships
        for friendshipn in range(self.n_friendships):
            if "weight" in F.keys():
                G.add_edge(F["node1"][friendshipn],F["node2"][friendshipn],weight=F["weight"][friendshipn])
            else:
                G.add_edge(F["node1"][friendshipn],F["node2"][friendshipn])
