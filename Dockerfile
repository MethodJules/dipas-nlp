FROM python:3.7

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -U spacy
RUN python3 -m pip install -U scikit-learn
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download de_core_news_sm
RUN python3 -m spacy download de_core_news_lg
RUN python3 -m spacy download de_dep_news_trf
RUN python3 -m pip install flask
RUN python3 -m pip install numpy
RUN python3 -m pip install nltk
RUN python3 -m pip install spacy-sentiws
RUN python3 -m pip install pandas
RUN python3 -m pip install openpyxl
RUN python3 -m pip install gensim
RUN python3 -m pip install pyldavis
RUN python3 -m pip install neo4j



EXPOSE 5000

WORKDIR /app

ENTRYPOINT [ "python3" ]

CMD ["app.py"]
