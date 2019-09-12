# panorama-textures in Docker

Extracting textures for (3d) objects from panoramas. This project can be run from inside a Docker, saving 
the output to a directory that will persist after the docker is shut down.


### Before first run

Before the first run, make sure you have Docker installed, then build the image in the root of the project:

    docker build . -t local/panorama-texture

### Extract texture for a Plane in 3D space

    usage: texture_line.py [-h] [--resolution RESOLUTION] [--height HEIGHT]
                        pano_id left right filename
 
    positional arguments:
       pano_id               Id of the panorama to project on a plane
       left                  comma-separated x,y in RD: left bottom point of the
                             plane to project on
       right                 comma-separated x,y in RD: right bottom point of the
                             plane to project on
       filename              output filename
     
     optional arguments:
       -h, --help            show this help message and exit
       --resolution RESOLUTION
                             Resolution in pixels per meter (defaults to 10)
       --height HEIGHT       Height of the facade in meters (defaults to 30)

Running from the root of the project, otherwise replace the `pwd` with the full path to your the output directory.

It is possible to extract the required input parameters from the Data Portal of the City of Amsterdam:

[Left-bottom point](https://data.amsterdam.nl/data/geozoek/?center=52.3730434%2C4.8936129&locatie=52.3733044%2C4.8936084&zoom=15)
and
[Right-bottom point](https://data.amsterdam.nl/data/geozoek/?center=52.3728795%2C4.8941328&locatie=52.3729217%2C4.8944116&zoom=15)

The RD-coordinates can be copied from the page (remove the space)

Then select the panorama image in the [interface](https://data.amsterdam.nl/data/panorama/TMX7316010203-001187_pano_0000_001503/?center=52.3728418%2C4.893152&heading=48.97997622076379&lagen=pano%3A1&locatie=52.3728418022451%2C4.89315196317801&pitch=0.3190651159979569&zoom=14)
The pano_id can be copied from the URL.

The final command may look something like this:

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_line.py \
                     TMX7316010203-001187_pano_0000_001503 \
                     121386.57,487384.36 \
                     121440.98,487341.41 \
                     dam_1-7.jpg \
                     --height 36 \
                     --resolution 15
                     

### Extract composite texture, from multiple panoramas, for a Plane in 3D space

    usage: texture_composite.py [-h] [--steps STEPS] [--resolution RESOLUTION]
                                [--height HEIGHT]
                                from_pano_id to_pano_id left right filename

    positional arguments:
      from_pano_id          Id of the first panorama in a row to project
      to_pano_id            Id of the first panorama in a row to project (should
                            be same )
      left                  comma-separated x,y in RD: left bottom point of the
                            plane to project on
      right                 comma-separated x,y in RD: right bottom point of the
                            plane to project on
      filename              output filename
    
    optional arguments:
      -h, --help            show this help message and exit
      --steps STEPS         Sample one in every steps panorama (defaults to 1)
      --resolution RESOLUTION
                            Resolution in pixels per meter (defaults to 10)
      --height HEIGHT       Height of the facade in meters (defaults to 30)
  
Run it the root of the project, otherwise replace the `pwd` with the full path to your the output directory.

It is possible to extract the required input parameters from the Data Portal of the City of Amsterdam:

[Left-bottom point](https://data.amsterdam.nl/data/geozoek/?center=52.3730434%2C4.8936129&locatie=52.3733044%2C4.8936084&zoom=15)
and
[Right-bottom point](https://data.amsterdam.nl/data/geozoek/?center=52.3728795%2C4.8941328&locatie=52.3729217%2C4.8944116&zoom=15)

The RD-coordinates can be copied from the page (remove the space)

Then select the panorama image in the [interface](https://data.amsterdam.nl/data/panorama/TMX7316010203-001187_pano_0000_001503/?center=52.3728418%2C4.893152&heading=48.97997622076379&lagen=pano%3A1&locatie=52.3728418022451%2C4.89315196317801&pitch=0.3190651159979569&zoom=14)
The pano_id can be copied from the URL.

The final command may look something like this:

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_composite.py \
                     TMX7316010203-001181_pano_0000_005814 \
                     TMX7316010203-001181_pano_0000_005849 \
                     121947.89,486581.27 \
                     122118.38,486632.83 \
                     test.jpg \
                     --height 20 \
                     --resolution 15
                     

### Extract texture for a Building


    usage: texture_pand.py [-h] [--resolution RESOLUTION] [--height HEIGHT]
                           [--simplify SIMPLIFY] [--force]
                           pano_id pand_id filename
    
    positional arguments:
      pano_id               Id of the panorama to project on a plane
      pand_id               The BAG ID of the building on which the panorama is to
                            be projected
      filename              output filename
    
    optional arguments:
      -h, --help            show this help message and exit
      --resolution RESOLUTION
                            Resolution in pixels per meter (defaults to 10)
      --height HEIGHT       Height of the facade in meters (defaults to 30)
      --simplify SIMPLIFY   Smoothing the geometry, in meters (default off)
      --force               Force all forward facing sides to be projected, even
                            those under a shallow angle

Running from the root of the project, otherwise replace the `pwd` with the full path to your the output directory.

It is possible to extract the required input parameters from the Data Portal of the City of Amsterdam:

[pand_id](https://data.amsterdam.nl/data/bag/pand/id0363100012168052/?center=52.3728795%2C4.8941328&zoom=13)

Then select the panorama image in the [interface](https://data.amsterdam.nl/data/panorama/TMX7316010203-001187_pano_0000_001503/?center=52.3728418%2C4.893152&heading=48.97997622076379&lagen=pano%3A1&locatie=52.3728418022451%2C4.89315196317801&pitch=0.3190651159979569&zoom=14)
The pano_id can be copied from the URL.

In this case the command would look something like this:

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_pand.py \
                     TMX7316010203-001187_pano_0000_001503 \
                     0363100012168052 \
                     dam_1.jpg \
                     --height 33 \
                     --resolution 12

Only sides from the building that are facing under not a too shallow angle to the panorama are pasted in the image.
 
With additional parameters:
 
    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_pand.py \
                     TMX7316010203-001187_pano_0000_001503 \
                     0363100012168052 \
                     dam_1_simple.jpg \
                     --height 33 \
                     --resolution 12 \
                     --simplify 1 \
                     --force

This simplifies the geometry (removing all aspects smaller than 1m) and forces to paste all the sides that
are facing the camera, even the ones with a shallow angle.
 
### Extract texture for a Building Block

    usage: texture_bouwblok.py [-h] [--resolution RESOLUTION] [--height HEIGHT]
                               [--simplify SIMPLIFY] [--force]
                               pano_id blok_id filename
    
    positional arguments:
      pano_id               Id of the panorama to project on a plane
      blok_id               The BAG ID of the block on which the panorama is to be
                            projected
      filename              output filename
    
    optional arguments:
      -h, --help            show this help message and exit
      --resolution RESOLUTION
                            Resolution in pixels per meter (defaults to 10)
      --height HEIGHT       Height of the facade in meters (defaults to 30)
      --simplify SIMPLIFY   Smoothing the geometry, in meters (default off)
      --force               Force all forward facing sides to be projected, even

Running from the root of the project, otherwise replace the `pwd` with the full path to your the output directory.

It is possible to extract the required input parameters from the Data Portal of the City of Amsterdam:

[blok_id](https://data.amsterdam.nl/data/gebieden/bouwblok/id03630012100938/?center=52.3728795%2C4.8941328&zoom=13)

Press the 'i' icon to expand the BAG-ID

Then select the panorama image in the [interface](https://data.amsterdam.nl/data/panorama/TMX7316010203-001187_pano_0000_001503/?center=52.3728418%2C4.893152&heading=48.97997622076379&lagen=pano%3A1&locatie=52.3728418022451%2C4.89315196317801&pitch=0.3190651159979569&zoom=14)
The pano_id can be copied from the URL.
                            those under a shallow angle

An example of the usage could be:

    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_bouwblok.py \
                     TMX7316010203-001187_pano_0000_001503 \
                     03630012100938 \
                     ya77.jpg \
                     --height 37 \
                     --resolution 16

Only sides from the building that are facing the panorama are pasted in the image.
 
With additional parameters:
 
    docker run -v `pwd`/texture_output:/app/textmap_output local/panorama-texture python texture_bouwblok.py \
                     TMX7316010203-001187_pano_0000_001503 \
                     03630012100938 \
                     ya77_simple.jpg \
                     --height 37 \
                     --resolution 16 \
                     --simplify 2 \
                     --force

This simplifies the geometry (removing all aspects smaller than 2m) and forces to paste all the sides that
are facing the camera, even the ones with a shallow angle.
 
 
 
 