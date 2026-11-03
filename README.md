# Wave Function Collapse Demonstrator

This Python script demonstrates the Wave Function Collapse algrorithm using pygame to create the topogragraphy of a game on a grid where one tile is randomly picked and placed. The Wave Function Algorithm then proceeds to fill out the rest of the grid with various tiles according to the rules provided to the algorithm.

Wave Function Collapse Algorithm demonstrator. This program takes no input and generates a world using the Wave Function.

Wave Function Collapse is a very independent-minded algorithm and needs almost no outside help or instruction. You feed it an example to start with and it figures everything else out for itself using the supplied set of rules that you have provided.

A random tile is chosen from the set of possible tiles to place in a given location. The tile is then collapsed to a single possibility based on the weights of the tiles in the set. The weights are determined by the number of times a tile appears in the set of possible tiles to place in a given location. 

Many of the algorithms and code have been taken from various repositories on GitHub and the internet, Most of the code has been translated from other languages and modified to work with this project, additionally to pass pylint and bandit security checks. 

Overrides for pylint, bandit have been added to the code to allow for the use of the random.choices() function, which is flagged as a false positive security issue by bandit and pylint.

The graphic (sprite) images are from Puny World and are freely usuable.

**TL;DR** - Assuming that you have Python installed. To run this demonstration, do the following.

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 ./wave_function_collapse.py
```

## Python support

Continuous integration tests and linting run on Python 3.10, 3.11, and 3.14.

## Run in a container

Build the image:

```bash
docker build -t wave-function-collapse .
```

Run the app container:

```bash
docker run --rm -it wave-function-collapse
```

> Note: this project uses pygame, so displaying the game window from a container
> requires display forwarding (for example, X11/Wayland passthrough).

## Run with Docker Compose

Build and run:

```bash
docker compose up --build
```

By default, `docker-compose.yml` sets `SDL_VIDEODRIVER=dummy` for headless runs.
To try GUI display forwarding, set `SDL_VIDEODRIVER` and `DISPLAY` in your shell
before running compose.
