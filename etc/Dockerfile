FROM ubuntu:16.04

# Update Ubuntu and install necessary packages
RUN apt update && \
    apt install -y python2.7 python-pip git gfortran mpich zip

# Clone the spc repository
WORKDIR /root
RUN git clone https://github.com/whbrewer/spc
RUN pip install --upgrade "pip < 21.0" && pip install virtualenv

# Initialize spc
WORKDIR /root/spc
RUN sed -i '/pyyaml/d' requirements.txt # remove requirement for pyyaml
RUN echo Y | ./spc init
RUN ./spc install https://github.com/whbrewer/fmendel-spc-linux/archive/master.zip

# Clone mendel-f90 into apps/mendel and copy necessary files
WORKDIR /root/spc/apps
RUN rm -r mendel
RUN git clone https://github.com/whbrewer/mendel-f90 mendel

# Build mendel-f90
WORKDIR /root/spc/apps/mendel
RUN make

# Update files from distro for SPC use
WORKDIR /root/spc
RUN mkdir -p static/apps/mendel && \
    cp apps/mendel/mendel.tpl views/apps && \
    cp apps/mendel/mendel.js static/apps/mendel && \
    cp apps/mendel/help.html static/apps/mendel && \
    cp apps/mendel/about.html static/apps/mendel

# Create mendel package for SPC
#WORKDIR /root/spc/apps
#RUN zip -rm mendel.zip mendel

# Install mendel package into SPC
WORKDIR /root/spc
RUN ./spc install apps/mendel.zip

# Expose port 8580
EXPOSE 8580

# Set the entrypoint to run spc on container launch
WORKDIR /root/spc
ENTRYPOINT ["./spc", "run"]
