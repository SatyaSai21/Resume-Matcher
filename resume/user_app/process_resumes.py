from resume.user_app.reader import read_multiple_files
from resume.resume_matcher.dataextractor.Data_Extractor import DataExtractor
from resume.resume_matcher.scripts.parser import ParseDocumentToJson


files_data = read_multiple_files

class Process_Files():
    def __init__(self,data):
        self.files_data=data
    
    def clean_and_extract(self):
        
        json_data = dict()
        for key,file_data in self.files_data.items():
            parsed_data = ParseDocumentToJson(file_data,"resume").get_JSON()
            json_data[key] = parsed_data
        return json_data


