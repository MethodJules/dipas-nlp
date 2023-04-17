from nlpProcess import nlpProcess

nlpProc = nlpProcess()

input = {"1": "Es fehlt ein sicherer Radweg in der Behring- und Barnerstraße von der Kreuzung Am Born bis zum " \
              "Lessingtunnel. Hier wird häufig viel zu schnell gefahren und es werden die zu Radfahrern " \
              "einzuhaltenden Mindestabstände missachtet. An den besonders verkehrsreichen Kreuzungen an der" \
              " Friedensallee und Bahrenfelder Straße gleicht das Einordnen und Links-Abbiegen für Radfahrer einem" \
              " hochriskanten Abenteuer. Das Ausweichen nicht nur jugendlicher Radfahrer auf den vor Autos sicheren" \
              " Fußweg wird mit bösen Kommentaren der Fußgänger quittiert. Ein baulich von den Autos getrennter" \
              " Radweg mit Vorrang für Radler würde die Fahrbahnbreite einschränken, so dass die Autofahrer nicht" \
              " mehr zum schnellen Fahren auf breiten Straßen verführt werden -" \
              "gerade nachts beim Rennen mit hochmotorisierten Sportwagen. Hier besteht dringend Handlungsbedarf. " \
              "Viele Grüße von einem auto- und vor allem radfahrenden Anwohner",
         "2": "Aus meiner Sicht fehlt die Glashütter Landstraße ab Stadtgrenze in Verbindung mit deren"
              " Verlängerung, der Hummelsbüttler Hauptstraße in der Kategorie 2. Der Umstand, dass sich der"
              " Straßenname ändert, kann ja keinen Unterschied ausmachen."}

# Identify relations for each comment.
for id, comment in input.items():
    relations = nlpProc.extractRelations(comment)
    print(f"Relations for comment {id}: {relations}")

# Remove stopwords from each comment.
filtered = nlpProc.removeStopwords(input)
print(filtered)

# Find entities in each comment.
entities = nlpProc.findEntities(input)
print(entities)