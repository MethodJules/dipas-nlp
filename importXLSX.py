import spacy
import pandas as pd

def commentReader(file_path):

    df = pd.read_excel(file_path)
    df = df.sort_values(by=["Comment ID"])

    xlsxDict = None

    for i in df.index:
        
        if xlsxDict is None:
            xlsxDict = {df.at[i, "Comment ID"]:df.at[i, "Comment Text"]}
        else:
            xlsxDict.update({df.at[i, "Comment ID"]:df.at[i, "Comment Text"]})

    return xlsxDict