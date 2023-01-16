import spacy
import csv
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from spacy import displacy
'''
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)

print("============================")
# Name Entity Recognition
for ent in doc.ents:
    print(ent.text, ent.label_)
print("============================")

nlp = spacy.load("de_core_news_sm")
doc = nlp("Gerne mehr Strassenbäume im Nördlichen Teil der Lindenalle. Und besonders dort auch bitte kein Querparken mehr, von den schmalen Gehwegen bleibt ja durch den überstand der Autos fast gar nichts mehr übrig. Die gesamte Lindenalle sollte breitere Gehwege erhalten. Da muss man halt notfalls auch mal ein wenig Parkraum oder Strassenraum abzwacken. Irgendwo muss der Platz ja herkommen. Und der Platz am Wendehammer sollte umgestaltet werden, mit blumen und evtl. einem Brunnen..")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)
# display name entities
displacy.serve(doc, style="ent")

print("============================")
nlp = spacy.load("de_dep_news_trf")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)
# create a html code to show
html = displacy.render([doc], style="dep", page=False)
print(html)
