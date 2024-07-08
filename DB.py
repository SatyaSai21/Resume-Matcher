from qdrant_client import QdrantClient
import logging
from typing import List
logger = logging.getLogger(__name__)
# qdrant_client = QdrantClient(
#     url="https://0413c2b1-3d5c-4c4a-9222-cbb0b10ecdb3.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="MUnRHVqTwAEj-lYHnOH4725q6dQCQbRzJrd-tNTTM56jm5bGFbD5Aw",
# )

# print(qdrant_client.get_collections())
# collection_name = 'demo_collection'

#     # Retrieve points from the collection
# points = qdrant_client.scroll(
#         collection_name=collection_name,
#         scroll_filter=None,  # You can specify a filter if needed
#         limit=10  # Adjust the limit as needed
#     )

# print("Points in the collection:")
# for point in points:
#     print(point)
#     logger.info("Finished getting similarity score")


# # Initialize the Qdrant client
# client = QdrantClient(host='localhost', port=8501)
# print(client.get_collections())
resume_string = """ACHUTH KUMAR DATHA KOMPELLA 
+91 7702398219 ⋄ Hyderabad, Telangana. 
achuth.kompella@gmail.com ⋄ Linkedin ⋄ Github 
OBJECTIVE 
I am a learning enthusiast and a passionate student at IIEST (Indian Institute of Engineering Science and Technology), 
Shibpur, an eminent institute of national importance with a NIRF ranking of 35 in 2023 as published by the Ministry of 
Education, Government of India; Pursuing Bachelors in Computer Science and technology. I am constantly developing 
my skills and always open to new challenges and opportunities that allow me to grow professionally and personally. 
I am actively seeking internship opportunities. I am willing to go above and beyond in every position I take and aspire 
to stand out and have a meaningful impact on society. 
EDUCATION 
Indian Institute of Engineering Science and Technology, Shibpur, 
Bachelor of technology in Computer Science And Technology. 
Vikas The Concept School, Hyderabad 
Senior Secondary (CBSE). 
SKILLS 
December 2021 – July 2026 
CGPA - 5.49/10 
June. 2019 – March 2021 
76.6 percent 
C++, Python, Git and Github, Tensorflow, Deep Learning, Generative Adversarial Networks (GANs), Object
oriented programming System(OOPs), Data Structures And Algorithms Google Cloud Platform, VS Code, 
Jupyter Notebook. 
EXPERIENCE 
• Indian Institute Of Science Banglore(IISc), Internship — Certificate 
MAY 2023 - JULY 2023 
Objective: I have learned about optimization techniques such as Linear Programming, Particle Swarm Optimization 
(PSO),implementing them in Python and applied them to solve many benchmark problems and a real case study of 
optimal reservoir operation in India. Skills: Python, Jupyter Notebook 
• INFOSYS Limited, Internship — Certificate 
JAN 2023 - MAY 2023 
Objective: To enable Color Vision Deficiency(CVD) patients to identify images using Generative adversarial 
networks(GANs). I have developed an algorithm for the given complex dataset to create recolored images using 
deep learning techniques. This model is trained and tested using GAN. These recolored images are easily 
recognizable by CVD patients. 
Skills: Python, Tensorflow, Image Processing, Deep Learning, GAN. Key 
Learnings: Learned how to use AI techniques in real world 
EXTRA-CURRICULAR ACTIVITIES AND CERTIFICATES 
• CodeIIEST - The Coding Club Of IIEST Shibpur 
Member 
JUN 2022 - Present 
• Google Certified IT Automation With Python, Git-Github, and Cloud 
Certificate """
job_description_string = """Job Title: Data Scientist 
Location: San Francisco, CA 
Company: InnovateTech Solutions 
Type: Full-time 
Department: Data Science and Analytics 
About Us: 
InnovateTech Solutions is a leading technology company committed to transforming 
industries through innovative solutions and cutting-edge technology. Our mission is to drive 
progress and make a positive impact on the world. We are seeking a talented Data Scientist to 
join our dynamic team and help us harness the power of data to drive business decisions and 
improve our products and services. 
Job Description: 
As a Data Scientist at InnovateTech Solutions, you will play a critical role in analyzing 
complex data sets to help drive business decisions and improve our products and services. 
You will work closely with cross-functional teams, including product development, 
marketing, and operations, to uncover insights, build predictive models, and support data
driven strategies. 
Key Responsibilities: 
• Collect, clean, and preprocess large datasets from various sources. 
• Perform exploratory data analysis (EDA) to uncover trends, patterns, and insights. 
• Develop and implement predictive models and machine learning algorithms. 
• Design experiments and perform hypothesis testing to validate business strategies. 
• Communicate findings and insights through visualizations and presentations to 
stakeholders. 
• Collaborate with software engineers to integrate data-driven solutions into production 
systems. 
• Stay updated with the latest advancements in data science, machine learning, and AI. 
• Document processes, methodologies, and analyses for future reference. 
Requirements: 
• Education: Bachelor's or Master's degree in Data Science, Computer Science, 
Statistics, Mathematics, or a related field. 
• Experience: Minimum of 3 years of experience in data science, analytics, or a related 
field. 
• Technical Skills: 
o Proficiency in programming languages such as Python or R. 
o Experience with data manipulation and analysis libraries (e.g., Pandas, 
NumPy, Scikit-learn). 
o Strong knowledge of machine learning algorithms and frameworks (e.g., 
TensorFlow, PyTorch). 
o Experience with data visualization tools (e.g., Matplotlib, Seaborn, Tableau). 
o Familiarity with SQL and database management. 
• Analytical Skills: Excellent problem-solving abilities and a strong analytical mindset. 
• Communication: Strong verbal and written communication skills, with the ability to 
explain complex technical concepts to non-technical stakeholders. 
• Team Player: Ability to work collaboratively in a team environment and with cross
functional teams. 
• Attention to Detail: High level of accuracy and attention to detail in work. 
Preferred Qualifications: 
• Ph.D. in Data Science, Computer Science, Statistics, or a related field. 
• Experience with big data technologies (e.g., Hadoop, Spark). 
• Knowledge of cloud platforms (e.g., AWS, Google Cloud, Azure). 
• Experience with natural language processing (NLP) and computer vision. 
What We Offer: 
• Competitive salary and benefits package. 
• Opportunities for professional growth and development. 
• A collaborative and innovative work environment. 
• Flexible working hours and remote work options. 
• Employee wellness programs and on-site gym. 
• Stock options and performance bonuses. 
How to Apply: 
Please submit your resume, cover letter, and any relevant work samples or portfolio to 
hr@innovatetechsolutions.com with the subject line "Data Scientist Application - [RES]". 
Application Deadline: August 31, 2024 """
documents: List[str] = [resume_string]
client = QdrantClient(":memory:")
client.set_model("BAAI/bge-base-en")

client.add(
        collection_name="demo_collection",
        documents=documents,
    )

search_result = client.query(
        collection_name="demo_collection", query_text=job_description_string
    )
collection_name = 'demo_collection'

    # Retrieve points from the collection
points = client.scroll(
        collection_name=collection_name,
        scroll_filter=None,  # You can specify a filter if needed
        limit=10  # Adjust the limit as needed
    )

print("Points in the collection:")
for point in points:
    print(point)
    logger.info("Finished getting similarity score")