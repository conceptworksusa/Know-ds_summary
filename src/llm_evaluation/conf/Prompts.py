# Define the default prompt for the Llama model
prompt1 = """Classify the user's intent into one of the following categories and output only the intent name as a single word — no explanations, no labels:

1. Greet - For greetings like "hi", "hello", "how are you" etc.  
2. Claims - For questions about the current claim or questions related to claims.  
3. UnKnown - For anything else that does not fall under the above categories.

User Query: {query}

Only respond with one of: Greet, Status, UnKnown"""



prompt2 = """
if the user query has multiple questions, split the input query into multiple questions.

Understand the gist of the each input question and classify the user's intent into one of the following categories:

Classify the user's intent into one of the following categories and output one intent only as a single word like 'unknown' or 'greet' or 'status':

1. Greet - if user intent is to say like "hi", "hello", "how are you" etc.  
2. Status - if user intent is about knowing the status of a ticket or case number etc.  
3. UnKnown - if you are not sure or uncertain about the intent or mixed intents.

User Query: {query}

Intent:"""


RAG_PROMPT1 = """
Label above rephrased question from a conversation with an intent. Reply ONLY with the name of the intent.

The intent should be one of the following:
- greet
- status
- unknown

Message: {query1}    # Got from vector database
Intent:  {intent1}   # Got from vector database
Message: {query2}    # Got from vector database
Intent:  {intent2}   # Got from vector database

query: {query}    # Got from user input
Intent:

"""

RAG_PROMPT2 = """
step1:
Rephrase the question: include only the core ask and output the ask in a clear and appropriate 'how to' or 'what is' or 'why is' question. ONLY output the rephrased question.
Question: {query}

step2:
Label above rephrased question from a conversation with an intent. Reply ONLY with the name of the intent.

The intent should be one of the following:
- greet
- status
- unknown

Message: {query1}    # Got from vector database
Intent:  {intent1}   # Got from vector database
Message: {query2}    # Got from vector database
Intent:  {intent2}   # Got from vector database

query: {query}    # Got from user input
Intent:

"""

HALLUCINATION_SYSTEM_PROMPT = """
Evaluate the following RESPONSE for faithfulness to the CONTEXT. 
A faithful response should only include information present in the context, avoid inventing new details, 
and not contradict the context. Return one of the following labels: 'Faithful' or 'Hallucinated’.

RESPONSE: {generated_text}
CONTEXT: {context}

Return the answer as a single string label. For example, answer is 'Faithful' if the response is faithful to the context,
otherwise answer is 'Hallucinated'.
Do not include any additional text or explanations in the response.
"""

# Prompt to evaluate the relevance of context to a question
CONTEXT_RELEVANCE_PROMPT = """
Evaluate the relevance of the text in answering the  QUESTION.
A relevant text contains information that helps answer the question, even if partially.
Return one of the following labels: 'Relevant', or 'Irrelevant.

QUESTION: {question}
TEXT: {context}

Return the answer as a single string label. For example, answer is 'Relevant' if the text is relevant to the question,
otherwise answer is 'Irrelevant'.
Do not include any additional text or explanations in the response.
"""

BATCH_CONTEXT_RELEVANCE_PROMPT = """
You are given a list of QUESTIONS and a corresponding list of TEXTS.
Each QUESTION corresponds the TEXT at the same index ( i.e. QUESTION[0] corresponds to TEXT[0] , QUESTION[1] corresponds to TEXT[1] and so on).

Evaluate the relevance of the TEXT in answering the QUESTION.
A relevant text contains information that helps answer the question, even if partially.
Mark each pair as either 'Relevant' or 'Irrelevant'.

Example format:
QUESTIONS: ['What is the capital of France?', 'How many continents are there?']
TEXTS: ['Paris is the capital of France.', 'America is a richer country.']
Response: ['Relevant', 'Irrelevant']

QUESTIONS: {questions}
TEXTS: {contexts}
Response: ?

Return a list of labels, each label must be either 'Relevant' or 'Irrelevant'.
The Response must be list of strings like ["Relevant", "Irrelevant", ...] with one label per each QUESTION-TEXT pair.

Do not include any additional text or explanations in the response.
"""


# Prompt for Evaluating correctness based on reference answer.
CORRECTNESS_PROMPT = """
Compare the generated RESPONSE to the REFERENCE answer.
Evaluate if the generated response correctly conveys the same meaning, even if the wording is different.
Return one of these labels: 'Correct’ or 'Incorrect.'
  
RESPONSE: {generated_text}
REFERENCE: {reference_answer}

Return the answer as a single string label. For example, answer is 'Correct' if the response is correct,
otherwise answer is 'Incorrect'.

Do not include any additional text or explanations in the response.
  """
