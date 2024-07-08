import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

# Load the English model
nlp = spacy.load("en_core_web_md")

RESUME_SECTIONS = [
    "Contact Information",
    "Objective",
    "Summary",
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
    "Licenses",
    "Awards",
    "Honors",
    "Publications",
    "References",
    "Technical Skills",
    "Computer Skills",
    "Programming Languages",
    "Software Skills",
    "Soft Skills",
    "Language Skills",
    "Professional Skills",
    "Transferable Skills",
    "Work Experience",
    "Professional Experience",
    "Employment History",
    "Internship Experience",
    "Volunteer Experience",
    "Leadership Experience",
    "Research Experience",
    "Teaching Experience",
]

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b',
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
}

READ_RESUME_FROM = "Data/Resumes/"
SAVE_DIRECTORY_RESUME = "Data/Processed/Resumes"

READ_JOB_DESCRIPTION_FROM = "Data/JobDescription/"
SAVE_DIRECTORY_JOB_DESCRIPTION = "Data/Processed/JobDescription"

diction = []

class TextCleaner:
    
    def remove_emails_links(text):
        
        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], " ", text)
        return text

    def clean_text(text):
        text = TextCleaner.remove_spaces_between_words(text)
        # print("---"*20)
        # print(text)
        # print("---"*20)
        text = TextCleaner.remove_emails_links(text)
        # print("---"*20)
        # print(text)
        # print("---"*20)
        text = TextCleaner.remove_bulletpoints(text)
        # print("---"*20)
        # print(text)
        # print("---"*20)
        text = TextCleaner.Lemmatize_and_rm_stopwords(text)
        # print("---"*20)
        # print(text)
        # print("---"*20)
        tokens = word_tokenize(text)
        # print("---"*20)
        # print(tokens)
        # print("---"*20)
        text = TextCleaner.preserve_numbers(tokens)
        text=text.replace(r' .','.')
        text=text.replace(r'  ',' ')
        # print("---"*20)
        # print(text)
        # print("---"*20)
        doc = nlp(text)
        for token in doc:
            if token.pos_ == "PUNCT" and token.text!="." and (token.text.isalpha()==False):
                # print(f"TEXT --> {token.text}")
                #diction.append(token.text)
                text = text.replace(token.text, "")
          
        # print("---"*20)
        # print(text)
        # print("---"*20)
        return str(text)
    
    def remove_spaces_between_words(text):
        # a regex pattern to remove extra spaces between words
        pattern = r'\s+'
        
        # Use re.sub() to replace all occurrences of the pattern with no space
        cleaned_text = re.sub(pattern, ' ', text)
        return cleaned_text
    
    def Lemmatize_and_rm_stopwords (text):
        lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        words = [word for word in tokens if word not in stop_words and len(word)>0]
        tokens = [lemmatizer.lemmatize(token) for token in words ]
        
        cleaned_text = " ".join(tokens)
        return cleaned_text
    
    def preserve_numbers(tokens):
        for i in range(len(tokens)):
            res = TextCleaner.is_valid_number(tokens[i])
            if res==False :
              if len(tokens[i])<=1:
                #print(tokens[i])
                continue
              if tokens[i][len(tokens[i])-1]=='.':
                #print("1")
                tokens[i]=tokens[i][0:len(tokens[i])-1]

              if tokens[i][0]=='.':
                tokens[i]="0"+tokens[i].strip()

        return " ".join(tokens)
                
    
    def remove_bulletpoints(text):
        # Removing (•, ●, ○), hyphens, asterisks, and the diamond symbol. Here '○' is not alphabet(O). 
        cleaned_text = re.sub(r'[\u2022\u25CF\u25CB\-,*⋄+]', '', text)
        #print(cleaned_text)
        # Removing Numberings.
        pattern = r'^\s*(\d+\.\s+|\d+\)\s+|[a-zA-Z]\.\s+|[a-zA-Z]\)\s+|[\*\-\•]\s*)'
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.MULTILINE)
        #print(cleaned_text)
        # Removing Brackets
        pattern = r'[\[\]\(\)\{\}\<\>]'
        cleaned_text = re.sub(pattern, '', cleaned_text)
        # Removing Extra Spaces
        cleaned_text = re.sub('\s+',' ',cleaned_text)
        return cleaned_text.strip()
        
    def is_valid_number(s):
        pattern = re.compile(r'^-?\d+(\.\d+)?$')
        return bool(pattern.match(s))
    
class CountFrequency:
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)

    def count_frequency(self):
        pos_freq = {}
        for token in self.doc:
            if token.pos_ in pos_freq:
                pos_freq[token.pos_] += 1
            else:
                pos_freq[token.pos_] = 1
        return pos_freq
