import json
import logging
import os

from numpy import vectorize
import yaml
import cohere
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Batch
from resume.resume_matcher.utils.Similar import match
from resume.resume_matcher.utils.logger import get_handlers,init_logging_config
from resume.resume_matcher.utils.tf_idf import do_tfidf,get_vectors
from sklearn.metrics.pairwise import cosine_similarity


init_logging_config(basic_log_level=logging.INFO)
# Get the logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)

stderr_handler, file_handler = get_handlers()


def find_path(folder_name):
   
    curr_dir = os.getcwd()##get the current working directory
    while True:
        if folder_name in os.listdir(curr_dir):
            return os.path.join(curr_dir, folder_name)
        else:
            parent_dir = os.path.dirname(curr_dir)
            if parent_dir == "/":
                break
            curr_dir = parent_dir
    raise ValueError(f"Folder '{folder_name}' not found.")


cwd = find_path("Resume-Matcher")
READ_RESUME_FROM = os.path.join(cwd, "Data", "Processed", "Resumes")
READ_JOB_DESCRIPTION_FROM = os.path.join(cwd, "Data", "Processed", "JobDescription")
config_path = os.path.join(cwd, "scripts", "similarity")


def read_config(filepath):
    """
    Reads a configuration file in YAML format and returns the parsed configuration.

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        dict: The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        yaml.YAMLError: If there is an error parsing the YAML in the configuration file.
        Exception: If there is an error reading the configuration file.

    """
    try:
        with open(filepath) as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError as e:
        logger.error(f"Configuration file {filepath} not found: {e}")
    except yaml.YAMLError as e:
        logger.error(
            f"Error parsing YAML in configuration file {filepath}: {e}", exc_info=True
        )
    except Exception as e:
        logger.error(f"Error reading configuration file {filepath}: {e}")
    return None


def read_doc(path):
    """
    Read a JSON file and return its contents as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.

    Raises:
        Exception: If there is an error reading the JSON file.
    """
    with open(path) as f:
        try:
            data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            data = {}
    return data


# This class likely performs searches based on quadrants.
class QdrantSearch:
    def __init__(self, resumes, jd):
        """
        The function initializes various parameters and clients for processing resumes and job
        descriptions.

        Args:
          resumes: The `resumes` parameter in the `__init__` method seems to be a list of resumes that
        is passed to the class constructor. It is likely used within the class for some processing or
        analysis related to resumes. If you have any specific questions or need further assistance with
        this parameter or any
          jd: The `jd` parameter in the `__init__` method seems to represent a job description. It is
        likely used as input to compare against the resumes provided in the `resumes` parameter. The job
        description is probably used for matching and analyzing against the resumes in the system.
        """
        #config = read_config(config_path + "/config.yml")
        self.cohere_key = "R7EUx8jTIXQ9BWRNEmj1FsqJ5DAfJWHcjzM8MblC"#config["cohere"]["api_key"]
        self.qdrant_key = "MUnRHVqTwAEj-lYHnOH4725q6dQCQbRzJrd-tNTTM56jm5bGFbD5Aw"#config["qdrant"]["api_key"]
        self.qdrant_url = "https://0413c2b1-3d5c-4c4a-9222-cbb0b10ecdb3.us-east4-0.gcp.cloud.qdrant.io"#config["qdrant"]["url"]
        self.resumes = resumes
        self.jd = jd
        self.cohere = cohere.Client(self.cohere_key)
        self.collection_name = "resume_collection_name"
        self.qdrant = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_key,
        )

        vector_size = 4096 #--->embed-english-v2.0
        #vector_size=1024 #--->embed-english-v3.0
        # vector_size = 786
        print(f"collection name={self.collection_name}")
        self.qdrant.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )

        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.addHandler(stderr_handler)
        self.logger.addHandler(file_handler)

    def get_embedding(self, text):
        
        try:#"embed-english-v3.0"
            res = self.cohere.embed(texts=[text],model="embed-english-v2.0",input_type="search_query",embedding_types=['float'])
            #print(res)#API RESPONSE 
            #we mentioned the type of embedding is float,so using _float
            embedding=res.embeddings.float_ 
            #print(f"LENGTH 1 :{embedding}")
            return list(map(float, embedding[0])), len(embedding[0])
        except Exception as e:
            self.logger.error(f"Error getting embeddings: {e}", exc_info=True)

    def update_qdrant(self):
        """
        This Python function updates vectors and corresponding metadata in a Qdrant collection based on
        resumes.
        """
        vectors = []
        ids = []
        for i, resume in enumerate(self.resumes):
            vector, size = self.get_embedding(resume)
            vectors.append(vector)
            ids.append(i)
        try:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=Batch(
                    ids=ids,
                    vectors=vectors,
                    payloads=[{"text": resume} for resume in self.resumes],
                ),
            )
        except Exception as e:
            self.logger.error(
                f"Error upserting the vectors to the qdrant collection: {e}",
                exc_info=True,
            )

    def search(self):
        
        vector, _ = self.get_embedding(self.jd)

        hits = self.qdrant.search(
            collection_name=self.collection_name, query_vector=vector, limit=30
        )
        results = []
        for hit in hits:
            result = {"text": str(hit.payload)[:30], "score": hit.score}
            results.append(result)

        return results
#####################################################################################################################
#############################------USING BERT-----------#############################
# def semantic_similarity_bert_base_nli_mean_tokens(job,resume):
#     """calculate similarity with bert_base_nli_mean_tokens"""
#     model = SentenceTransformer('bert-base-nli-mean-tokens')
#     #Encoding:
#     score = 0
#     sen = job+resume
#     sen_embeddings = model.encode(sen)
#     for i in range(len(job)):
#         if job[i] in resume:
#             score += 1
#         else:
#             if max(cosine_similarity([sen_embeddings[i]],sen_embeddings[len(job):])[0]) >= 0.4:
#                 score += max(cosine_similarity([sen_embeddings[i]],sen_embeddings[len(job):])[0])
#     score = score/len(job)  
#     return round(score,3)

########################################################################################################################

def get_tfidf_score(resume_string,jd_string):
    res1=do_tfidf(resume_string)
    res2=do_tfidf(jd_string)
    print("------------------TFIDF----------------------\n")
    print(match(res1,res2))

def get_similarity_tfidf(resume_string,jd_string):
    tfidf_matrix = get_vectors(resume_string,jd_string)
    score=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])
    return score[0][0]

def get_similarity_score(resume_string, job_description_string):
    #print(f"\n\nMATCH----------------> :{match(resume_string, job_description_string)}\n\n")
    logger.info("Started getting similarity score")
    qdrant_search = QdrantSearch([resume_string], job_description_string)
    qdrant_search.update_qdrant()
    search_result = qdrant_search.search()
    logger.info("Finished getting similarity score")
    return search_result


if __name__ == "__main__":
    # To give your custom resume use this code
    resume_dict = read_doc(
        READ_RESUME_FROM
        + "/resume_Achuth_CV_IND.pdf1bd14bd4-01c1-4700-b14e-ffedb4985104.json"
    )
    job_dict = read_doc(
        READ_JOB_DESCRIPTION_FROM
        + "/job_description_Job Title.pdfafaad93b-289e-4aa0-8530-22c55d97c3c0.json"
    )
    resume_keywords = resume_dict["extracted_keywords"]
    job_description_keywords = job_dict["extracted_keywords"]

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    res1=do_tfidf(resume_string)
    res2=do_tfidf(jd_string)
    print("------------------TFIDF----------------------\n")
    print(match(res1,res2))
    print("------------------------------------------\n")
    print(match(resume_string, jd_string))
    print("-----------------GET SIMILARITY-------------------------\n")
    final_result = get_similarity_score(resume_string, jd_string)
    for r in final_result:
        print(r)
    print("------------------------------------------\n")
    final_result = get_similarity_score(res1, res2)
    for r in final_result:
        print(r)
    print("------------------------------------------\n")
    print("--------------------TFIDF VECTOR SCORE----------------------\n")
    score = get_similarity_tfidf(jd_string,resume_string)
    print(score)

