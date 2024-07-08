from resume.resume_matcher.scripts.get_score import get_score_pair
#from resume.resume_matcher.scripts.utils import read_json
import json

def get_final_score(jd,resumes):
    scores = dict({})
    jd_file_name = list(jd.keys())[0]
    job_dict = jd[jd_file_name]
    job_string = job_dict["extracted_keywords"] + job_dict["entities"]
    job_string = ' '.join(job_string)
    resume_file_names =  list(resumes.keys())
    print(resume_file_names )
    for resume in resume_file_names:
        scores[resume] =  dict({})
        #resume_dict = read_json(resumes[resume])
        resume_dict = resumes[resume]
        resume_string = resume_dict["extracted_keywords"] + resume_dict["entities"]
        resume_string = ' '.join(resume_string)
        print(f"DATA : {resume_string}")
        score =  get_score_pair(resume_string,job_string)
        scores[resume] = score
    
    return scores

        
        
    