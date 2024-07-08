import re
import urllib

import spacy

from resume.resume_matcher.dataextractor.Text_Cleaner import TextCleaner


nlp = spacy.load("en_core_web_sm")

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
RESUME_SECTIONS = [ section.upper() for section in RESUME_SECTIONS]

class DataExtractor:
    """
    A class for extracting various types of data from text.
    """

    def __init__(self, raw_text: str):
        """
        Initialize the DataExtractor object.

        Args:
            raw_text (str): The raw input text.
        """

        self.text = raw_text
        
        self.clean_text = TextCleaner.clean_text(self.text.lower())
        self.doc = nlp(self.clean_text)

    def extract_links(self):
        """
        Find links of any type in a given string.

        Args:
            text (str): The string to search for links.

        Returns:
            list: A list containing all the found links.
        """
        link_pattern = r"\b(?:https?://|www\.)\S+\b"
        links = re.findall(link_pattern, self.text)
        return links

    def extract_links_extended(self):
        """
        Extract links of all kinds (HTTP, HTTPS, FTP, email, www.linkedin.com,
          and github.com/user_name) from a webpage.

        Args:
            url (str): The URL of the webpage.

        Returns:
            list: A list containing all the extracted links.
        """
        links = []
        try:
            response = urllib.request.urlopen(self.text)
            html_content = response.read().decode("utf-8")
            pattern = r'href=[\'"]?([^\'" >]+)'
            raw_links = re.findall(pattern, html_content)
            for link in raw_links:
                if link.startswith(
                    (
                        "http://",
                        "https://",
                        "ftp://",
                        "mailto:",
                        "www.linkedin.com",
                        "github.com/",
                        "twitter.com",
                    )
                ):
                    links.append(link)
        except Exception as e:
            print(f"Error extracting links: {str(e)}")
        return links

    def extract_names(self):
        """Extracts and returns a list of names from the given
        text using spaCy's named entity recognition.

        Args:
            text (str): The text to extract names from.

        Returns:
            list: A list of strings representing the names extracted from the text.
        """
        names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        return names

    def extract_emails(self):
        """
        Extract email addresses from a given string.

        Args:
            text (str): The string from which to extract email addresses.

        Returns:
            list: A list containing all the extracted email addresses.
        """
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        emails = re.findall(email_pattern, self.text)
        return emails

    def extract_phone_numbers(self):
        """
        Extract phone numbers from a given string.

        Args:
            text (str): The string from which to extract phone numbers.

        Returns:
            list: A list containing all the extracted phone numbers.
        """
        pattern = r'[\+\-\(\)]'
        text_data = re.sub(pattern, '', self.text)
        pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b'
        phone_numbers = re.findall(pattern, text_data)
        for i in range(len(phone_numbers)):
            phone_no=phone_numbers[i].split(' ')
            if len(phone_no)>1:
                #print(i.split(' ')[1])
                if len(phone_no[1])==10:
                    phone_numbers[i]=phone_no[1]
                phone_numbers[i] = re.sub(r'\s','',phone_numbers[i])
        return phone_numbers

    def extract_experience(self):
        """
        Extract experience from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract experience.

        Returns:
            str: A string containing all the extracted experience.
        """
        experience_section = []
        in_experience_section = False
        
        for token in self.doc:
            if token.text.upper() in RESUME_SECTIONS:
                if token.text.upper()  == "Experience" or "EXPERIENCE" or "experience":
                    in_experience_section = True
                else:
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(token.text)

        return " ".join(experience_section)

    def find_resume_sections_in_text(self):
        prsent = []
        for word in RESUME_SECTIONS:
            # Create a pattern that matches the exact word with word boundaries
            pattern = fr'\b{re.escape(word)}\b'
            # Search for the pattern in the text
            if re.search(pattern, self.clean_text, re.IGNORECASE):
                prsent.append(word.strip())
        return prsent
    
    def extract_position_year(self):
        """
        Extract position and year from a given string.

        Args:
            text (str): The string from which to extract position and year.

        Returns:
            list: A list containing the extracted position and year.
        """
        position_year_search_pattern = (
            r"(\b\w+\b\s+\b\w+\b),\s+(\d{4})\s*-\s*(\d{4}|\bpresent\b)"
        )
        position_year = re.findall(position_year_search_pattern, self.text)
        return position_year

    def extract_particular_words(self):
        """
        Extract nouns and proper nouns from the given text.

        Args:
            text (str): The input text to extract nouns from.

        Returns:
            list: A list of extracted nouns.
        """
        pos_tags = ["NOUN", "PROPN"]
        nouns = [token.text for token in self.doc if token.pos_ in pos_tags]
        return nouns
    
    def extract_entities(self):
        """
        Extract named entities of types 'GPE' (geopolitical entity) and 'ORG' (organization) from the given text.

        Args:
            text (str): The input text to extract entities from.

        Returns:
            list: A list of extracted entities.
        """
        entity_labels = ["GPE", "ORG"]
        entities = [
            token.text for token in self.doc.ents if token.label_ in entity_labels
        ]
        for i,entity in enumerate(entities):
            entities[i] = re.sub('\s+',' ', entity).strip()
        return list(set(entities))
    def extract_entities_updated(self):
        """
        Extract named entities of types 'GPE' (geopolitical entity) and 'ORG' (organization) from the given text.

        Args:
            text (str): The input text to extract entities from.

        Returns:
            list: A list of extracted entities.
        """
        #nlp1 = spacy.load("en_core_web_sm")
        doc1=nlp(self.text)

        entity_labels = ["GPE", "ORG","PRODUCT","PERCENT"]
        entities = [
            token.text for token in self.doc.ents if token.label_ in entity_labels
        ]
        
        temp_st=self.find_resume_sections_in_text()
        for wo in temp_st:
            entities.append(wo.upper())
        
        for i,entity in enumerate(entities):
            entities[i] = re.sub('\s+',' ', entity).strip()
        
        entities=set(entities)
        entities_new=[
            token.text for token in doc1.ents if token.label_ in entity_labels
        ]
        for i,entity in enumerate(entities_new):
            entities_new[i] = TextCleaner.clean_text(entity).strip()
             #entities[i] = re.sub('\s+',' ', entity).strip()
        
        #print(entities)
        entities_new=set(entities_new)
        #print(entities_new)
        entities.update(entities_new)
        #print(entities)
        return list(set(entities))
