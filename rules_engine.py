# rules_engine.py

# Translated rules from "3.1 Instructions specific to NDAs"
NDA_DRAFTING_RULES = {
    "Preamble and Parties": {
        "description": "The introductory section identifying the parties and effective date.",
        "instructions": "Draft a standard preamble for a Non-Disclosure Agreement between [Party 1 Name], [Party 1 Type and Address], and [Party 2 Name], [Party 2 Type and Address]. The effective date should be [Effective Date]. Clearly identify which party is the Disclosing Party and which is the Receiving Party based on the user's role selection. If it's a bilateral agreement, state that both parties will act as Disclosing and Receiving Parties."
    },
    "Purpose": {
        "description": "The 'Whereas' or 'Background' clause.",
        "instructions": "Draft a 'Purpose' clause explaining why the confidential information is being shared. Use the following user-provided purpose: '[Purpose]'."
    },
    "Representatives": {
        "description": "Definition of who can receive the information.",
        "receiving": [
            "Define 'Representatives' narrowly. Limit the scope strictly to what is needed for the Purpose.",
            "The Receiving Party's liability for misuse by Representatives should be limited to its employees and directors only. (Mandatory)"
        ],
        "disclosing": [
            "Define 'Representatives' broadly to include employees, directors, officers, affiliates, and advisors (like banks, accountants).",
            "The Receiving Party must be held legally responsible for any breach by any of its Representatives. This must be an explicit clause. (Mandatory)"
        ],
        "mutual": "Draft a fair and balanced definition of 'Representatives', typically including employees, directors, and professional advisors (legal, financial) on a need-to-know basis. Both Parties shall be responsible for breaches by their respective Representatives."
    },
    "Confidential Information": {
        "description": "The core definition of what is considered confidential.",
        "receiving": [
            "Define 'Confidential Information' narrowly by listing the specific types of information to be shared. (Mandatory)",
            "Include a clause requiring information to be explicitly marked 'Confidential' to be protected (Optional, but preferred for Recipient).",
            "Minimum acceptable exclusions are: (a) already public, (b) received from a third party without breach, (c) already in recipient's possession, (d) independently developed. (Mandatory)"
        ],
        "disclosing": [
            "Define 'Confidential Information' as broadly as possible, covering all forms of information (written, oral, electronic). (Mandatory)",
            "Ensure oral disclosures are included and must be summarized in writing within a short period (e.g., 15 days) to be protected.",
            "Refuse any extended or non-standard exclusions. Stick to the basic public domain/prior knowledge exceptions. (Mandatory)"
        ],
        "mutual": "Draft a broad but fair definition of 'Confidential Information', including oral disclosures. Use standard exclusions that are acceptable to both sides."
    },
    "Use of Information": {
        "description": "Restrictions on how the information can be used.",
        "receiving": [
            "Limit the use of Confidential Information strictly to the defined 'Purpose'.",
            "Do not add extra obligations beyond a reasonable standard of care (i.e., the same care used for its own confidential information)."
        ],
        "disclosing": [
            "Limit the use of Confidential Information strictly to the defined 'Purpose' and prohibit any other use. (Mandatory)",
            "Add obligations prohibiting reverse engineering, decompiling, or unauthorized copying. (Mandatory)",
            "Require that disclosure is limited to Representatives on a strict 'need-to-know' basis."
        ],
        "mutual": "Draft a standard 'Permitted Use' clause limiting use to the Purpose. Include a standard of care commitment for both parties."
    },
    "Duration": {
        "description": "The term of the agreement and the survival of confidentiality obligations.",
        "receiving": [
            "The agreement duration should be as short as possible, preferably 6 months to 2 years.",
            "Refuse any duration longer than 2 years. (Mandatory)",
            "The confidentiality obligation itself should survive for a fixed, reasonable period after the agreement terminates (e.g., 2-3 years)."
        ],
        "disclosing": [
            "The agreement duration should be longer, preferably > 3 years. (Mandatory)",
            "The confidentiality obligation should survive for as long as possible, ideally indefinitely for trade secrets, or for a long fixed period (e.g., 5-10 years) for other information."
        ],
        "mutual": "Propose a reasonable agreement duration (e.g., 2-3 years) and a confidentiality survival period of 3-5 years post-termination."
    },
    "Return/Destruction of Information": {
        "description": "Obligations at the end of the agreement.",
        "receiving": [
            "Agree to return or destroy information, but ensure the clause allows for retention of copies in automated backup systems and for legal/compliance purposes.",
            "The obligation should be 'upon written request' from the Disclosing Party."
        ],
        "disclosing": [
            "Mandate that the Receiving Party must, upon request, promptly return or destroy all Confidential Information.",
            "Require the Receiving Party to provide a written certificate confirming destruction, signed by an officer. (Mandatory)"
        ],
        "mutual": "Draft a standard return/destroy clause, including an option for certification and acknowledging standard archival/backup exceptions."
    },
    "Remedies for Breach": {
        "description": "What happens if the agreement is breached.",
        "receiving": [
            "Limit remedies to actual, proven monetary damages.",
            "Reject any clauses for indemnification or payment of the other party's legal fees. (Mandatory)",
            "Reject any mention of punitive damages. (Mandatory)"
        ],
        "disclosing": [
            "State that monetary damages are inadequate and that the Disclosing Party is entitled to seek injunctive relief (a court order to stop the breach) without posting a bond. (Mandatory)",
            "Include a clause for indemnification for any losses suffered due to a breach.",
            "Request reimbursement of legal fees if the Disclosing Party prevails in litigation."
        ],
        "mutual": "Acknowledge that injunctive relief may be appropriate. Omit clauses on indemnification and legal fees, leaving it to the governing law."
    },
    "Governing Law and Jurisdiction": {
        "description": "The legal framework for the contract.",
        "instructions": "The governing law shall be [Applicable Law]. Any disputes shall be resolved through [Litigation]."
    },
    "Responsibility": {
        "description": "Who is responsible for breaches by Representatives.",
        "receiving": [
            "Each Party hereto is fully liable for damages to the other Party for any harm or damage caused to the other Party or that Party’s customers or business partners due to violation of the terms of this Agreement, including for any harm or damage caused by the breaching Party’s Representatives.",
        ],
        "disclosing": [
            "Each Party hereto is fully liable for damages to the other Party for any harm or damage caused to the other Party or that Party’s customers or business partners due to violation of the terms of this Agreement, including for any harm or damage caused by the breaching Party’s Representatives.",
        ],
        "mutual": "Each Party hereto is fully liable for damages to the other Party for any harm or damage caused to the other Party or that Party’s customers or business partners due to violation of the terms of this Agreement, including for any harm or damage caused by the breaching Party’s Representatives."
    },
    "General Provisions": {
        "description": "Boilerplate clauses like 'Modification', 'Entire Agreement', 'Notices'.",
        "instructions": "Include standard boilerplate clauses for 'Entire Agreement', 'Modification', 'Applicable Law', and 'Notices'. Ensure the notice addresses are those of the parties mentioned in the preamble."
    },
}

GENERAL_DRAFTING_INSTRUCTIONS = """
- Use capital letters and bold text for Defined Terms (e.g., **"Confidential Information"**).
- Use capital letters every time a defined term is used subsequently.
- Check all cross-references to ensure they are logical (the LLM should handle this implicitly).
- Ensure professional, clear, and unambiguous legal language throughout.
- The final output should be a single, complete document, ready for signature. Do not include any of these instructions or any commentary in the final text.
"""

def get_role_key(party_role):
    """Translates user-friendly role to a dictionary key."""
    if party_role == "Receiving Party":
        return "receiving"
    elif party_role == "Disclosing Party":
        return "disclosing"
    else: # "Both"
        return "mutual"

def build_llm_prompt(user_inputs):
    """Builds a structured prompt for the LLM based on user inputs and rules."""
    
    role_key = get_role_key(user_inputs["party_role"])

    prompt = f"""
You are an expert legal AI assistant. Your task is to draft a complete Non-Disclosure Agreement based on the following context and specific clause-by-clause instructions.

**OVERALL CONTEXT:**
- This is a {user_inputs['nature_of_obligations']} Non-Disclosure Agreement.
- Our Client's Role: {user_inputs['party_role']}.
- Party 1 (Our Client): {user_inputs['client_name']}
- Party 1 Type and Address: {user_inputs['client_type_and_address']}
- Party 2 (Counterparty): {user_inputs['counterparty_name']}
- Party 2 Type and Address: {user_inputs['counterparty_type_and_address']}
- Purpose of Disclosure: {user_inputs['purpose']}
- Applicable Law: {user_inputs['applicable_law']}
- Dispute Resolution (Litigation): {user_inputs['litigation']}
- Duration of Confidentiality: {user_inputs['duration']} months
- Language of the Contract: {user_inputs['language']}
- Effective Date: {user_inputs.get('effective_date', 'Today')}
**DRAFTING INSTRUCTIONS - CLAUSE BY CLAUSE:**

"""
    # Iterate through the rules and build the prompt chunk by chunk
    for topic, rules in NDA_DRAFTING_RULES.items():
        prompt += f"--- \n"
        prompt += f"**Clause Topic: {topic}**\n"
        
        # Get the specific instructions based on the role
        if "instructions" in rules:
            # For clauses with single instruction set (Preamble, Purpose, etc.)
            instruction_text = rules["instructions"]
        else:
            # For clauses with role-based instructions
            instruction_text = rules[role_key]

        # Format instructions nicely
        if isinstance(instruction_text, list):
            for item in instruction_text:
                prompt += f"- {item}\n"
        else:
            prompt += f"- {instruction_text}\n"

    # Add general formatting instructions at the end
    prompt += "\n--- \n"
    prompt += "**FINAL FORMATTING INSTRUCTIONS:**\n"
    prompt += GENERAL_DRAFTING_INSTRUCTIONS

    # Replace placeholders in the prompt itself
    prompt = prompt.replace("[Party 1 Name]", user_inputs['client_name'])
    prompt = prompt.replace("[Party 2 Name]", user_inputs['counterparty_name'])
    prompt = prompt.replace("[Party 1 Type and Address]", user_inputs['client_type_and_address'])
    prompt = prompt.replace("[Party 2 Type and Address]", user_inputs['counterparty_type_and_address'])
    prompt = prompt.replace("[Effective Date]", str(user_inputs.get('effective_date', 'Today')))
    prompt = prompt.replace("[Party 1 Role]", user_inputs['party_role'])
    prompt = prompt.replace("[Nature of Obligations]", user_inputs['nature_of_obligations'])
    prompt = prompt.replace("[Language]", user_inputs['language'])
    prompt = prompt.replace("[Duration]", str(user_inputs['duration']))
    prompt = prompt.replace("[Purpose]", user_inputs['purpose'])
    prompt = prompt.replace("[Applicable Law]", user_inputs['applicable_law'])
    prompt = prompt.replace("[Litigation]", user_inputs['litigation'])

    return prompt