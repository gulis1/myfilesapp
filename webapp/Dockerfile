FROM ubuntu:25.10
 
RUN apt update && \
    apt install -y git python3 python3-pip
 
RUN git clone https://github.com/gulis1/animalAPP
WORKDIR animalAPP
 
RUN pip install --break-system-packages -r requirements.txt
COPY ./appconf.json /animalAPP
 
EXPOSE 5000
ENTRYPOINT ["python3", "app.py"]
