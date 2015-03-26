==================================================================
Social participation data analysis and exploitation
==================================================================

This project gathers social data and routines for analysis and exploitation. At the most fundamental level, social participation linked data is accessed and analyzed. Public data, such as provided by the Gmane database or donated profiles from private networks (e.g. Facebook), or even gathered by Twitter, is incorporated as RDF in the Social Graph considered. Observance of stability and the synthesis of audiovisual artifacts eases observation, probing and exploitation.

Usage example
=================
Download messages from one GMANE list:

.. code:: python

    import social as S

    # put facebook user and password in ~/.social/fb/profile
    # or login on the browser window that will appear
    # or input login as arguments:
    sb=S.ScrapyBrowser()
    # input user id and returns the friend ids (and names...)
    friends=sb.getFriends()

    # To load GDF file:
    fg=S.GDFgraph("../data/RenatoFabbri06022014.gdf") # graph should be on fg.G
    # To make an abstract animtion with it:
    song=S.FSong(fg.G,"fsong/",True,True,False,True)
    # Check mixedVideo.webm

    # more ***in construction***

    ##########################################
    # SKETCH. This is not the toolbox.

    #S.download() # download ontologies and data

    #S.generalStats() # print number of triples, individuals, etc.

    #data=S.data()

    #d1=S.makeBasicDatastructures(data["participa"])
    #d2=S.makeBasicDatastructures(data["aa"])
    #d3=S.makeBasicDatastructures(data["cd"])

    #S.Analyze()

    # use the gmane python package to analyse network structure

    # Enjoy!
