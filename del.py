import streamlit as st

st.success("Ravi: Hello Chandu")
st.success("Chandu: Hi Ravi")

HALLUCINATION_SYSTEM_PROMPT = """
Evaluate the following SUB-CONTEXT for faithful to the CONTEXT. 
Assume SUB-CONTEXT is generated from the CONTEXT.
Assume SUB-CONTEXT is a part of the CONTEXT and it should be faithful to the CONTEXT.
Assume SUB-CONTEXT must not-contradict the CONTEXT information.
A faithful SUB-CONTEXT should only include information strictly present in the given CONTEXT (Even wording is difference, but semantically same). 
Also factual SUB-CONTEXT should be part of the CONTEXT information ONLY. 


SUB-CONTEXT: {generated_text}
CONTEXT: {context}

Return the answer as a single string label. For example, answer is 'factual' if the SUB-CONTEXT is factual to the CONTEXT,
otherwise answer is 'non-factual'.
Do not include any additional text or explanations in the response.
"""
