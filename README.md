# panorama-textures

Extracting textures for (3d) objects from panoramas. This project contains example code to extract possible textures 
from panorama images

### See code

Code has been arranged in several files:

- `array_image.py`: code to treat images programmatically with `numpy` and `scipy` array-manupilations
- `array_math.py`: the code that programmitacly manipulates arrays (projections, samples)
- `texture.py`: methods to extract textures from images, given a simple 3D plane, and a point of view

Both `sample.py` and several `obj{*}.py` files use this code.

### See results

The output of the actions below are currently also available in GitHub, see the `src/obj_output` and 
`src/sample_output` directories.

### Do it yourself

Requires `python` to run, but examples are included, so they can be shown as is.

To run examples, install the dependencies from `requirements.txt`:

    pip install -r src/requirements.txt


#### Sample

Two examples have been made from the Dam:

See: [this sample on Amsterdam CityData](https://data.amsterdam.nl/data/panorama/TMX7316010203-000716_pano_0000_001622?modus=gesplitst&center=52.3728927%2C4.8930551&heading=-109.09024292815127&lagen=pano%3A1&legenda=false&locatie=52.3728926697179%2C4.89305514150316&pitch=-9.229251781352469&zoom=16) (valid as of february 2019)

To 'build' it:

    $ cd src
    /src $ python sample.py

Then in the sample_output folder you will find the following files:

- `paleis_opgang.jpg`: the entrance to the palace
- `paleis_voorgevel.jpg`: the whole Dam-side facade of the palace
- `tussauds_dam.jpg`: the Dam facing facade of Tussaud's
- `tussauds_rokin.jpg`: the Rokin facing facade of Tussaud's
- `tussauds.jpg`: the stitched together facades of Tussaud's


#### Obj

Three example `.obj` files have been provided by the 3DAmsterdam project (Digital Twin)

For these files some preleminary facade sets have been calculated.

To 'build' it:

    $ cd src
    /src $ python obj.py

Then in the obj_output folder you will find the following sets of files:

