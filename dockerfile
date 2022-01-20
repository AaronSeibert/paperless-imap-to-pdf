# We need wkhtmltopdf

FROM python:3

ENV DIR=/usr/local/bin/

# Change directory so that our commands run inside this new directory
WORKDIR $DIR

ENV WKHTML_VERSION 0.12.4
# Builds the wkhtmltopdf download URL based on version number above
ENV DOWNLOAD_URL "https://downloads.wkhtmltopdf.org/0.12/${WKHTML_VERSION}/wkhtmltox-${WKHTML_VERSION}_linux-generic-amd64.tar.xz" -L -o "wkhtmltopdf.tar.xz"

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl libxrender1 libfontconfig libxtst6 xz-utils

# Download and extract wkhtmltopdf
RUN curl $DOWNLOAD_URL
RUN tar Jxvf wkhtmltopdf.tar.xz
RUN cp wkhtmltox/bin/wkhtmltopdf $DIR

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

RUN mkdir /output
ENV SAVE_DIRECTORY "/output"

CMD [ "python", "./main.py" ]