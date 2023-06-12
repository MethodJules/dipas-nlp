import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

# Daten einlesen
df = pd.read_excel("Overlapping_Tags_and_Comments.xlsx")

# Funktion für Text preprocessing
def preprocess_text(text):
    # Entferne spezielle Charakter und Nummern
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Konvertiere alles zu Kleinbuchstaben
    text = text.lower()
    
    # Entferne stopwords
    stop_words = set(stopwords.words('german'))
    words = nltk.word_tokenize(text)
    text = ' '.join([word for word in words if word not in stop_words])
    
    return text

# Verarbeite die Kommente mit der Funktion
df['Comment'] = df['Comment'].apply(preprocess_text)

# Spalten der Daten in 70/30 Split
train_df, val_df = train_test_split(df, test_size=0.3, random_state=42)

# Kommentare und Labels extrahieren
X_train = train_df["Comment"].values
X_val = val_df["Comment"].values

y_train = [tags.split(',') for tags in train_df["Overlapping_Tags"].values]
y_val = [tags.split(',') for tags in val_df["Overlapping_Tags"].values]

# Binärumwandlung der Labels
mlb = MultiLabelBinarizer()
y_train = mlb.fit_transform(y_train)
y_val = mlb.transform(y_val)

# Pipeline erstellen mit TF-IDF Vectorizer und OneVsRestClassifier mit LinearSVC
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_df=0.8, min_df=5)),
    ("clf", OneVsRestClassifier(LinearSVC(C=1.5)))
])

# Model trainieren
pipeline.fit(X_train, y_train)

# Validierung bzw. Test
y_pred = pipeline.predict(X_val)

# Ausgabe des Classification Reports bezüglich der Performance
print(classification_report(y_val, y_pred, target_names=mlb.classes_, zero_division=0))
