import networkx as x
def readGML(filename="../data/RenatoFabbri06022014.gml"):
    gg=x.read_gml(filename)
    nodes=gg.nodes(data=True)
    nodes_=[i[1] for i in nodes]
    nodes__={}
    nkeys=nodes_[0].keys()
    for key in nkeys:
        if key == "id":
            nodes__["name"]=[]
#            nodes__["label"]=[]
            for node in nodes_:
                nodes__["name"]+=["user_{}".format(node[key])]
#                nodes__["label"]+=["user_{}".format(node[key])]
        else:
            nodes__[key]=[]
            for node in nodes_:
                nodes__[key]+=[node[key]]

    edges=gg.edges(data=True)
    edges_={"node1":[], "node2":[],"name":[]}
    i=1
    for edge in edges:
        u1="user_{}".format(edge[0])
        u2="user_{}".format(edge[1])
        edges_["node1"]+=[u1]
        edges_["node2"]+=[u2]
        i+=1
#    if edges[0][2]:
#        edges_=[i[2] for i in edges]
#        edges__={}
#        ekeys=edges_[0].keys()
#    for key in ekeys:
#       edges__[key]=[]
#       for edge in edges_:
#           edges__[key]+=[edge[key]]
   
    return {"relations": edges_,
            "individuals": nodes__}
    return gg
def readGDF(filename="../data/RenatoFabbri06022014.gdf"):
    """Made to work with gdf files from my own network and friends and groups"""
    with open(filename,"r") as f:
        data=f.read()
    lines=data.split("\n")
    columns=lines[0].split(">")[1].split(",")
    column_names=[i.split(" ")[0] for i in columns]
    data_friends={cn:[] for cn in column_names}
    for line in lines[1:]:
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
                if column_names[i] in ("name","groupid"): pass
                elif field.isdigit(): field=int(field)
                data_friends[column_names[i]].append(field)
        else:
            for i, field in enumerate(fields):
                if column_names2[i]=="name": pass
                elif field.isdigit(): field=int(field)
                data_friendships[column_names2[i]].append(field)
    return {"relations":data_friendships,
            "individuals":data_friends}

