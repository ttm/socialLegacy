import matplotlib.animation as animation
import numpy as np
from pylab import *


dpi = 200

def ani_frame():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    im = ax.imshow(1+100*rand(200,200),cmap='gray',interpolation='nearest')
    im.set_clim([0,1])
    fig.set_size_inches([5,5])

    tight_layout()

    def update_img(n):
        tmp = 1+100*rand(200,200)
        im.set_data(tmp)
        return im
    #legend(loc=0)
    ani = animation.FuncAnimation(fig,update_img,200,interval=30)
    writer = animation.writers['avconv'](fps=30)
    ani.save('demo.mp4',writer=writer,dpi=dpi)
    return ani
