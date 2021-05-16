FROM tensorflow/tensorflow:2.4.1
COPY makeup-bot/ /home/bot/makeup-bot/
COPY models/ /home/bot/models/
COPY requirements.txt /home/bot/requirements.txt
COPY .env /home/bot/config.yaml
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install -r /home/bot/requirements.txt
WORKDIR /home/bot/makeup-bot/
CMD python main.py