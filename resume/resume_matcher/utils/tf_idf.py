from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
import pandas as pd
import math
# Function to get sorted TF-IDF scores for the document

def get_vectors(res_document,job):
    tfidf = TfidfVectorizer()
    words = tfidf.fit_transform([res_document,job])
    dense = words.toarray()
    return dense

def get_top_words_based_on_tfidf_scores(token,limit=20):
    tfidf = TfidfVectorizer()
    words = tfidf.fit_transform([token])
    dense = words.todense()
    feature_name=tfidf.get_feature_names_out()
    df = pd.DataFrame(dense, columns=feature_name)
    stopword_s = set(stopwords.words('english'))
    # n_size = df.shape[1]
    tfidf_scores = df.iloc[0]  # Since there is only one document, we use index 0
    # print(f"MEAN Score :{tfidf_scores.mean()}")
    # print(f"MAX Score :{tfidf_scores.max()}")
    # print(f"STD Score:{tfidf_scores.var()}")
    # print(f"MIN Score :{tfidf_scores.min()}")
    # print(f"Q Score :{tfidf_scores.quantile(0.2)}")
    sorted_tfidf_scores = tfidf_scores.sort_values(ascending=False)
    result = []
    for i in range(limit):
        if sorted_tfidf_scores.index[i] not in stopword_s:
            result.append(sorted_tfidf_scores.index[i])
    # mi = tfidf_scores.quantile(0.9)
    # q1=tfidf_scores.quantile(0.9)
    # ct = 0
    # for i in range(len(sorted_tfidf_scores)):
    #     if sorted_tfidf_scores.iloc[i]>=q1:
    #         ct+=1
    # #print(f"Q1 Score :{q1}---->COUNT : {ct}")
    # ct = 0
    #q2=tfidf_scores.mean()
    
    # for i in range(len(sorted_tfidf_scores)):
    #     if sorted_tfidf_scores.iloc[i]>=q2:
    #         result.append(sorted_tfidf_scores.index[i])
    #         #print(sorted_tfidf_scores.index[i])
    #         ct+=1
    #print(f"Q2 Score :{q2}---->COUNT : {ct}")
    # ct = 0
    # q3=tfidf_scores.quantile(0.7)
    # for i in range(len(sorted_tfidf_scores)):
    #     if sorted_tfidf_scores.iloc[i]>=q3:
    #         ct+=1
    # #print(f"Q3 Score :{q3}---->COUNT : {ct}")
    # ct = 0
    # q3=tfidf_scores.quantile(0.6)
    # for i in range(len(sorted_tfidf_scores)):
    #     if sorted_tfidf_scores.iloc[i]>=q3:
    #         ct+=1
    # #print(f"Q4 Score :{q3}---->COUNT : {ct}")
    # ct = 0
    # q3=tfidf_scores.quantile(0.5)
    # for i in range(len(sorted_tfidf_scores)):
    #     if sorted_tfidf_scores.iloc[i]>=q3:
    #         ct+=1
    #print(f"Q5 Score :{q3}---->COUNT : {ct}")
    # for i in range(len(sorted_tfidf_scores)):
    #     print(f"{sorted_tfidf_scores.iloc[i]}======Score-->{sorted_tfidf_scores.index[i]}")
    return result

def do_tfidf(token):
    tfidf = TfidfVectorizer()
    words = tfidf.fit_transform([token])
    dense = words.todense()
    feature_name=tfidf.get_feature_names_out()
    
    # print(set(len(feature_name)))
    # print(len(feature_name))
    # Create a DataFrame to display the TF-IDF scores
    # print("\n\n================\n\n")
    # print(df)
    # print("\n\n================\n\n")
    # print("\n\n================\n\n")
    # print(sorted_tfidf_scores)
    # print("\n\n================\n\n")
    # sentence = " ".join(feature_name)
    # # print("\n\n================\n\n")
    # # print(sentence)
    # # print("\n\n================\n\n")
    # return sentence
    sentence = " ".join(feature_name)
    #print(sentence)
    return sentence
