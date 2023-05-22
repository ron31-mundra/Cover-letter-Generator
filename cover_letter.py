import streamlit  as st
import openai as ai
import time
from dotenv import load_dotenv
import os


print("** Loading API Key")

load_dotenv()
ai.api_key= os.getenv("OPENAI_API_KEY")    #create a environment variable (OPENAI_API_KEY) and assign your openai api key to it


st.title("Ai Cover Letter Generator")
st.markdown("# Lazy Apply")

with st.sidebar: 
    st.title("Quick Guide!!")
    st.markdown("## 1. What is a Cover Letter Generator?")
    st.write("A Cover letter generator is a AI based tool that is used to generate personalized cover letter for each job posting based on the information you tell it. The AI cover letter generator is trained on millions of cover letter templates to generate a personalised catchy and convincing cover letter for each job post.")
    st.markdown("## 2. How do I use the Cover Letter ai?")
    st.write("using cover letter ai is really simple. Just enter your information like your name, position for which you are writing cover letter, to whom you want to send this cover letter and company to which you are planning to apply using this cover letter. Hit generate cover letter button and let ai handle rest of things for you.")
    st.markdown("3. Can i download cover letter?")
    st.write("Yes, you can download unlimited cover letters in pdf format")
    
with st.form(key='my_form_to_submit'):    
    company_name = st.text_input("Company Name: ", "Hashtrust")
    role = st.text_input("What role are you applying for? ", "Python Developer")
    contact_person = st.text_input("Who are you emailing? ", "Technical Hiring Manager")
    your_name = st.text_input("What is your name? ", "Ronak Mundra")
    personal_exp = st.text_input("I have experience in...", "Bachelor's degree in computer science, computer engineering, or related field,1-2 years of experience as a Python developer,Knowledge of Python and related frameworks including Django and Flask. ")
    job_desc = st.text_input("I am excited about the job because...", "We are looking for an experienced Python developer to join our engineering team and help us create dynamic software applications for our clients. In this role, you will be responsible for writing and testing scalable code, developing back-end components, and integrating user-facing elements in collaboration with front-end developers. " )
    passion = st.text_input("I am passionate about...", "Ability to collaborate on projects and work independently when required.")
    job_specific = st.text_input("What do you like about this job? (Please keep this brief, one sentence only.) ")
    specific_fit = st.text_input("Why do you think your experience is a good fit for this role? (Please keep this brief, one sentence only.) ")
    submit_button = st.form_submit_button(label='Submit')
    
# prompt=("You are a Cover Letter Writter for a job seeker with ten year of experience in the industry.Write a cover letter in about 250 to 400 words to " + contact_person + " from " + your_name +" for a " + role + " job at " + company_name +"." + " I have experience in " +personal_exp + " I am excited about the job because " +job_desc + " I am passionate about "+ passion)
prompt = ("Write a cover letter to " + contact_person + " from " + your_name +" for a " + role + " job at " + company_name +"." + " I have experience in " +personal_exp + " I am excited about the job because " +job_desc + " I am passionate about "+ passion)
print(prompt)

if submit_button:
    response = ai.Completion.create(
        engine = 'text-davinci-002',
        prompt=prompt, 
        max_tokens=int(3000), 
        temperature=0.99,
        top_p=int(1), 
        n=1,
        frequency_penalty=0.3,
        presence_penalty=0.9 
    )


    text =response.choices[0].text.strip()
    print("Prompt:", prompt)
    print("Response:", text)

    st.subheader("Cover Letter Prompt")
    st.write(prompt)
    st.subheader("Auto-Generated Cover Letter")
    st.write(text)

    print("Other results:", response)
    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.success('Ai Cover letter is generated', icon="✅")


    with open('cover_letters.txt','w') as f:
        f.write(text)
        
    print("Other results:", response)
    
        
    from fpdf import FPDF

    def convert_file(file):
        pdf = FPDF()
        pdf.add_page()

        for text in file:
            if len(text) <= 20:
                pdf.set_font("Arial","",size=16) # For title text
                pdf.cell(w=200,h=10,txt=text,ln=1,align="L")
            else:
                pdf.set_font("Arial",size=15) # For paragraph text
                pdf.multi_cell(w=0,h=10,txt=text,align="L")
        pdf.output("Cover_letter.pdf")
        print("Successfully converted!")
    file = open("cover_letters.txt","r")

    convert_file(file)
    
    with open("Cover_letter.pdf","rb") as pdf_file:
        PDFbyte = pdf_file.read()
    
    st.download_button(label='Download Cover Letter', file_name=f'Cover_letter_{your_name}.pdf', data=PDFbyte,mime="application/octet-stream")
