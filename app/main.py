import uuid
from fastapi import FastAPI, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


from sd import gen_image, gen_image_768
import logger
from cache import Cache

app = FastAPI()
logger = logger.get_module_logger(__name__)

class Inputs(BaseModel):
    prompt: str
    image: bytes = File(...)


# to serve static files in fastapi
app.mount("/sd/output", StaticFiles(directory="/app/output"), name="output")

# the cache to store all the prompts and image filenames
imgcache = Cache()


@app.get("/")
async def generate_form(prompt: str = "an astronaut riding a horse on mars"):
    htmlresponse = f"""<form action="/sd/imagegen" enctype="multipart/form-data" method="post">
            <textarea name="prompt" value="{prompt}">{prompt}</textarea><p/>
            <input name="image" type="file"><p/>
            <input type="submit">
        </form>
    """
    return HTMLResponse(content=htmlresponse, status_code=200)


@app.post("/sd/imagegen")
async def generate_new_image(inputs: Inputs):
    # generate new image using the prompt and image provided in the inputs
    result_image = inputs.image     # generate_new_image(inputs.prompt, inputs.image)
    htmlresponse = f"""<head>
            <title>{inputs.prompt}</title>
        </head>
        <form action="/sd/imagegen" enctype="multipart/form-data" method="post">
            <textarea name="prompt" value={inputs.prompt}></textarea><p/>
            <input name="image" type="file"><p/>
            <input type="submit">
        </form>
        <img src="data:image/png;base64,{result_image.encode()}">
        """
    return HTMLResponse(content=htmlresponse, status_code=200)


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
async def textarea(text: str = "High quality photo of an astronaut riding a horse in space", response_class=HTMLResponse):
    id = uuid.uuid4()
    imagepath = f"output/{id}.png"
    gen_image_768(text, imagepath)
    imgcache[str(id)] = text
    logger.debug(f"{text};{imagepath}")
    return generate_html_response(text, imagepath)
