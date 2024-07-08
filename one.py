import streamlit as st
from resume.resume_matcher.scripts.utils import read_multiple_pdf
from controller import do_everything
# Function to read text from uploaded file

def home():
    st.title("Job Description and Resume Similarity Checker")

    # Job description input
    st.header("Job Description")

    job_description_file = st.file_uploader("Upload job description file", type=["txt", "pdf", "docx"])
    # if job_description_file is not None:
    #     st.write(job_description_file.name)
    #     st.write(job_description_file.type)
        #job_description = read_file(job_description_file)

    # Upload multiple resumes
    st.header("Resume Files")

    uploaded_resumes = st.file_uploader("Upload resume files", type=["txt", "pdf", "docx"], accept_multiple_files=True, key="uploaded_resumes")
    # Ensure both job description and resumes are uploaded before calling the function
    start = st.button("START Processing",key="start")
    if start and job_description_file is not None and uploaded_resumes is not None and len(uploaded_resumes) > 0:
        
        names,job_d,resumes,scores=do_everything(job_description_file, uploaded_resumes)
        st.session_state['names'] = names
        st.session_state['scores'] = scores
        st.session_state['job_d'] = job_d
        st.session_state['resumes'] = resumes
        
        # Initialize session state for resume index
        if "current_resume_index" not in st.session_state:
            st.session_state.current_resume_index = 0

        # Display buttons to show resumes

        st.subheader(f"Number of uploaded resumes: {len(uploaded_resumes)}")

        # Previous and Next buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Previous"):
                if st.session_state.current_resume_index > 0:
                    st.session_state.current_resume_index -= 1
        
        with col3:
            if st.button("Next"):
                if st.session_state.current_resume_index < len(uploaded_resumes) - 1:
                    st.session_state.current_resume_index += 1

        # Display the current resume
        resume_index = st.session_state.current_resume_index
        st.subheader(f"Resume {resume_index + 1}")
        selected_file = resumes[names[resume_index]]
        resume_text = selected_file["clean_data"]
        st.write(resume_text)
        #st.text(resume_text)    
    else:
        st.write("Please upload at least one resume.")


