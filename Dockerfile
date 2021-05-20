FROM nini94/tensorflow2.5.0-dlib19.22-opencv4.5.2
COPY makeup-bot/ /home/bot/makeup-bot/
COPY requirements_dockerfile.txt /home/bot/requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
RUN pip install -r /home/bot/requirements.txt
WORKDIR /home/bot/makeup-bot/
CMD python main.py