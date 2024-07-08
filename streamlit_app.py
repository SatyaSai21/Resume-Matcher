
import json
import os
from typing import List

import networkx as nx
import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from annotated_text import annotated_text, parameters
from streamlit_extras import add_vertical_space as avs

from resume.resume_matcher.scripts.get_similarity_score import *
from resume.resume_matcher.utils.ReadFiles import get_filenames_from_dir
from resume.resume_matcher.utils.logger import init_logging_config

# Set page configuration
st.set_page_config(
    page_title="Resume Matcher",
    initial_sidebar_state="auto",
)

init_logging_config()
cwd = find_path("Resume-Matcher")
config_path = os.path.join(cwd, "scripts", "similarity")

try:
    nltk.data.find("tokenizers/punkt")
    nltk.find("stopwords")
except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")

parameters.SHOW_LABEL_SEPARATOR = False
parameters.BORDER_RADIUS = 3
parameters.PADDING = "0.5 0.25rem"
import re
from typing import List

def annotate_text_with_highlight(input_text: str, highlight_words: List[str], annotation: str, highlight_color: str) -> str:
    """
    Annotate specified words in the input text with a highlight and annotation.

    Parameters:
    - input_text: The text to be processed.
    - highlight_words: A list of words to be highlighted and annotated.
    - annotation: The annotation text to add after the highlighted word.
    - highlight_color: The background color for the highlighted word.

    Returns:
    - Annotated text with HTML formatting.
    """
    # Convert the list to a set for quick lookups
    highlight_set = set(highlight_words)
    highlight_corpus = ' '.join(highlight_set)

    # Tokenize the input text
    tokens = nltk.word_tokenize(input_text)
    stopwords = nltk.corpus.stopwords.words('english')
    tokens=[token for token in tokens if token not in set(stopwords)]
    # Initialize an empty list to hold the annotated text
    annotated_tokens = []

    for token in tokens:
        
        if (token.isalpha()==True) and (re.search(token, highlight_corpus) is not None):
            annotated_tokens.append(f'<span style="background-color: {highlight_color}; border-radius: 4px; padding: 2px;"> {token} </span><span style="font-size: smaller; color: gray;"> ({annotation})</span>')
        else:

            annotated_tokens.append(token)

    # Join the annotated tokens into a single string with spaces
    return ' '.join(annotated_tokens)

annotation = "important"
highlight_color = "#FFD700"  # Light yellow color

def create_annotated_text(
    input_string: str, word_list: List[str], annotation: str, color_code: str
):
    
    # Convert the list to a set for quick lookups
    word_set = set(word_list)
    temp_corpus = ' '.join(word_set)
    # Tokenize the input string
    tokens = nltk.word_tokenize(input_string)

    # Initialize an empty list to hold the annotated text
    annotated_text = []

    for token in tokens:
        # Check if the token is in the set
        if re.search(token,temp_corpus) is not None:
            # If it is, append a tuple with the token, annotation, and color code
            annotated_text.append((' '+token+' ', annotation, color_code))
        else:
            # If it's not, just append the token as a string
            annotated_text.append(' '+token+' ')

    return annotated_text


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def tokenize_string(input_string):
    tokens = nltk.word_tokenize(input_string)
    return tokens


# Display the main title and subheaders
st.title(":blue[Resume Matcher]")

st.divider()
avs.add_vertical_space(1)

resume_names = get_filenames_from_dir("Data/Processed/Resumes")


st.markdown(
    f"##### There are {len(resume_names)} resumes present. Please select one from the menu below:"
)
output = st.selectbox(f"SELECT A RESUME", resume_names)


avs.add_vertical_space(5)

# st.write("You have selected ", output, " printing the resume")
selected_file = read_json("Data/Processed/Resumes/" + output)

avs.add_vertical_space(2)
st.markdown("#### Parsed Resume Data")
st.caption(
    "This text is parsed from your resume. This is how it'll look like after getting parsed by an ATS."
)
st.caption("Utilize this to understand how to make your resume ATS friendly.")
avs.add_vertical_space(3)
# st.json(selected_file)
st.write(selected_file["clean_data"])

avs.add_vertical_space(3)
annotated_text_res = annotate_text_with_highlight(selected_file["clean_data"], selected_file["extracted_keywords"] + selected_file["entities"], annotation, highlight_color)
st.markdown(annotated_text_res, unsafe_allow_html=True)
avs.add_vertical_space(7)
st.write("Now let's take a look at the extracted keywords from the resume.")

annotated_text(
    create_annotated_text(
        selected_file["clean_data"],
        selected_file["extracted_keywords"] + selected_file["entities"],
        "keyword",
        "#FFD700",
    )
)

avs.add_vertical_space(5)

# Call the function with your data
# create_star_graph(selected_file["keyterms"], "Entities from Resume")

df2 = pd.DataFrame(selected_file["keyterms"], columns=["keyword", "value"])
df2["value"] = df2["value"]*100
# Define color scale based on value
color_scale = ['#66C2A5', '#8DA0CB'] # Red and Green

# Create Plotly figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=df2["keyword"],
    y=df2["value"],
    marker_color=[color_scale[int(val > 80)] for val in df2["value"]],
    text=df2["value"].apply(lambda x: f'{x:.2f}%'),
    textposition='outside',  # Place text outside the bars
))

# Update layout for better appearance
fig.update_layout(
    title="Keyword Values",
    xaxis_title="Keywords",
    yaxis_title="Value (%)",
    plot_bgcolor='#f0f0f0',  # Background color
)

# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True)

st.divider()

fig = px.treemap(
    df2,
    path=["keyword"],
    values="value",
    color_continuous_scale="Rainbow",
    title="Key Terms/Topics Extracted from your Resume",
)
st.write(fig)

avs.add_vertical_space(5)

job_descriptions = get_filenames_from_dir("Data/Processed/JobDescription")


st.markdown(
    f"##### There are {len(job_descriptions)} job descriptions present. Please select one from the menu below:"
)
output = st.selectbox("SELECT YOUR JOB DESCRIPTION", job_descriptions)


avs.add_vertical_space(5)

selected_jd = read_json("Data/Processed/JobDescription/" + output)

avs.add_vertical_space(2)
st.markdown("#### Job Description")

avs.add_vertical_space(3)
# st.json(selected_file)
st.write(selected_jd["clean_data"])
avs.add_vertical_space(3)
st.write("JOB TITLE:\n")
annotated_text_res1 = annotate_text_with_highlight(selected_jd["clean_data"], selected_jd["extracted_keywords"] + selected_jd["entities"], annotation, highlight_color)
st.markdown(annotated_text_res1, unsafe_allow_html=True)
avs.add_vertical_space(7)
st.markdown("#### Common Words between Job Description and Resumes Highlighted.")

annotated_text_res2 = annotate_text_with_highlight(selected_file["clean_data"], selected_jd["extracted_keywords"] + selected_jd["entities"], annotation, highlight_color)
st.markdown(annotated_text_res2, unsafe_allow_html=True)

annotated_text(
    create_annotated_text(
        selected_file["clean_data"], selected_jd["extracted_keywords"] + selected_jd["entities"], " keyword ","#87CEEB",
    )
)

st.write("Now let's take a look at the extracted entities from the job description.")

# Call the function with your data
# create_star_graph(selected_jd["keyterms"], "Entities from Job Description")

df2 = pd.DataFrame(selected_jd["keyterms"], columns=["keyword", "value"])

# Create the dictionary
keyword_dict = {}
for keyword, value in selected_jd["keyterms"]:
    keyword_dict[keyword] = value * 100

fig = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["Keyword", "Value"], font=dict(size=12), fill_color="#070A52"
            ),
            cells=dict(
                values=[list(keyword_dict.keys()), list(keyword_dict.values())],
                line_color="darkslategray",
                fill_color="#6DA9E4",
            ),
        )
    ]
)
st.plotly_chart(fig)

st.divider()

fig = px.treemap(
    df2,
    path=["keyword"],
    values="value",
    color_continuous_scale="Rainbow",
    title="Key Terms/Topics Extracted from the selected Job Description",
)
st.write(fig)

avs.add_vertical_space(3)

resume_string = " ".join(selected_file["extracted_keywords"])
jd_string = " ".join(selected_jd["extracted_keywords"])
result = get_similarity_score(resume_string, jd_string)
similarity_score = round(result[0]["score"] * 100, 2)
score_color = "green"
if similarity_score < 60:
    score_color = "red"
elif 60 <= similarity_score < 75:
    score_color = "orange"
st.markdown(
    f"Similarity Score obtained for the resume and job description is "
    f'<span style="color:{score_color};font-size:24px; font-weight:Bold">{similarity_score}</span>',
    unsafe_allow_html=True,
)

# Go back to top
st.markdown("[:arrow_up: Back to Top](#resume-matcher)")
