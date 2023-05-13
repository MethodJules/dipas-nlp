import pandas as pd

df = pd.read_excel("Comments_To_Concepts.xlsx")

# Finden von gemeinsamen Tags in den drei Spalten
common_tags = []
common_words = set()
#Excel Datei darf im Spaltennamen keine Leerzeichen enthalten, deswegen wurde aus bspw. Alex Tags --> Alex_Tags
for row in df.itertuples():
    words1 = set(str(getattr(row, "Amira_Tags")).split(","))
    words2 = set(str(getattr(row, "Marcel_Tags")).split(","))
    words3 = set(str(getattr(row, "Alex_Tags")).split(","))
    common = words1.intersection(words2, words3)
    common_tags.append(", ".join(common))
    common_words.update(common)

df["common_tags"] = common_tags

common_words = list(common_words)
common_words.sort()

for word in common_words:
    df[word] = "0"

for index, row in df.iterrows():
    for tags in row["common_tags"].split(","):
        if tags.strip() != "":
            df.at[index, tags.strip()] = "1"

df.to_excel("common_tags.xlsx", index=False)
