FROM python:3.7

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -U spacy
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download de_core_news_sm
RUN python3 -m spacy download de_dep_news_trf
RUN python3 -m pip install flask
RUN python3 -m pip install numpy
RUN python3 -m pip install nltk

EXPOSE 5000

WORKDIR /app

ENTRYPOINT [ "python3" ]

CMD ["app.py"]