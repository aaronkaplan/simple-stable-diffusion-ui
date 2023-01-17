from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
import contextlib
autocast = contextlib.nullcontext


# here is how you could force it to use a specific GPU (1 in this case) from within the code
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def gen_image(prompt: str, output_filename: str):
    """Use stable diffusion 2 to generate an image based on text"""

    repo_id = "stabilityai/stable-diffusion-2-base"
    repo_id = "stabilityai/stable-diffusion-2-1"
    pipe = DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, revision="fp16", device_map="auto", cache_dir='/model-cache')

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")

    image = pipe(prompt, guidance_scale=9, num_inference_steps=25).images[0]
    image.save(output_filename)


def gen_image_768(prompt: str, output_filename: str):
    """Use stable diffusion 2 to generate an image based on text and expand the image (scale it up)"""

    model_id = "stabilityai/stable-diffusion-2"

    # Use the Euler scheduler here instead
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, revision="fp16", torch_dtype=torch.float16, device_map="auto", cache_dir='/model-cache')
    pipe = pipe.to("cuda")

    image = pipe(prompt, height=768, width=768).images[0]

    image.save(output_filename)
