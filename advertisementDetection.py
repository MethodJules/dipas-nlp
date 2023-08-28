import pandas as pd
import re

"""
Klasse zum erkennen von URLS in Kommentaren
Benötigt als Input einen JSON Dataframe und eine Spalte mit dem Namen text
Gibt einen Dict mit der ID und dem Kommentar aus, in dem eine URL erkannt wurde
"""

def detectUrl (df):

    comment_urls = {}
    url_pattern = r"(https?:\/\/)?(www\.)?[a-zA-Z0-9][a-zA-Z0-9-]*\.[a-zA-Z]{2,}"

    for index, row in df.iterrows():
        text = row["text"]
        
        contains_url = bool(re.search(url_pattern, text))

        if contains_url:
            comment_urls[index] = text

    return comment_urls

"""
df = pd.read_json("comments_export2.json", orient="index")

urls = detectUrl(df)

for index, text in urls.items():
    print(index, text)
    print()

print(len(urls))
"""
