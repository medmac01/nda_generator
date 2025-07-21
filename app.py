# app.py

import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from rules_engine import build_llm_prompt
from j2_engine import render_template
import datetime


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PoC NDA Generator",
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

if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

# A dedicated system prompt for the chat/modification phase.
CHAT_SYSTEM_PROMPT = """
You are a precise legal contract editor. Your task is to modify the provided Non-Disclosure Agreement (NDA) based *only* on the user's explicit request.

**Your Core Directives:**
1.  **Strict Adherence:** Only make the change requested by the user. Do not add, remove, or alter any other part of the contract.
2.  **Maintain Professional Tone:** Ensure the wording of your modifications is formal, professional, and consistent with the existing legal language of the document.
3.  **Output the Full Document:** After making the requested change, you MUST return the entire, complete, and updated text of the NDA. Do not provide summaries, explanations, or confirmation messages. Your output should be only the contract text itself.
4.  **No Commentary:** Do not include phrases like "Here is the updated version:", "I have made the requested change:", or any other conversational text. The output must be ready to be copied and pasted directly into a legal document.
5.  **If Unclear, Ask:** If the user's request is ambiguous, ask for clarification instead of guessing. For example: "Could you please specify which clause you are referring to for the 'indemnity' change?"

Your role is to act as a silent, precise editing tool. The user provides an instruction, you provide the fully updated document.
"""

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
    
def generate_or_modify_contract(prompt, is_modification=False):
    """
    Calls the Google Gemini API to generate or modify the contract text.
    Handles both initial generation and subsequent chat-based modifications.
    """
    try:
        generation_config = {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 8192,
        }
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite-preview-06-17",
            generation_config=generation_config,
            system_instruction=prompt if not is_modification else CHAT_SYSTEM_PROMPT
        )
        chat_session = model.start_chat(
            history=st.session_state.messages if is_modification else []
        )
        spinner_text = "Modifying the NDA..." if is_modification else "Drafting the NDA..."
        with st.spinner(spinner_text):
            content_to_send = prompt if is_modification else "Generate the initial contract based on the system instructions you have received."
            response = chat_session.send_message(content_to_send)
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

with st.expander("Step 1: Generate the Initial Draft", expanded=not st.session_state.nda_text):
    st.header("Contract Details")
    col1, spacer, col2 = st.columns([1, 0.1, 1])

    with col1:
            st.header("First Party")
        
            first_party = st.text_input("First Party", "OCP")
            first_party_address = st.text_input(
                "First Party Address",
                "Rue Al Abtal, Hay Erraha 20200, Casablanca Morocco"
            )
            first_party_incorporation_state = st.text_input(
                "First Party Incorporation State",
                "Casablanca, Morocco"
            )
            first_party_representative = st.text_input(
                "First Party Representative",
                "Mr. Last First"
            )
            first_party_registration_number = st.text_input(
                "First Party Registration Number",
                "40327"
            )
            first_party_role = st.selectbox(
                "First Party Role",
                ("Receiving Party", "Disclosing Party", "Both (Bilateral)")
            )

    with col2:
            st.header("Second Party")
        
            second_party = st.text_input("Second Party", "UM6P Foundry")
            second_party_address = st.text_input(
                "Second Party Address",
                "Lot 660, Hay Moulay Rachid Ben Guerir, 43150, Morocco"
            )
            second_party_incorporation_state = st.text_input(
                "Second Party Incorporation State",
                "Ben Guerir, Morocco"
            )
            second_party_representative = st.text_input(
                "Second Party Representative",
                "Mr. Last First"
            )
            second_party_registration_number = st.text_input(
                "Second Party Registration Number",
                "1037"
            )

            default_second_party_role = ""
            if first_party_role == "Disclosing Party":
                default_second_party_role = "Receiving Party"
            elif first_party_role == "Receiving Party":
                default_second_party_role = "Disclosing Party"
            elif first_party_role == "Both (Bilateral)":
                default_second_party_role = "Both (Bilateral)"
            second_party_role = st.text_input(
                "Second Party Role",
                value=default_second_party_role,
                disabled=True
            )
        
    st.markdown("----------")
    purpose_type = st.selectbox(
                "Purpose of Disclosure Type",
                ("Education", "Business", "Research", "Other")
            )        
    default_purpose = ""
    if purpose_type == "Research":
        default_purpose = "The contemplated cooperation between the Parties relating to the impact of AI on the future of work"
    elif purpose_type == "Education":
        default_purpose = "The contemplated cooperation between the Parties relating to the creation of a joint Master on Data Science"
    elif purpose_type == "Business":
        default_purpose = "The contemplated merger between the Parties"          
    purpose = st.text_area(
                "Purpose of Disclosure",
                value=default_purpose,           
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
                value=st.session_state.get("effective_date", datetime.date.today()),
                help="The date when the NDA becomes effective. Defaults to today."
            )
            
    litigation = st.selectbox(
                "Dispute Resolution",
                ("Arbitration under ICC Rules, seat in Paris", "Arbitration under LCIA Rules, seat in London")
            )
            
    submitted = st.button("Draft NDA", type="primary", use_container_width=True)


    if submitted:
        user_inputs = {
            "first_party": first_party,
            "first_party_address": first_party_address,
            "first_party_incorporation_state": first_party_incorporation_state,
            "first_party_representative": first_party_representative,
            "first_party_registration_number": first_party_registration_number,
            "first_party_role": first_party_role,

            "second_party": second_party,
            "second_party_address": second_party_address,
            "second_party_incorporation_state": second_party_incorporation_state,
            "second_party_representative": second_party_representative,
            "second_party_registration_number": second_party_registration_number,
            "second_party_role": second_party_role,

            "purpose_type": purpose_type,
            "purpose": purpose,
            "applicable_law": applicable_law,
            "language": language,
            "duration": duration,
            "date": date.strftime("%Y-%m-%d"),
            "litigation": litigation,
            "nature_of_obligations": "Unilateral" if first_party_role != "Both (Bilateral)" else "Bilateral"
        }

        st.session_state.first_party = first_party
        st.session_state.second_party = second_party
        st.session_state.effective_date = date.strftime("%Y-%m-%d")
        
        # Build the prompt (No changes needed in rules_engine.py)
        # st.session_state.prompt = build_llm_prompt(user_inputs)
        
        # Generate the contract using the new Gemini function
        # generated_text = generate_contract_from_prompt(st.session_state.prompt)
        generated_text = render_template(user_inputs)
        if generated_text:
            st.session_state.nda_text = generated_text

        # Clear previous chat history and set the initial contract as the first "model" message
        st.session_state.messages = [
            {"role": "user", "parts": ["Please generate the initial NDA."]},
            {"role": "model", "parts": [generated_text]}
        ]
        st.rerun() # Rerun to update the UI immediately

# --- Document Display and Chat Section ---
# if st.session_state.nda_text:
#     st.markdown("---")
#     st.header("Step 2: Review and Modify the Document")
    
#     # Display the current version of the NDA
#     st.text_area("Current NDA Draft", st.session_state.nda_text, height=400, key="nda_display")
#     st.download_button(
#         label="📥 Download as Word Document",
#         data=create_docx(st.session_state.nda_text),
#         file_name=f"NDA_{first_party}_{second_party}.docx",
#         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )

#     st.markdown("---")
#     st.subheader("💬 Chat to Modify")

#     ### NEW ###
#     # Display chat history
#     for message in st.session_state.messages:
#         # We only want to show the user's explicit requests in the chat log
#         if message["role"] == "user" and message["parts"] != ["Please generate the initial NDA."]:
#             with st.chat_message("user"):
#                 st.markdown(message["parts"][0])
    
#     # Chat input for user
#     if user_prompt := st.chat_input("How would you like to modify the contract?"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "parts": [user_prompt]})
        
#         # Display the user's message immediately
#         with st.chat_message("user"):
#             st.markdown(user_prompt)

#         # Generate the modified contract
#         modified_text = generate_or_modify_contract(user_prompt, is_modification=True)
        
#         if modified_text:
#             # Update the main NDA text in session state
#             st.session_state.nda_text = modified_text
#             # Add the model's new version to the history
#             st.session_state.messages.append({"role": "model", "parts": [modified_text]})
#             # Rerun the script to update the text area and chat display
#             st.rerun()
# # st.markdown("----------")
# # st.header("Generated Document")
    
# # if st.session_state.nda_text:
# #     st.markdown(st.session_state.nda_text)

# #     col1, spacer, col2 = st.columns([0.9, 0.01, 0.09]) 
# #     with col1:
# #         feedback = st.text_input(
# #             "Enter your message:",
# #             placeholder="Type something here...",
# #             label_visibility="collapsed" 
# #         )

# #     with col2:
# #         chat_button = st.button("Send ✉️")

# #     if chat_button:
# #         if feedback:
# #             st.success(f"Message sent: '{feedback}'")
# #         else:
# #             st.warning("Please enter a message before sending!")

#     # Create docx in memory for download
#     docx_bytes = create_docx(st.session_state.nda_text)
        
#     st.download_button(
#         label="📥 Download as Word Document",
#         data=docx_bytes,
#         file_name=f"NDA_{first_party.replace(' ', '')}_{second_party.replace(' ', '')}.docx",
#         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#         use_container_width=True
#     )
        
#         # Expander to see the prompt that was used
#     with st.expander("Show the AI Prompt"):
#         st.code(st.session_state.prompt, language='markdown')

st.markdown("---")
st.header("Step 2: Review and Modify the Draft")

# Display the conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # The contract text is displayed as a markdown block inside the chat message
        st.markdown(message["parts"][0])

# Chat input for user
if user_prompt := st.chat_input("How would you like to modify the contract? (e.g., 'Change duration to 5 years')"):
    # Append the user's request to the history
    st.session_state.messages.append({"role": "user", "parts": [user_prompt]})
    
    # Generate the modified contract
    # We pass the user's prompt to the function, but the real context is the history
    modified_text = generate_or_modify_contract(user_prompt, is_modification=True)
    
    if modified_text:
        # Update the main NDA text in session state
        st.session_state.nda_text = modified_text
        # Add the model's new version (the full contract) to the history
        st.session_state.messages.append({"role": "model", "parts": [modified_text]})
        # Rerun the script to display the new messages
        st.rerun()

# Place the download button in a consistent location
if st.session_state.nda_text:
    st.download_button(
        label="📥 Download Current Version as Word Document",
        data=create_docx(st.session_state.nda_text),
        file_name=f"NDA_{st.session_state.first_party}_{st.session_state.second_party}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Fill out the form on the left and click 'Draft NDA' to generate the document.")