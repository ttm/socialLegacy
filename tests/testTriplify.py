import social as S, os
ENV=os.environ["PATH"]
import  importlib
from IPython.lib.deepreload import reload as dreload
importlib.reload(S.triplification.participaTriplification)
#dreload(g,exclude="pytz")
dreload(S.triplification,exclude="rdflib")

trip=S.triplification.ParticipaTriplification()












