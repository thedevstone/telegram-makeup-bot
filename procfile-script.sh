DEBIAN_FRONTEND=noninteractive
DEBCONF_NONINTERACTIVE_SEEN=true
RUN apt-get update && apt-get install -y python3-opencv