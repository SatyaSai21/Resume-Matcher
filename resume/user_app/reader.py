import PyPDF2
# import docx

# class UnsupportedFileTypeError(Exception):
#     """Custom exception for unsupported file types."""
#     pass
#     #print("\nUnsupported file type\n")

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
            output[file_name + str(i+1)] = ' '.join(pdf_data)
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

# def read_multiple_files(files: list,file_type : str) -> dict:
    
#     output = {}
#     output["file_type"] = file_type
#     output["data"] = dict({})
#     for i,file in enumerate(files):
#         try:
#             file_name =  file.name
#             if file.type == "text/plain":
                 
#                 output["data"][file_name + str(i+1)] = str(file.read(), "utf-8")    
#             elif file.type == "application/pdf":
                
#                 pdf_data = []
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 count = len(pdf_reader.pages)
#                 for i,page in enumerate(pdf_reader.pages):
#                     pdf_data.append(page.extract_text())
#                 output["data"][file_name + str(i+1)] = ' '.join(pdf_data)
#             elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                
#                 doc = docx.Document(file)
#                 output["data"][file_name + str(i+1)] = "\n".join([para.text for para in doc.paragraphs])
#             else:
                
#                 raise UnsupportedFileTypeError(f"Unsupported file type: {file.type}")

#         except UnsupportedFileTypeError as e:
#             print(f"Error: {str(e)}")    
            
#         except Exception as e:
#             print(f"Error reading file '{file}': {str(e)}")
        
#     return output

