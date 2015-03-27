__all__=["ParticipaTriplification"]
import psycopg2, rdflib as r, sys, urllib, re
class ParticipaTriplification:
    def __init__(self,dbname="newdb",username="r",separator="/",filename="participaTriplestore",render=True,write_files=True,compute_networks=True,compute_bows=False):
        """Reads PostgreSQL Participabr/Noosfero database and writes them as RDF.
        """
        self.connectDatabase(dbname,username)
        self.readTables() #creates D and N
        self.initNamespaces() # creates P
        self.startGraph()
        self.auxFunctions()

        self.separator=separator
        self.filename=filename
        self.write_files=write_files
        self.render=render
        self.compute_networks=compute_networks
        self.compute_bows=compute_bows

        if render:
            self.triplifyAll()
        if write_files:
            self.writeGraph()

    def triplifyAll(self):
        self.triplifyPortalInfo()
        self.triplifyProfiles()
        self.triplifyComments()
        self.triplifyFriendships()
        self.triplifyVotes()
        self.triplifyTags()
        self.triplifyOverallStructures()
    def connectDatabase(self,dbname="newdb",username="r"):
        self.con = psycopg2.connect(database=dbname, user=username)
        self.cur = self.con.cursor()
    def readTables(self):
        """Retrieves data (D) and names (N) from relational tables.
        """
        class D: pass
        cur=self.cur
        cur.execute('SELECT * FROM users')
        D.users = cur.fetchall()
        cur.execute('SELECT * FROM profiles')
        D.profiles = cur.fetchall()
        cur.execute('SELECT * FROM articles')
        D.articles = cur.fetchall()
        cur.execute('SELECT * FROM comments')
        D.comments = cur.fetchall()
        cur.execute('SELECT * FROM friendships')
        D.friendships= cur.fetchall()
        cur.execute('SELECT * FROM votes')
        D.votes= cur.fetchall()
        cur.execute('SELECT * FROM tags')
        D.tags= cur.fetchall()
        cur.execute('SELECT * FROM taggings')
        D.taggings= cur.fetchall()
        self.D=D

        class N: pass
        cur.execute("select column_name from information_schema.columns where table_name='users';")
        UN=cur.fetchall()
        N.UN=[i[0] for i in UN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='profiles';")
        PN=cur.fetchall()
        N.PN=[i[0] for i in PN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='articles';")
        AN=cur.fetchall()
        N.AN=[i[0] for i in AN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='comments';")
        CN=cur.fetchall()
        N.CN=[i[0] for i in CN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='friendships';")
        FRN=cur.fetchall()
        N.FRN=[i[0] for i in FRN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='votes';")
        VN=cur.fetchall()
        N.VN=[i[0] for i in VN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='tags';")
        TN=cur.fetchall()
        N.TN=[i[0] for i in TN[::-1]]
        cur.execute("select column_name from information_schema.columns where table_name='taggings';")
        TTN=cur.fetchall()
        N.TTN=[i[0] for i in TTN[::-1]]
        self.N=N

    def initNamespaces(self):
        class P: pass
        P.rdf = r.namespace.RDF
        P.foaf = r.namespace.FOAF
        P.xsd = r.namespace.XSD
        P.opa = r.Namespace("http://purl.org/socialparticipation/opa/")
        P.ops = r.Namespace("http://purl.org/socialparticipation/ops/")
        P.wsg = r.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        P.dc2 = r.Namespace("http://purl.org/dc/elements/1.1/")
        P.dc = r.Namespace("http://purl.org/dc/terms/")
        P.sioc = r.Namespace("http://rdfs.org/sioc/ns#")
        P.tsioc = r.Namespace("http://rdfs.org/sioc/types#")
        P.skos = r.Namespace("http://www.w3.org/2004/02/skos/core#")
        P.schema = r.Namespace("http://schema.org/")
        P.part = r.Namespace("http://participa.br/") 
        self.P=P
    def startGraph(self):
        """Starts RDF graph and bing namespaces"""
        g = r.Graph()
        g.namespace_manager.bind("rdf", r.namespace.RDF)    
        g.namespace_manager.bind("foaf", r.namespace.FOAF)    
        g.namespace_manager.bind("xsd", r.namespace.XSD)    
        g.namespace_manager.bind("opa", "http://purl.org/socialparticipation/opa/")    
        g.namespace_manager.bind("ops", "http://purl.org/socialparticipation/ops/")    
        g.namespace_manager.bind("wsg", "http://www.w3.org/2003/01/geo/wgs84_pos#")    
        g.namespace_manager.bind("dc2", "http://purl.org/dc/elements/1.1/")    
        g.namespace_manager.bind("dc", "http://purl.org/dc/terms/")    
        g.namespace_manager.bind("sioc", "http://rdfs.org/sioc/ns#")    
        g.namespace_manager.bind("tsioc", "http://rdfs.org/sioc/types#")    
        g.namespace_manager.bind("schema", "http://schema.org/")
        g.namespace_manager.bind("part", "http://participa.br/")
        self.g=g
    def auxFunctions(self):
        TAG_RE = re.compile(r'<[^>]+>')
        class X:
            def remove_tags(text):
                return TAG_RE.sub('', text)
            def Qu(termo):
                user_id=pp[PN.index("user_id")]
                val=[i for i in users if i[0]==user_id][0][UN.index(termo)]
                return val
            def G(S,P,O):
                self.g.add((S,P,O))
            def L(data, datatype_=None):
                if datatype_:
                    return r.Literal(data, datatype=datatype_)
                else:
                    return r.Literal(data)
            def fparse(mstring):
                foo=[i for i in mstring.split("\n")[1:-1] if i]
                return dict([[j.strip().replace('"',"") for j in i.split(":")[1:]] for i in foo if  len(i.split(":"))==3])
            U=r.URIRef
            QQ=urllib.parse.quote
            def Q_(mstr):
                return QQ(pp[PN.index(mstr)])
            def Q(mstr):
                return pp[PN.index(mstr)]
            def QA(mstr):
                return aa[AN.index(mstr)]
            def QC(mstr):
                return cc[CN.index(mstr)]
            def QF(mstr):
                return fr[FRN.index(mstr)]
        self.X=X
    def triplifyPortalInfo(self):
        """Make triples with information about the portal.
        """
        uri=self.P.opa.ParticipationPortal+self.separator+"participabr"
        self.X.G(uri,self.P.rdf.type,self.P.opa.ParticipationPortal)
        self.X.G(uri,self.P.opa.description,self.X.L(DATA.portal_description,self.P.xsd.string))
        self.X.G(uri,self.P.opa.url,self.X.L("http://participa.br/",self.P.xsd.string))
    def triplifyOverallStructures(self):
        """Insert into RDF graph the textual and network structures.

        Ideally, one should be able to make bag of words related to
        each item (communities, users, posts, comments, tags, etc).
        Interaction and friendship networks should be made.
        Human networks mediated by co-ocurrance (time os posts,
        geographical locations, vocabulary, etc) should be addressed
        as well.
        """
        if self.compute_networks:
            self.computeNetworks()
        if self.compute_bows:
            self.computeBows()
    def computeBows(self):
        pass
    def computeNetworks(self):
        pass
    def triplifyProfiles(self):
        pass
    def triplifyComments(self):
        pass
    def triplifyFriendships(self):
        pass
    def triplifyVotes(self):
        pass
    def triplifyTags(self):
        pass
    def writeGraph(self):
        f=open("participaTriplestore.rdf","wb")
        f.write(self.g.serialize())
        f.close()
        f=open("participaTriplestore.ttl","wb")
        f.write(self.g.serialize(format="turtle"))
        f.close()
class DATA:
    portal_description="""
    O que é o dados.gov.br?

    O Portal Brasileiro de Dados Abertos é a ferramenta disponibilizada pelo governo para que todos possam encontrar e utilizar os dados e as informações públicas. O portal preza pela simplicidade e organização para que você possa encontrar facilmente os dados e informações que precisa. O portal também tem o objetivo de promover a interlocução entre atores da sociedade e com o governo para pensar a melhor utilização dos dados em prol de uma sociedade melhor.

    Quais dados estão disponíveis aqui?

    O portal tem o objetivo de disponibilizar todo e qualquer tipo de dado. Por exemplo, dados da saúde suplementar, do sistema de transporte, de segurança pública, indicadores de educação, gastos governamentais, processo eleitoral, etc.
    O portal funciona como um grande catálogo que facilita a busca e uso de dados publicados pelos órgãos do governo. Neste momento o portal disponibiliza o acesso à uma parcela dos dados publicados pelo governo. O plano estratégico prevê que nos próximos 3 anos o portal disponibilize acesso aos dados publicados por todos os órgãos do governo federal, além de dados das esferas estaduais e municipais.

    O que dados abertos tem a ver com você?

    O acesso a informação está previsto na Constituição Federal e na Declaração Universal dos Direitos Humanos. Dados Abertos é a publicação e disseminação dos dados e informações públicas na Internet, organizados de tal maneira que permita sua reutilização em aplicativos digitais desenvolvidos pela sociedade.

    Isso proporciona ao cidadão um melhor entendimento do governo, no acesso aos serviços públicos, no controle das contas públicas e na participação no planejamento e desenvolvimento das políticas públicas. Se interessou pelo tema? Saiba mais sobre Dados Abertos aqui !

    Por que estamos fazendo isso?

    Em 18 de novembro de 2011 foi sancionada a Lei de Acesso a Informação Pública (Lei 12.527/2011) que regula o acesso a dados e informações detidas pelo governo. Essa lei constitui um marco para a democratização da informação pública, e preconiza, dentre outros requisitos técnicos, que a informação solicitada pelo cidadão deve seguir critérios tecnológicos alinhados com as “3 leis de dados abertos”. Dentro desse contexto o Portal Brasileiro de Dados Abertos é a ferramenta construída pelo governo para centralizar a busca e o acesso dos dados e informações públicas.

    O Brasil como membro co-líder da Parceria de Governo Aberto, ou Open Government Partnership (OGP), tem este Portal como um de seus compromissos que foram formalizados no Plano de ação de governo aberto, lançado na OGP e referenciado pelo Decreto sem número de 15 de setembro de 2011.
    """
