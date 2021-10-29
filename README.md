# FastAPI-Panel
A minimum reproducible repository for embedding panel in FastAPI

1. Clone the repository (git clone https://github.com/t-houssian/FastAPI-Panel.git)
2. Install the needed libraries
  `pip install "fastapi[all]"`
  `pip install panel`
3. Set the evniroment variable BOKEH_ALLOW_WS_ORIGIN=127.0.0.1:8000 (or whatever your local host is)
  If using a conda environment then use `conda env config vars set BOKEH_ALLOW_WS_ORIGIN=127.0.0.1:8000`
4. Run the app using `uvicorn main:app --reload`
5. Open the app at `http://127.0.0.1:8000/`

That's it! You can change, modify, or add to the code in any way you'd like.

## Multiple Apps
This is just a basic single app example. To run multiple apps you will need to do the following:
1. Create a new file in your panelApps directory (ex. `app2.py`) and add your new app code.
2. Create another pn_app file in your panelApps directory (ex. `pn_app2.py`) That might look something like this:
```
import panel as pn

from .app2 import SineWave2

def createApp2(doc):
    sw = SineWave2()
    row = pn.Row(sw.param, sw.plot)
    return row.server_doc(doc)
```
3. Create a new html template (ex. app2.html) with the same contents as base.html
4. Import your new app in main.py `from panelApps.pn_app import createApp2`
5. Add your new app to the dictionary in bk_worker() Server
```
{'/app': createApp, '/app2': createApp2}
```
7. Add a new async function to rout your new app (The bottom of `main.py` should look something like this now):
```
@app.get("/")
async def bkapp_page(request: Request):
    script = server_document('http://127.0.0.1:5000/app')
    return templates.TemplateResponse("base.html", {"request": request, "script": script})
    
@app.get("/app2")
async def bkapp_page2(request: Request):
    script = server_document('http://127.0.0.1:5000/app2')
    return templates.TemplateResponse("app2.html", {"request": request, "script": script})

def bk_worker():
    server = Server({'/app': createApp, '/app2': createApp2},
        port=5000, io_loop=IOLoop(), 
        allow_websocket_origin=["*"])

    server.start()
    server.io_loop.start()

th = Thread(target=bk_worker)
th.daemon = True
th.start()
```
