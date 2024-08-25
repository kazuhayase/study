# set up the container.
FROM python:3-slim AS base

# install libraries.
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential \
&& apt-get clean 
#&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
#RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# copy the python dir.
WORKDIR /python
RUN mkdir log
COPY db_llama db_llama
COPY fapi fapi

## copy db_llama replace ## COPY Downloads Downloads
## copy db_llama replace ## COPY llama_mkvec.py llama_mkvec.py
## copy db_llama replace ## #RUN --mount=type=secret,id=env source /run/secrets/env
## copy db_llama replace ## COPY source-env.sh source-env.sh
## copy db_llama replace ## COPY mkdb-for-docker.sh mkdb-for-docker.sh
## copy db_llama replace ## #RUN ["/bin/bash","source-env.sh"]
## copy db_llama replace ## #CMD ["/usr/bin/python3", "llama_mkvec.py"]

## copy db_llama replace ## FROM base AS build-chromadb
## copy db_llama replace ## WORKDIR /python
## copy db_llama replace ## #RUN --mount=type=secret,id=env,src=/home/kazu/.env ["/bin/bash","mkdb-for-docker.sh"]
## copy db_llama replace ## RUN --mount=type=secret,src=/home/kazu/.env ["/bin/bash","mkdb-for-docker.sh"]
## copy db_llama replace ## #RUN --mount=type=secret,required=true,id=.env ["/bin/bash","mkdb-for-docker.sh"]
## copy db_llama replace ## FROM build-chromadb AS run

FROM base AS run

# expose the port.g
EXPOSE 9000

# set the working dir.
WORKDIR /python/fapi
#WORKDIR /python

# command to run the app using uvicorn.
#CMD ["uvicorn","main:app","--host","0.0.0.0","--port","9000"]

CMD ["/bin/bash","run-for-docker.sh"]
#CMD ["/bin/bash"]
