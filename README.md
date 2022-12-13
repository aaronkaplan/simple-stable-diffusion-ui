# Simple Stable Diffusion UI

This is an extremely simple [Stable Diffusion](https://huggingface.co/stabilityai/stable-diffusion-2) web based
UI. The UI is using the [fastapi](http://fastapi.tiangolo.com/) microservice framework.
The installation will also install stable-diffusion for you (note that the initial first run might take long because it will download the whole SD model).


It comes with:

* a totally minimalistic UI. Easy enough for anyone to understand the code and for tweaking it and making it prettier (Pull requests welcome!) :-)
* a cache (redis) which saves the prompt, the timestamp and the filename of the generated image. This is just there to save the prompts so that you can build upon them later on. Regard it as a log.


# Requirements

You'll need a machine with a working NVIDIA based GPU .

I tested and developed on an NVIDIA GeForce RTX 3080 with Driver Version: 520.56.06    CUDA Version: 11.8  , Ubuntu 20.04


# How to install it?

## The manual way

1. git clone it
2. ``pip install -r requirements``
3. Run it: ``uvicorn  --host 0.0.0.0 app:app ``. **Note**: the first time, you run it, this will take long and download large models.
4. Install [redis-stack](https://redis.io/docs/stack/). **Note**: of course, you can also just use plain redis]


## With docker

In case you want to run everything via docker, you can build a docker image and run docker-compose up -d:

```bash

docker build -t simple-stable-diffusion-ui:0.1 . --network=host
docker-compose up -d
```


# How to explore the cache?
``ls -al output/`` as well as using redis-cli to explore the prompt which matched a specific file.

Also, you can use redis-insights (which comes with redis-stack) to graphically explore the filename to prompt mapping

Go to https://localhost:8001/

![redis-insights](docs/redis-insights-screenshot.png)

More documentation on redis-stack [here](https://redis.io/docs/stack/get-started/install/docker/).



# How to report bugs?
Please create a pull request and improve.


