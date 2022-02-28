FROM python:3.9

COPY . /opt/app
WORKDIR /opt/app

RUN pip3 install -r requirements.txt
RUN mkdir ~/config
RUN cp config.toml ~/config/config.toml
RUN cp credentials.toml ~/config/credentials.toml

EXPOSE 80
USER root

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]