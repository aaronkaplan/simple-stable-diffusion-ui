import uuid
import os
from fastapi import FastAPI, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


from sd import gen_image_768
import logger
from cache import Cache

app = FastAPI()
logger = logger.get_module_logger(__name__)


class Inputs(BaseModel):
    prompt: str
    image: bytes = File(...)


# to serve static files in fastapi
OUTDIR = os.environ.get('OUTPUTDIR', '/app/output')
app.mount("/sd/output", StaticFiles(directory=OUTDIR), name="output")

defaultprompt = """NASA austronaut chasing chicken on a chickenfarm on the moon,photorealistic,hasselblad,8k"""


# the cache to store all the prompts and image filenames
imgcache = Cache()


def generate_html_response(text: str, imagepath: str):
    htmlresponse = f"""<html>
        <head>
            <title>{text}</title>
        </head>
        <body>
            <h1>{text}</h1>
            <img src={imagepath}/>
        </body>
    </html>
    """
    return HTMLResponse(content=htmlresponse, status_code=200)


@app.get("/sd/")
async def textarea(text: str = defaultprompt, response_class=HTMLResponse):
    id = uuid.uuid4()
    imagepath = f"{OUTDIR}/{id}.png"
    gen_image_768(text, imagepath)
    imgcache[str(id)] = text
    logger.debug(f"{text};{imagepath}")
    return generate_html_response(text, imagepath)
