import glob
import json
import logging
import os
import os.path
from uuid import uuid4

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def find_path(folder_name):
    
    curr_dir = os.getcwd()
    while True:
        if folder_name in os.listdir(curr_dir):
            return os.path.join(curr_dir, folder_name)
        else:
            parent_dir = os.path.dirname(curr_dir)
            if parent_dir == "/":
                break
            curr_dir = parent_dir
    raise ValueError(f"Folder '{folder_name}' not found.")


def read_json(path):
    
    with open(path) as f:
        try:
            data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            data = {}
    return data


def read_multiple_pdf(file_path: str) -> list:
    
    pdf_files = get_pdf_files(file_path)
    output = []
    for file in pdf_files:
        try:
            pdf_data = []
            with open(file, "rb") as f:
                pdf_reader = PdfReader(f)
                count = len(pdf_reader.pages)
                for i,page in enumerate(pdf_reader.pages):
                    pdf_data.append(page.extract_text())
            output.append(' '.join(pdf_data))
        except Exception as e:
            print(f"Error reading file '{file}': {str(e)}")
        
    return output


def read_single_pdf(file_path: str) -> str:
    
    output = []
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            count = len(pdf_reader.pages)
            for i,page in enumerate(pdf_reader.pages):
                output.append(page.extract_text())
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
    return str(" ".join(output))


def get_pdf_files(file_path: str) -> list:
    
    pdf_files = []
    try:
        pdf_files = glob.glob(os.path.join(file_path, "*.pdf"))
    except Exception as e:
        print(f"Error getting PDF files from '{file_path}': {str(e)}")
    return pdf_files


def generate_unique_id():
    
    return str(uuid4())


def get_filenames_from_dir(directory_path: str) -> list:
    filenames = [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f)) and f != ".DS_Store"
    ]
    return filenames
