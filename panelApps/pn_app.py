import panel as pn

from .app1 import SineWave

def createApp():
    sw = SineWave()
    return pn.Row(sw.param, sw.plot).servable()