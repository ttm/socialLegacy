import gizeh
import moviepy.editor as mpy

W=128
def make_frame(t):
    surface = gizeh.Surface(128,128) # width, height
    radius = W*(1+ (t*(2-t))**2 )/6 # the radius varies over time
    circle = gizeh.circle(radius, xy = (64,64), fill=(1,0,0))
    circle.draw(surface)
    return surface.get_npimage() # returns a 8-bit RGB array

clip = mpy.VideoClip(make_frame, duration=2) # 2 seconds
clip.write_gif("circle.gif",fps=15)
