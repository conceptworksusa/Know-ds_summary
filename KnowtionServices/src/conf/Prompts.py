# Define the default prompt for the Llama2 model
default_prompt = "Use the following pieces of information to answer the user's queries. If you don't know the answer, just say that you don't know, don't try to make up an answer."

default_prompt0 = "Use the following pieces of information to answer the user's queries. If you don't know the answer, just say that you don't know, don't try to make up an answer.Only return the helpful answers below and nothing else.Helpful answer:"

default_prompt1 = """As an AI assistant. Please provide simple and precise answer, you will answer question based strictly on the given information. If the answer cannot be found in the given information, respond with "Answer not found in context"."""

default_prompt11 = """As an AI assistant. Please provide simple and precise answers, you will answer questions based strictly on the given context. If the answer cannot be found in the context, respond with "Answer not found in context"."""



default_prompt2 = """As an AI assistant, please provide simple, accurate and precise answers. You will answer questions based strictly on the given context. If the answer cannot be found in the context, respond with "I don't know". Don't try to make up an answer"""

default_prompt3 =  """Use the following pieces of information to answer the user's queries.
If you don't know the answer, just say that you don't know, don't try to make up an answer"""

default_prompt4 = """Use the given context to answer the question. If you don't find the answer in given context, just say you "I don't know". Keep the answer concise and accurate."""

# Define system prompt for question answering task for the Llama3 model
system_prompt_for_qa = """As an AI assistant. Please provide simple and precise answer, you will answer question based strictly on the given information.
                   If the answer cannot be found in the given information, respond with "Answer not found in context"
        
                    Example format:
                    Q: What is the title of the document?
                    A: Sample Document Title
            
                    Q: Who is the authorizing agent of the document?
                    A: Dr. John Doe.
                    
                    Please respond in a similar format.
                    """

# Define user prompt for question answering task for the Llama3 model
user_prompt_for_qa = "The question is: {questions} \n\n The information provided is: {context}"

# Define prompt structure for the Llama3 model for question answering task
llama3_prompt_for_qa = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

    {system_prompt_for_qa}<|eot_id|><|start_header_id|>user<|end_header_id|>

    {user_prompt_for_qa}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


# Define system prompt for summarization task for the Llama3 model
# system_prompt_for_summarize = "Write a concise summary of the following context use paragraph format. Use bulleted point where necessary."
system_prompt_for_summarize = "Write a concise summary of the following context and consider all individual persons if there exist more than one. Use paragraph format. Use bulleted point where necessary."
# Define user prompt for summarization task for the Llama3 model
user_prompt_for_summarize = "Context: {context}"

# Define prompt structure for the Llama3 model for summarization task
llama3_prompt_for_summarize = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
    f"{system_prompt_for_summarize}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
    f"{user_prompt_for_summarize}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
)

# Define the chunks prompt for the Llama3 model
chunks_prompt = """
                Please summarize the below document:
                document:`{text}'
                Summary:
                """
# Define the final combine prompt for the Llama3 model
final_combine_prompt = """
                Write a complete summary for the following intermediate summaries
                and combine them into a final, consolidated summary. 
                Do not lose any intermediate summary information. 
                Use paragraph and bulleted point format where necessary.
                Below are the intermediate summaries: \n {text} \n """

# Define the prompt for the Llama3 model for summarization task using stuff chain
system_prompt = "Write a concise summary of the following document. Use paragraph format and bulleted point where necessary."

# Define the additional prompt for the Llama3 model for summarization task
additional_prompt = "Start with answer , do not start like, here is the summery. \n\n document:`{text}'"

# system_prompt_for_json = """
#     Convert the following JSON object into clear, human-understandable language.
#     Instructions:
#     - Do not skip any field unless its value is null.
#     - Format date values into a human-readable format (e.g., "2000-07-09T00:00:00" → "July 9, 2000").
#     - Use complete data and preserve every piece of data.
#     - Give the output in a single paragraph.
#     - Strictly follow the format of the output.
#     - If there are any nested information must consider all information , do not skip any information
#
#     Input JSON:
#     {
#       "DemographicsInfo": {
#         "PatientDateOfBirth": "2000-07-09T00:00:00",
#         "PatientGender": "M",
#         "PatientAddress": "25096 150TH ST",
#         "PatientCity": "DIKE",
#         "PatientState": "IA",
#         "PatientZip": "50624"
#         "ServiceDateFrom": "2023-07-05T00:00:00",
#         "ServiceDateThrough": "2023-07-10T00:00:00",
#         "SubscriberFirstName": "MATTHEW",
#         "SubscriberLastName": "WAGNER",
#         "RemitClaimLineDetails": [
#             {
#             "Id": 2038905,
#             "RemitClaimLineItemGuid": "0c89717d-c953-47ff-9259-47df0dcabda4",
#             "RemitClaimGuid": "5e859b16-8b92-4a57-a069-9f6cc4c3510c",
#             }]
#       }
#     }
#
#     Output format:
#     Demographics Info : The patient's date of birth is July 9, 2000. The gender is male. The permanent address is 25096 150TH Street, located in the city of Dike, in the state of Iowa, with the ZIP code 50624. The service began on July 5, 2023 and ended on July 10, 2023. The subscriber's first name is Matthew and last name is Wagner. Remit Claim details The remit claim line item ID is 2038905. The remit claim line item GUID is 0c89717d-c953-47ff-9259-47df0dcabda4. The remit claim GUID is 5e859b16-8b92-4a57-a069-9f6cc4c3510c.
#     """

# system_prompt_for_json = """
#     Convert the following JSON object into clear, human-understandable language in single paragraph.
#
#     Instructions:
#     - Do not skip any field unless its value is null.
#     - Format date values into a human-readable format (e.g., "2000-07-09T00:00:00" → "July 9, 2000").
#     - Do not summarize. Use complete sentences and preserve every piece of information.
#     """
#
system_prompt_for_json = """

    Convert the following JSON object into clear, human-understandable language in single paragraph which an appeals nurse
    could use to assist them with drafting an appeal letter. Make sure to only include  relevant information and details.

    Instructions:
    - Do not skip any field unless its value is null.
    - Start with the content only and do not start like, here is the JSON object converted into blah blah.
    - Format date values into a human-readable format (e.g., "2000-07-09T00:00:00" → "July 9, 2000").
    - Do not summarize. Use complete sentences and preserve every piece of information.
    """

# system_prompt_for_json = """
#
#     Convert the following JSON object into clear, human-understandable language in single paragraph which an appeals nurse
#     could use to assist them with drafting an appeal letter. Make sure to only include  relevant information and details.
#     Strictly follow the given instructions.
#
#     Instructions:
#     - Act as an appeals nurse and convert the JSON object into a clear, human-understandable language.
#     - Start with the content(response) only and do not start like, here is the JSON object converted into blah blah.
#     - Do not skip any field unless its value is null.
#     - Format date values into a human-readable format (e.g., "2000-07-09T00:00:00" → "July 9, 2000").
#     - Do not summarize. Use complete sentences and preserve every piece of information.
#     """
