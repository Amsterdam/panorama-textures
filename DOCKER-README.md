# panorama-textures in Docker

Extracting textures for (3d) objects from panoramas. This project can be run from inside a Docker, saving 
the output to a directory that will persist after the docker is shut down.



### Before first run

Before the first run, make sure you have Docker installed, then build the image:

    docker build . -t local/panorama-texture

### Extract texture for a BAG-Pand

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python bag2texture.py