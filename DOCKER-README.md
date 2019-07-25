# panorama-textures in Docker

Extracting textures for (3d) objects from panoramas. This project can be run from inside a Docker, saving 
the output to a directory that will persist after the docker is shut down.



### Before first run

Before the first run, make sure you have Docker installed, then build the image in the root of the project:

    docker build . -t local/panorama-texture

### Extract texture for a BAG-Pand

Running from the root of the project, otherwise modify the `pwd` accordingly to change the output directory.

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python bag2texture.py

