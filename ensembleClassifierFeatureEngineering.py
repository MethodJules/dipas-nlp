import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
from collections import Counter
import numpy as np
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import FunctionTransformer
from unidecode import unidecode

# Daten einlesen
df = pd.read_excel("Overlapping_Tags_and_Comments.xlsx")

# Funktion für Text preprocessing
def preprocess_text(text):
    # Entferne spezielle Charakter und Nummern
    text = unidecode(text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Konvertiere alles zu Kleinbuchstaben
    text = text.lower()
    
    # Entferne stopwords
    stop_words = set(stopwords.words('german'))
    words = nltk.word_tokenize(text)
    text = ' '.join([word for word in words if word not in stop_words])
    
    return text

def clean_labels(labels):
    cleaned = []
    for tag_list in labels:
        cleaned_list = [tag.lower().strip() for tag in tag_list]
        cleaned.append(cleaned_list)
    return cleaned

# Neue Funktion um die Länge der Kommentare zu determinieren
def get_text_length(x):
    return np.array([len(t) for t in x]).reshape(-1, 1)

# Verarbeite die Kommente mit der Funktion
df['Comment'] = df['Comment'].apply(preprocess_text)

# Neue Spalte mit der Länge des Kommentares
df['Comment_Length'] = df['Comment'].apply(lambda x: len(x))

# Spalten der Daten in 70/30 Split
train_df, val_df = train_test_split(df, test_size=0.3, random_state=42)

# Kommentare und Labels extrahieren
X_train = train_df[["Comment", "Comment_Length"]].values
X_val = val_df[["Comment", "Comment_Length"]].values

y_train = [tags.split(',') for tags in train_df["Overlapping_Tags"].values]
y_val = [tags.split(',') for tags in val_df["Overlapping_Tags"].values]

# Wende die clean_labels Methode an
y_train = clean_labels(y_train)
y_val = clean_labels(y_val)

# Reduziere die Dimensionen der Tags und zähle die Frequenz der einzelnen Tags
all_tags = [tag for tags_list in y_train for tag in tags_list]
tag_counter = Counter(all_tags)

# Finde die n am häufigsten vorkommenden Tags
most_common_tags = tag_counter.most_common(6)  # Parameter

# Extrahiere nur die Tags, nicht ihre Anzahl
most_common_tags = [tag[0] for tag in most_common_tags]

# Binärumwandlung der Labels
mlb = MultiLabelBinarizer(classes=most_common_tags)
y_train = mlb.fit_transform(y_train)
y_val = mlb.transform(y_val)

# Stelle die zuvor identifizierten Parameter ein für die Classifier
clf1 = SGDClassifier(loss='log_loss', alpha=0.0001)  
clf2 = SVC(C=1, gamma=1, kernel='sigmoid', degree=4, probability=True)
clf3 = RandomForestClassifier(n_estimators=100)

# Konfiguration des Assembly Classifiers
eclf = VotingClassifier(
    estimators=[('sgd', clf1), ('svc', clf2), ('rf', clf3)],
    voting='soft'
)

# Extrahiere Kommentare
get_text_data = FunctionTransformer(lambda x: x[:, 0], validate=False)

# Extrahiere Kommentarlänge
get_length_data = FunctionTransformer(get_text_length, validate=False)


# Erstelle die Pipeline
pipeline = Pipeline([
    ("union", FeatureUnion(
        transformer_list = [
            ("text_features", Pipeline([
                ("selector", get_text_data),
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_df=0.8, min_df=5, use_idf=False))
            ])),
            ("length_features", Pipeline([
                ("selector", get_length_data),
            ]))
        ]
    )),
    ("clf", OneVsRestClassifier(eclf))
])

# Trainiere das Modell
pipeline.fit(X_train, y_train)

# Vorhersage der Labels
y_pred = pipeline.predict(X_val)

# Ausgabe des Classification Reports
print(classification_report(y_val, y_pred, target_names=mlb.classes_, zero_division=0))