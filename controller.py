# from resume.user_app.reader import read_multiple_files
import PyPDF2
from resume.user_app.process_jd import Process_JOB
from resume.user_app.process_resumes import Process_Files
from resume.user_app.scorer import get_final_score

def read_multiple_files(files,file_type,file_names) -> dict:

        output = {}
        for i,file in enumerate(files):
            
            try:
                file_name = file_names[i]
                
                # if file_type[i] == "text/plain":
                #     output[file_name + str(i+1)] = str(file.read(), "utf-8")
                # elif 
                if file_type[i] == "application/pdf":
                    print("\n\n-------------------yes------------------\n\n")
                pdf_data = []
                pdf_reader = PyPDF2.PdfReader(file)
                count = len(pdf_reader.pages)
                for i,page in enumerate(pdf_reader.pages):
                    pdf_data.append(page.extract_text())
                res = ' '.join(pdf_data)
                output[file_name + str(i+1)] = str(res)
                
            except Exception as e:
                print(f"Error reading file '{file}': {str(e)}")
            #     elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    
            #         doc = docx.Document(file)
            #         output[file_name + str(i+1)] = "\n".join([para.text for para in doc.paragraphs])
            #     else:
            #         raise UnsupportedFileTypeError(f"Unsupported file type: {file.type}")

            # except UnsupportedFileTypeError as e:
            #     print(f"Error: {str(e)}")    
                
            # except Exception as e:
            #     print(f"Error reading file '{file}': {str(e)}")
        return output   
    


def do_everything(jd_file ,resume_files):
    types = []
    names = []
    for i in range(len(resume_files)):
        types.append(resume_files[i].type)
        names.append(resume_files[i].name)
    # print(names)
    # print(types)
    # return
    print(type(resume_files))
    print(type(jd_file))
    
    output_jobs = read_multiple_files([jd_file],[jd_file.type],[jd_file.name])
    output_resumes = read_multiple_files(resume_files,types,names)
    print(f"\n\nOUTPUT RESUMES :{output_resumes}\n\n")
    job_ds = Process_JOB(output_jobs).clean_and_extract()
    print(f"\n\nJOB DS : {job_ds}\n\n")
    resumes = Process_Files(output_resumes).clean_and_extract()
    print(f"\n\nRESUMES :{resumes}\n\n")
    scores = get_final_score(job_ds,resumes)
    print(f"\n\nSCORES :{scores}\n\n")
    
    resume_names = list(output_resumes.keys())
    return resume_names,job_ds,resumes,scores