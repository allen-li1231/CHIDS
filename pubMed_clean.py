"""
@Author: Allen Li       11/6/2019
"""
import pandas as pd
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt


_stopword = set()
_stopword.update(['natural', 'language', 'processing', 'nlp',
                  'use', 'using', 'used', 'set', 'also', 'compare',
                  'information', 'analysis', 'method',
                  'based', 'study', 'model', 'report', 'case',
                  'tool', 'concept', 'research', 'approach', 'notes'
                  'one', 'two', 'three', 'multiple', 'methods',
                  'group', 'outcome', 'toward', 'note', 'may',
                  'found', 'developed', 'task', 'term', 'including',
                  'provide', 'report', 'result', 'however', 'document',
                  'associate', 'respectively', 'finding', 'studies',
                  'results', 'associated', 'development'])

excel_path = "./pubMed_data_natural_language_processing.xlsx"
literature = pd.read_excel(excel_path)
title = literature.Title
abstract = literature.Abstract

# generate word cloud
cloud = WordCloud(stopwords=_stopword,
                  background_color="white",
                  max_words=30,
                  width=1000, height=800,
                  font_path="simkai.ttf")


def column_to_corpus_str(s: pd.Series) -> str:
    s = s.astype("str")
    s = " ".join(s)
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)
    s = s.split(" ")
    filtered = [word for word in s if word not in stopwords.words('english')]
    filtered = ' '.join(filtered)
    return filtered


def show_cloud(s: str) -> WordCloud:
    s_cloud = cloud.generate(s)
    plt.axis("off")
    plt.imshow(s_cloud, interpolation="bilinear")
    return s_cloud


def count_keyword(series, keyword, in_column) -> int:
    if isinstance(series[in_column], str):
        s = series[in_column].lower()
        return s.count(keyword)
    else:
        return 0


def group_count(data: pd.DataFrame, group_col, keywords: list, cols_to_count: list):
    cols_new = []
    for kwd in keywords:
        for col in cols_to_count:
            col_name = '_'.join(['Count', kwd, col])
            cols_new.append(col_name)
            data[col_name] \
                = data.apply(count_keyword, axis=1, args=(kwd, col))

    return data[cols_new].groupby(data[group_col]).sum()


title_filtered = column_to_corpus_str(title)
abstract_filtered = column_to_corpus_str(abstract)
title_cloud = show_cloud(title_filtered)
title_cloud.to_file("title_pubMed_natural_language_processing_word_cloud.png")

abstract_cloud = show_cloud(abstract_filtered)
abstract_cloud.to_file("abstract_pubMed_natural_language_processing_word_cloud.png")


def to_excel(path):
    col_to_count = ['Title', 'Abstract']
    keywords = ["diabetes", "social",
                "lifestyle", "life style",
                'hba1c', 'hyperglycemia',
                'insulin', 'glucose',
                'cardiovascular', 'heart']
    sts = group_count(literature, "Year", keywords, col_to_count)
    exl_writer = pd.ExcelWriter(path)
    sts.to_excel(exl_writer, sheet_name="STS")
    exl_writer.close()
