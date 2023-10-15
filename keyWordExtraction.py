import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

'''
Loads from the given file path custom stopwords into a list
Source of the stopwords: https://github.com/solariz/german_stopwords
'''


def load_custom_stopwords(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = [word.strip() for word in file.readlines()]
    return stopwords


'''
Custom preprocessing methood for all functions regarding the keyword extraction.
Input of the preprocessing is a pandas dataframe from which the column "text" is read
Output of the preprocessing is a pandas dataframe which was extended by the "column modiefied_text"

Steps of the preprocessing:
Delete identical comments
Remove line breaks
Remove URLs and email addresses
Remove special characters
Remove numbers
Remove whitepaces
Lemmatization
Converting to lowercase
Remove stopwords
'''


def preprocessing_keywords(df):

    nlp = spacy.load("de_core_news_lg")

    stopwords = load_custom_stopwords("stopwords.txt")

    checked_comments = []
    for index, row in df.iterrows():
        text = row["text"]

        if text in checked_comments:
            df.drop(index, inplace=True)
            continue
        checked_comments.append(text)

        text = text.replace("\n", "")
        text = re.sub(r'http\S+|www\S+|[\w]+@[\w]+\.[\w]+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.strip()

        doc = nlp(text)
        lemmatized_tokens = [token.lemma_ for token in doc]
        text = ' '.join(lemmatized_tokens)

        text = text.lower()

        tokens = text.split()
        filtered_tokens = [token for token in tokens if token not in stopwords]
        text = ' '.join(filtered_tokens)

        df.at[index, "modified_text"] = text
    return df


'''
Calculates the tfidf values for each word over the entire corpus and sums them up. In addition, the number of times each word occurs in the corpus is counted.
The keywords are sorted by the summed tfidf values and stored in a list together with the word frequency.
Input is a preprocessed pandas dataframe, which contains the column "modified_text" and the number of keywords which should be returned, which is also equal to the length of the list.
Output is a list with keywords, summed tfidf values and word frequency.
'''


def corpus_keywords(df_preprocessed, number_keywords):
    df_list = df_preprocessed["modified_text"].tolist()
    cv = CountVectorizer(max_df = 0.75)
    word_count_vector=cv.fit_transform(df_list)

    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    count_vector=cv.transform(df_list)
    tf_idf_vector=tfidf_transformer.transform(count_vector)

    feature_names = cv.get_feature_names_out()

    word_frequencies = {}
    for word, index in cv.vocabulary_.items():
        word_frequency = word_count_vector[:, index].sum()
        word_frequencies[word] = word_frequency

    total_tfidf_values = tf_idf_vector.sum(axis=0)

    df_tfidf = pd.DataFrame(total_tfidf_values.T, index=feature_names, columns=["TF-IDF"] )
    df_tfidf["Word Frequency"] = [word_frequencies.get(word, 0) for word in feature_names]

    df_tfidf = df_tfidf.sort_values(by="TF-IDF", ascending=False)

    top_keywords = df_tfidf.head(number_keywords)

    return top_keywords


'''
Calculates the tfidf values for each word in a comment. The keywords for every comment are sorted by the tfidf values and for each comment only the keywords with the fifth highest tfidf values are displayed.
If a comment does not have five keywords, the remaining keywords will be <none>.
Input is a preprocessed pandas dataframe, which contains the column "modified_text".
Output is a modified pandas dataframe, which contains the column "keywords"
'''
def comment_keywords(df_preprocessed):
    df_list = df_preprocessed["modified_text"].tolist()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(df_list)

    dict_of_tokens={i[1]:i[0] for i in vectorizer.vocabulary_.items()}

    tfidf_vectors = []
    for row in vectors:
        tfidf_vectors.append({dict_of_tokens[column]:value for (column,value) in zip(row.indices,row.data)})


    doc_sorted_tfidfs =[]
    for dn in tfidf_vectors:
        newD = sorted(dn.items(), key=lambda x: x[1], reverse=True)
        newD = dict(newD)
        doc_sorted_tfidfs.append(newD)

    df_preprocessed["keywords"] = None
    counter = 0
    for index, row in df_preprocessed.iterrows():
        keywords = []
        for i in doc_sorted_tfidfs[counter]:
            if len(keywords) >= 5:
                continue
            keywords.append(i)

        while len(keywords) < 5:
            keywords.append("<none>")

        df_preprocessed.at[index, "keywords"] = keywords
        counter += 1

    return(df_preprocessed)

"""
df = pd.read_json("comments_export2.json", orient="index")

df_preprocessed = preprocessing_keywords(df)

top_keywords = corpus_keywords(df_preprocessed, 30)

df_comment_keywords = comment_keywords(df_preprocessed)

pd.set_option('display.max_colwidth', None)
print(top_keywords)
print(df_comment_keywords.loc[20:25, ["related_node_id","text", "keywords"]])
print(df_comment_keywords[["text", "keywords"]])
"""
