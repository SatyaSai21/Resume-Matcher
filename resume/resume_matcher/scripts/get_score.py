import logging
import os
from typing import List

from qdrant_client import QdrantClient,models
from qdrant_client.http.models import Batch
from resume.resume_matcher.scripts.utils import find_path, read_json
from resume.resume_matcher.scripts.get_similarity_score import get_similarity_score, get_similarity_tfidf,get_tfidf_score
from resume.resume_matcher.utils.tf_idf import do_tfidf,get_top_words_based_on_tfidf_scores
# Get the logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)


cwd = find_path("Resume-Matcher")
READ_RESUME_FROM = os.path.join(cwd, "Data", "Processed", "Resumes/")
READ_JOB_DESCRIPTION_FROM = os.path.join(cwd, "Data", "Processed", "JobDescription/")
# from transformers import AutoTokenizer, AutoModel
# import torch as tf

# Load the tokenizer and model
# model_name = "BAAI/bge-base-en"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# def generate_embeddings(text, tokenizer, model):
#     # Tokenize the input text
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

#     # Generate embeddings
#     with torch.no_grad():
#         outputs = model(**inputs)

#     # Extract the embeddings from the output
#     embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

#     return embeddings

# # Example usage
# text = "This is an example sentence."
# embeddings = generate_embeddings(text, tokenizer, model)
# print(embeddings)


def get_score(resume_string, job_description_string):
    
    logger.info("Started getting similarity score")

    documents: List[str] = [resume_string]
    client = QdrantClient(":memory:")
    client.set_model("BAAI/bge-base-en")

    client.add(
        collection_name="demo_collection",
        
        documents=documents,
    )

    search_result = client.query(
        collection_name="demo_collection", query_text=job_description_string
    )
    #print(client.get_collections())
    logger.info("Finished getting similarity score")
    return search_result

# def get_score_transformers(resume_strings, job_description_string):
#     logger.info("STARTED get_score_transformers")
    
#     client = QdrantClient(":memory:")
#     client.recreate_collection(
#         collection_name="temp_collection",
#         vectors_config=models.VectorParams(
#             size=768,distance=models.Distance.COSINE
#         )
#     )
#     ids=[]
#     vectors=[]
#     for i,resume_string in enumerate(resume_strings):
#         ids.append(i)
#         embedding=generate_embeddings(resume_string,tokenizer,model)
#         vectors.append(embedding)
#     try:
#         client.upsert(
#             collection_name="temp_collection",
#             points=Batch(ids=ids,vectors=vectors,payloads=[{"text":resume_string} for resume_string in resume_string])
#         )
#     except:
#         logger.error("In Transformer Embedding : Failed to upsert")
    
#     vector, _ =  generate_embedding(job_description_string)

#     hits = client.search(
#         collection_name="temp_collection", query_vector=vector, limit=30
#     )
#     results = []
#     for hit in hits:
#         result = {"text": str(hit.payload)[:30], "score": hit.score}
#         results.append(result)    

#     return results
    
def get_score_pair(resume_string,jd_string):
    # resume_keywords = resume_dict["extracted_keywords"] + resume_dict["entities"]
    # job_description_keywords = job_dict["extracted_keywords"] + job_dict["entities"]
    # resume_string = " ".join(resume_keywords)
    # jd_string = " ".join(job_description_keywords)
    #print("*"*30)
    final_result = get_similarity_score(resume_string, jd_string)
    score  = 0
    for r in final_result:
        score += float(r["score"])
        #print(float(r["score"]))
    
    #print("***"*30)
    res1=do_tfidf(resume_string)
    res2=do_tfidf(jd_string)
    final_result = get_similarity_score(res1, res2)
    for r in final_result:
        score += float(r["score"])
        #print(float(r["score"]))
    
    return score/2
    
def custom_test():
    #"resume_sr_ds.pdf7aebda6f-4199-408a-9427-19793fd77fda"
    #"resume_Devon Conrad.pdf2a356c99-19d6-4f3e-adea-f728240804b2"
    #"resume_Achuth_CV_IND.pdf244ebcfc-919d-492c-93ba-db40783b8b72"
    #resume_Jane Smith.pdf25a7e4aa-8a36-4fcb-b289-2315efee7ab4
    # To give your custom resume use this code
    resume_dict = read_json(#"resume_Kaitlyn.pdf1c87ae6c-c063-4d25-94e6-4ccdaf075b6c
        READ_RESUME_FROM + "resume_sr_ds.pdf7aebda6f-4199-408a-9427-19793fd77fda.json" 
        #""
    )
    job_dict = read_json(
       READ_JOB_DESCRIPTION_FROM + "job_description_Job Title.pdf8f1b24f0-8dbe-4f2d-817d-f7882be4c16c.json"
    )
    resume_keywords = resume_dict["extracted_keywords"] + resume_dict["entities"]
    job_description_keywords = job_dict["extracted_keywords"] + job_dict["entities"]
    
    rs=get_top_words_based_on_tfidf_scores(resume_dict["clean_data"])
    resume_keywords_t = resume_keywords + rs
    
    js=get_top_words_based_on_tfidf_scores(job_dict["clean_data"])
    job_description_keywords_t = job_description_keywords + js

    #----------------with using keyterms ------------------
    # res_keys=[]
    # li = resume_dict["keyterms"]
    # for k in li:
    #     res_keys.append(k[0])
    # print(res_keys)
    # resume_keywords_test = resume_keywords + list(set(res_keys))
    # print("***"*30)
    # res_keys=[]
    # li = job_dict["keyterms"]
    # for k in li:
    #     res_keys.append(k[0])
    # print(res_keys)
    # job_description_keywords_test = job_description_keywords + list(set(res_keys))
    
    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    
    # -------------------with tfidf--------------------
    # rs_t=" ".join(resume_keywords_t)
    # js_t=" ".join(job_description_keywords_t)
    
    # print("***"*30)
    # final_result = get_score(resume_string, jd_string)
    # for r in final_result:
    #     print(float(r.score))
        
    # print("---"*30)
    # res1=do_tfidf(rs_t)
    # res2=do_tfidf(js_t)
    # final_result = get_score(res1, res2)
    # for r in final_result:
    #     print(float(r.score))
    
    print("*"*30)
    final_result = get_similarity_score(resume_string, jd_string)
    for r in final_result:
        print(float(r["score"]))
    
    # print("---"*30)
    # final_result = get_similarity_score(res1, res2)
    # for r in final_result:
    #     print(float(r["score"]))
        
    print("***"*30)
    res1=do_tfidf(' '.join(resume_keywords))
    res2=do_tfidf(' '.join(job_description_keywords))
    final_result = get_similarity_score(res1, res2)
    for r in final_result:
        print(float(r["score"]))
    
    # print("---"*30)
    # final_result = get_tfidf_score(resume_string, jd_string)

    print("***"*30)
    t1 = resume_dict["clean_data"]
    t2 = job_dict["clean_data"]
    sc=get_similarity_tfidf(t1,t2)
    print(sc)
    


if __name__ == "__main__":
    custom_test()
