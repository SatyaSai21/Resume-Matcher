from resume.resume_matcher.scripts.parser import ParseDocumentToJson

class Process_JOB():
    def __init__(self,data):
        self.files_data=data
    
    def clean_and_extract(self):
        
        json_data = dict()
        for k,file_data in self.files_data.items():
            print(type(self.files_data))
            parsed_data = ParseDocumentToJson(file_data,"job_description").get_JSON()
            json_data[k] = parsed_data
        return json_data