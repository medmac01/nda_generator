# app.py

import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from rules_engine import build_llm_prompt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PoC NDA Generator (Gemini)",
    page_icon="✍️",
    layout="wide"
)

# --- API KEY & SESSION STATE ---
try:
    # Configure the Gemini client with the API key from secrets
    api_key=st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("Secrets file not found or GEMINI_API_KEY is missing. Please create .streamlit/secrets.toml with your key.")
    st.stop()

if "nda_text" not in st.session_state:
    st.session_state.nda_text = ""
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

# --- FUNCTIONS ---
def generate_contract_from_prompt(prompt):
    """Calls the Google Gemini API to generate the contract text."""
    
    try:
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Set up the model generation configuration
        generation_config = {
            "temperature": 0.3,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 8192,
        }

        # Initialize the Generative Model
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite-preview-06-17",
            generation_config=generation_config
        )

        with st.spinner("Drafting the NDA..."):
            response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return None

def create_docx(text):
    """Creates a Word document in memory from the given text."""
    doc = Document()
    doc.add_heading('Non-Disclosure Agreement', 0)
    # Simple parsing: add paragraphs based on newlines
    for para in text.split('\n'):
        # Check if the line is likely a heading (e.g., "Article 1. Definitions")
        if para.strip().lower().startswith(("article", "section")) or para.strip().endswith(":"):
            doc.add_heading(para.strip(), level=2)
        elif para.strip(): # Avoid adding empty paragraphs
            doc.add_paragraph(para)
    
    # Save the document to a byte stream
    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()

# --- UI LAYOUT ---
st.title("📄 Proof-of-Concept NDA Generator")
st.markdown("This tool generates a first draft of a Non-Disclosure Agreement based on your selections. **All generated content must be reviewed by qualified legal counsel.**")

# Use two columns for a cleaner layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Contract Details")
    
    with st.form("nda_form"):
        client_name = st.text_input("Client Company Name (Party 1)", "OCP")
        client_type_and_address = st.text_input(
            "Client Type and Address",
            "Public Company, Casablanca, Morocco"
        )

        counterparty_name = st.text_input("Counterparty Name (Party 2)", "Tech Solutions Inc.")
        counterparty_type_and_address = st.text_input(
            "Counterparty Type and Address",
            "Private Company, Paris, France"
        )
        
        party_role = st.selectbox(
            "Which Party is our Client?",
            ("Receiving Party", "Disclosing Party", "Both (Bilateral)")
        )
        
        purpose = st.text_area(
            "Purpose of Disclosure",
            "For the purpose of the contemplated business relationship, will share confidential information.",
            # "To evaluate a potential business partnership and technology integration.",
            height=100
        )
        
        applicable_law = st.selectbox(
            "Applicable Law",
            ("English Law", "French Law", "Moroccan Law")
        )

        language = st.selectbox(
            "Language of the Contract",
            ("English", "French")
        )

        duration = st.number_input(
            "Duration of Confidentiality (months)",
            min_value=1,
            max_value=60,
            value=36,
            help="Duration for which the confidentiality obligations will apply."
        )

        date = st.date_input(
            "Effective Date",
            value=st.session_state.get("effective_date", None),
            help="The date when the NDA becomes effective. Defaults to today."
        )
        
        litigation = st.selectbox(
            "Dispute Resolution",
            ("Arbitration under ICC Rules, seat in Paris", "Arbitration under LCIA Rules, seat in London")
        )
        
        submitted = st.form_submit_button("Draft NDA", type="primary", use_container_width=True)

if submitted:
    user_inputs = {
        "client_name": client_name,
        "client_type_and_address": client_type_and_address,
        "counterparty_name": counterparty_name,
        "counterparty_type_and_address": counterparty_type_and_address,
        "language": language,
        "duration": duration,
        "party_role": party_role,
        "effective_date": date,
        "nature_of_obligations": "Unilateral" if party_role != "Both (Bilateral)" else "Bilateral",
        "purpose": purpose,
        "applicable_law": applicable_law,
        "litigation": litigation,
    }
    
    # Build the prompt (No changes needed in rules_engine.py)
    st.session_state.prompt = build_llm_prompt(user_inputs)
    
    # Generate the contract using the new Gemini function
    generated_text = generate_contract_from_prompt(st.session_state.prompt)
    if generated_text:
        st.session_state.nda_text = generated_text

with col2:
    st.header("Generated Document")
    
    if st.session_state.nda_text:
        st.markdown(st.session_state.nda_text)
        
        # Create docx in memory for download
        docx_bytes = create_docx(st.session_state.nda_text)
        
        st.download_button(
            label="📥 Download as Word Document",
            data=docx_bytes,
            file_name=f"NDA_{client_name.replace(' ', '')}_{counterparty_name.replace(' ', '')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        # Expander to see the prompt that was used
        with st.expander("Show the AI Prompt sent to Gemini"):
            st.code(st.session_state.prompt, language='markdown')
    else:
        st.info("Fill out the form on the left and click 'Draft NDA' to generate the document.")