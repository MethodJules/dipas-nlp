import spacy
import pandas as pd

def commentReader():

    df = pd.read_excel("Comments_To_Concepts.xlsx")

    df = df.sort_values(by=["Comment ID"])
    #df = df.loc[:,["Comment ID", "Comment Text"]] kann raus

    dict = None

    for i in df.index:

        if dict is None:
            dict = {df.at[i, "Comment ID"]:df.at[i, "Comment Text"]}
        else:
            dict.update({df.at[i, "Comment ID"]:df.at[i, "Comment Text"]})

    return dict

dict = commentReader()

#print(dict.keys())
#—&gt; steht schon so in der Exel, Kommentare evtl mit RegEx prüfen?
print(dict[8])
#print(dict.get(5))
#print(list(dict.values())[4])
#print(dict)
