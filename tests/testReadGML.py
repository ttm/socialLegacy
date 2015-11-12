import social as S, percolation as P, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(S.utils)
importlib.reload(pe)
#dreload(S)
os.environ["PATH"]=ENV

fg=S.fb.GDFgraph() # graph should be on fg.G
fg2=S.fb.readGDF() # graph should be on fg.G

