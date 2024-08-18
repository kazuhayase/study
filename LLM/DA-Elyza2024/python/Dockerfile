# set up the container.
FROM python:3-slim

# copy the python dir.
WORKDIR /python
COPY db_llama db_llama
COPY fapi fapi
COPY requirements.txt requirements.txt

#RUN hwclock --hctosys

# install libraries.
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential
RUN pip install --no-cache-dir -r requirements.txt

# set the working dir.
WORKDIR /python/fapi

# expose the port.
EXPOSE 9000

# command to run the app using uvicorn.
#CMD ["uvicorn","main:app","--host","0.0.0.0","--port","9000"]

CMD ["/bin/bash","run-for-docker.sh"]
#CMD ["/bin/bash"]
