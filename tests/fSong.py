import social as S, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
#importlib.reload(S.utils)
importlib.reload(S.fsong)
#dreload(S)
os.environ["PATH"]=ENV

fg=S.GDFgraph() # graph should be on fg.G

#song=S.FSong(fg.G,"fsongNew/",True,True)
song=S.FSong(fg.G,"fsongNew2/",True,True,False,True)


