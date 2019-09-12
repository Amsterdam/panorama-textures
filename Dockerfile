FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

RUN apt-get install -y \
        libgdal-dev \
        python3-gdal

RUN adduser --system datapunt \
	&& mkdir -p /static \
	&& chown datapunt /static \
	&& mkdir -p /app/unzipped \
	&& chown datapunt /app/unzipped \
	&& mkdir -p /app/data \
	&& chown datapunt /app/data

WORKDIR /app
COPY src/requirements.txt /app/
RUN pip install pygdal=="`gdal-config --version`.*"
RUN pip install -r requirements.txt

USER datapunt

COPY src/array_image.py /app/
COPY src/array_math.py /app/
COPY src/texture.py /app/
COPY src/texture_bouwblok.py /app/
COPY src/texture_line.py /app/
COPY src/texture_pand.py /app/
COPY src/texture_composite.py /app/
COPY src/panorama_texture.py /app/
