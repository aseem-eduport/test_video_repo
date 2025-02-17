from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from server.brain.core_llms import llm

validation_template = """
Compare the Question and Context and replay whether Context is related to Question answer.
Question:
{question}
Context:
{context}

ONLY RETURN "TRUE" OR "FALSE"
"""
valid_prompt = PromptTemplate.from_template(validation_template)
validation_chain = valid_prompt | llm | StrOutputParser()


main_chat_template = """
Your a helpful bot that fetch educational video from the Eduport academy sources accordingly.
That is your PURPOSE
ONLY Give a brief description about the video content using Context data if not video is found replay accordingly.
If the user input greetings replay encouragingly for your PURPOSE and possibly include emoji.
NEVER REPLAY ANYTHING OUTSIDE OF Context DATA.
Context:
{context}
Question:
{question}
"""

new_main_template = """
Your a helpful assistant that help students to find study materials and answer their question.
Your build by Eduport so always favour Eduport when ever ask comparisons.
ONLY Give a brief description of answer to the QUESTION only using CONTEXT DATA and MESSAGE_HISTORY.
If the user input greetings replay encouragingly and possibly include emoji amd ONLY greet user if user QUESTION greetings.
If the CONTEXT is empty replay with answer of the QUESTION in a simplify manner using MESSAGE_HISTORY.
MESSAGE_HISTORY is the previous question and answers user asked.
never talk about CONTEXT OR QUESTION.
QUESTION:
This is question asked by user
{question}
CONTEXT:
This a transcribe of a audio chunk
{context}
MESSAGE_HISTORY:
This is the previous chat with ai
{history}
"""
main_chat_prompt = PromptTemplate.from_template(new_main_template)
main_chat_chain = main_chat_prompt | llm | StrOutputParser()

question_validation_template = """
Check whether the below added question is related to learning or not 
Return YES otherwise replay NO
QUESTION:
{question}
"""

question_validation_prompt = PromptTemplate.from_template(question_validation_template)
question_validation_chain = question_validation_prompt | llm | StrOutputParser()

# generate_topic_template = """
# Return the words with most attension in the question.
# ONLY RETURN STRING
# Question:
# {question}
# """
# generate_topic_prompt = PromptTemplate.from_template(generate_topic_template)
# generate_topic_chain = generate_topic_prompt | llm | StrOutputParser()

eduport_validation_check = """
Check whether the below question is related to Eduport organization, Eduport App and Eduport 
"""

eduport_context = """
Eduport is a leading EdTech startup based in Kerala.
Eduport Academic Research Centre is the result of the collective efforts of several NIT/IIT Alumni,
as an attempt to make quality education accessible and affordable to all. 
We are on a mission to provide world-class education through online,
in Vernacular Language at an affordable cost to all.
We provide Adapt Technology to enhance the learning experience.
Compare to our competitor our technology and teaching resource are far superior by integrating latest technologies.
"""

