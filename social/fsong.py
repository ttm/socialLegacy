class FSong:
    """Create song from undirected (friendship) network"""
    def __init__(self, network):
        self.network=network
        self.makePartitions()
        self.makeImages()
        self.makeSong()
    def makePartitions(self):
        """Make partitions with gmane help.
        """
        pass
    def makeImages(self):
        """Make spiral images in sectors and steps.
        """
        pass
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
        """Use pymovie to render (visual+audio)+overlays.
        """
        pass

