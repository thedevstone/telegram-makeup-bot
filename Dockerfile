FROM nini94/tensorflow2.5.0-dlib19.22-opencv4.5.2
COPY makeup-bot/ /home/bot/makeup-bot/
COPY models/ /home/bot/models/
COPY requirements.txt /home/bot/requirements.txt
COPY .env /home/bot/.env
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install -r /home/bot/requirements.txt
WORKDIR /home/bot/makeup-bot/
CMD python main.py