import panel as pn

from .app1 import SineWave

def createApp(doc):
    sw = SineWave()
    row = pn.Row(sw.param, sw.plot)
    return row.server_doc(doc)