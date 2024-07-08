# Display results
import streamlit as st
st.title("Similarity Scores")
if 'names' in st.session_state and 'scores' in st.session_state:
    names = st.session_state['names']
    scores = st.session_state['scores']
    job_d = st.session_state['job_d']  
    resumes = st.session_state['resumes'] 
    # Display results in a table
    results = {"Resume File": names, "Score": [scores[name] for name in names]}
    st.table(results)
else:
    st.write("No results to display. Please upload files and process them on the main page.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import nltk
import re
from typing import List

def annotate_text_with_highlight(input_text: str, highlight_words: List[str], annotation: str, highlight_color: str) -> str:
    highlight_set = set(highlight_words)
    highlight_corpus = ' '.join(highlight_set)
    tokens = nltk.word_tokenize(input_text)
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if token not in set(stopwords)]
    annotated_tokens = []

    for token in tokens:
        if (token.isalpha() == True) and (re.search(token, highlight_corpus) is not None):
            annotated_tokens.append(f'<span style="background-color: {highlight_color}; border-radius: 4px; padding: 2px;"> {token} </span><span style="font-size: smaller; color: gray;"> ({annotation})</span>')
        else:
            annotated_tokens.append(token)

    return ' '.join(annotated_tokens)


if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

def res():
    if ('names' not in st.session_state) or ('scores' not in st.session_state) or ('job_d' not in st.session_state) or ('resumes' not in st.session_state):
        st.write("Please analyze the resumes from the Home page first.")
        return
    st.markdown("#### Job Description")
    job_ds_key = list(st.session_state['job_d'].keys())
    selected_jd = st.session_state['job_d'][job_ds_key[0]]
    st.write(selected_jd["clean_data"])
    annotation = "important"
    highlight_color = "#FFD700"
    names = st.session_state['names']
    scores = st.session_state['scores']
    results = {"Resume File": names, "Score": [scores[name] for name in names]}
    st.table(results)
    annotated_text_res1 = annotate_text_with_highlight(selected_jd["clean_data"], selected_jd["extracted_keywords"] + selected_jd["entities"], annotation, highlight_color)
    st.markdown(annotated_text_res1, unsafe_allow_html=True)
    #avs.add_vertical_space(7)
    
    current_index = st.session_state.get('current_index', 0)
    num_resumes = len(st.session_state['names'])

    st.title("Results")

    st.write(f"Displaying resume {current_index + 1} of {num_resumes}")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous Resume"):
            if current_index > 0:
                current_index -= 1
                st.session_state['current_index'] = current_index
                st.experimental_rerun()
    with col3:
        if st.button("Next Resume"):
            if current_index < num_resumes - 1:
                current_index += 1
                st.session_state['current_index'] = current_index
                st.experimental_rerun()

    selected_file = st.session_state['resumes'][st.session_state['names'][current_index]]

    # Displaying resume data
    st.markdown("#### Parsed Resume Data #####")
    st.write(selected_file["clean_data"])

    annotated_text_res = annotate_text_with_highlight(
        selected_file["clean_data"],
        selected_file["extracted_keywords"] + selected_file["entities"],
        annotation,
        highlight_color,
    )
    st.markdown(annotated_text_res, unsafe_allow_html=True)

    st.write("Now let's take a look at the extracted keywords from the resume.")

    df2 = pd.DataFrame(selected_file["keyterms"], columns=["keyword", "value"])
    df2["value"] = df2["value"] * 100
    color_scale = ['#66C2A5', '#8DA0CB']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df2["keyword"],
        y=df2["value"],
        marker_color=[color_scale[int(val > 80)] for val in df2["value"]],
        text=df2["value"].apply(lambda x: f'{x:.2f}%'),
        textposition='outside',
    ))
    fig.update_layout(
        title="Keyword Values",
        xaxis_title="Keywords",
        yaxis_title="Value (%)",
        plot_bgcolor='#f0f0f0',
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.treemap(
        df2,
        path=["keyword"],
        values="value",
        color_continuous_scale="Rainbow",
        title="Key Terms/Topics Extracted from your Resume",
    )
    st.write(fig)
    st.write("JOB TITLE:\n")

    st.markdown("#### Common Words between Job Description and Resumes Highlighted.")

    annotated_text_res2 = annotate_text_with_highlight(selected_file["clean_data"], selected_jd["extracted_keywords"] + selected_jd["entities"], annotation, highlight_color)
    st.markdown(annotated_text_res2, unsafe_allow_html=True)

    # if st.button("Back to Home"):
    #     st.query_params["page"]="Home"
        #st.experimental_rerun()

# Call the results function to display the page content
# results()
