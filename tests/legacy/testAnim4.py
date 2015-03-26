# use mpy to read files from
#animation/ dir and make gifs
# and video clips with and without sound
import moviepy.editor as mpy, mass as m, numpy as n, os

tdir="animation/"
filenames=os.listdir(tdir)
filenames_=[tdir+i for i in filenames]
durations=[1,2,2,1,2]

ut=m.Utils()
bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()
sy.adsrSetup(A=20,D=20,R=10)
note1=sy.render(d=1)
note2=sy.render(400.,d=2)
sy.adsrSetup(A=20,D=20,R=1110)
note3=sy.tremoloEnvelope(sound=sy.render(400.,d=2))
sy.adsrSetup(A=20,D=20,R=10)
note4=sy.tremoloEnvelope(sound=sy.render(200.,d=1))
sy.adsrSetup(A=120,D=20,R=10)
note5=sy.tremoloEnvelope(sound=sy.render(200.,d=2))
audio=n.hstack([note1,note2,note3,note4,note5])
ut.write(audio,"sound.wav")


iS=mpy.ImageSequenceClip(filenames_,durations=durations)
#iS.set_audio("sound.wav")

audio_=n.vstack((audio,audio))
#aclip=mpy.AudioClip.AudioArrayClip(audio_,44100)
aclip=mpy.AudioFileClip("sound.wav")
iS2=iS.set_audio(aclip)
iS2.audio=aclip
iS2.write_videofile("aqui2.webm",15,audio=True)
