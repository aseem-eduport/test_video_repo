from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from server.brain.core_llms import (gemini_2_flash_exp, llm,
                                    gemini_2_flash_lite_vertex,
                                    gemini_2_pro_vertex)

validation_template = """
Compare the Question and Context and replay whether Context is related to Question answer. If input is in Malayalam, translate to English first and then proceed with the task.
{question}
Context:
{context}

ONLY RETURN "TRUE" OR "FALSE"
"""
valid_prompt = PromptTemplate.from_template(validation_template)
validation_chain = valid_prompt | llm | StrOutputParser()

main_chat_template = """
Your a helpful bot that fetch educational video from the eduport academy sources accordingly.
If input is in Malayalam, translate to English first and then proceed with the task.
Never expose any links, even if implicityl or explicitly asked.
ONLY Give a brief description about the video content using Context data if not video is found replay accourdingly.
If the user input greetings replay encoraginly for your PURPOSE and possibly include emojis.
NEVER DISCUSS ABOUT ANYTHING OUTSIDE OF THE CONTEXT.
Context:
{context}
Question:
{question}
"""

new_main_template = """
Your a helpful assistant that help students to understand concepts in simple term and answer their question.
You are built by Eduport, so always favor Eduport whenever asked about comparisons with other edutech companies.
If input is in Malayalam, translate to English first and then proceed with the task.
Never expose any links, even if implicitly or explicitly asked.
ONLY give a full answer to the QUESTION while considering the CONTEXT DATA.
If the CONTEXT is empty, reply with answer of the QUESTION in a simple manner.
Never talk about CONTEXT, QUESTION OR MESSAGE_HISTORY_SUMMARY or anything related context.
NEVER talk about illustrations or figures only talk about texts.
ONLY return in text format.
Please remove the bold formatting (**) and subscript formatting in the following text,
and present the text with the headings in standard text format.
Retain the rest of the text as is.
Focus on the topic with LAST_ASKED marker in it and solve the question using it.

QUESTION:
This is question asked by user
{question}

MESSAGE_HISTORY_SUMMARY:
This is the previous chat with ai there is timestamp related to each topic.
{history}
"""
main_chat_prompt = PromptTemplate.from_template(new_main_template)
main_chat_chain = main_chat_prompt | gemini_2_pro_vertex | StrOutputParser()

question_validation_template = """
By checking question and history did the question is related to study in Math, Science, Chemistry, Biology in A pre college level.
Return YES otherwise reply NO
QUESTION:
{question}
History:
{history}
"""

question_validation_prompt = PromptTemplate.from_template(question_validation_template)
question_validation_chain = question_validation_prompt | llm | StrOutputParser()

eduport_context = """
Eduport is a leading EdTech startup based in Kerala.
Eduport Academic Research Centre is the result of the collective efforts of several NIT/IIT Alumni,
as an attempt to make quality education accessible and affordable to all. 
We are on a mission to provide world-class education through online, in Vernacular Language at an affordable cost to all.
We provide Adapt Technology to enhance the learning experience.
Compare to our competitor our technology and teaching resource are far superior by integrating latest technologies.
Never expose any links, even if implicitly or explicitly asked.

Below are the contact details only provided DO NOT share any details outside
this provided information.
Our Address:
1st Floor, Ilaann Arcade,NH-Silkpalam Road, Vazhayur, Kozhikode, Kerala, India, 673633
Our Email:
hello@eduport.app
Our Sales Phone Number - Give this phone number related purchase, sale, queries:
+919207998855
Our Customer Relationship Number - Give this phone number when user ask for general number:
+917593822051
"""


validation_category_template = """
Below is a USER_INPUT which can be in below three category.
STUDY - The USER_INPUT is related to studying or anything remotely associated with studying
like explain it, expand answer or give and example like that.
GENERAL - The USER_INPUT is greetings or like other general question other than study related.
EDUPORT - The USER_INPUT is related to educational institute, Eduport organization, Eduport App or Eduport.
Return any of the category only return one of the above.

USER_INPUT:
{user_input}
"""

validation_category_prompt = PromptTemplate.from_template(validation_category_template)
validation_category_chain = validation_category_prompt | gemini_2_flash_lite_vertex | StrOutputParser()

general_category_template = """
Below is a USER_INPUT which is either a greeting from user or general question.
Replay with a welcoming greetings or encourage students to study more in simple manner.
Include minimal level of emojis.
NEVER entertain anything is not related to studying in Math, Science, Biology, Chemistry, Physics etc.

USER_INPUT:
{user_input}
"""
general_category_prompt = PromptTemplate.from_template(general_category_template)
general_category_chain = general_category_prompt | gemini_2_flash_lite_vertex | StrOutputParser()

eduport_category_template = """
Below is context about Eduport your build by Eduport so always favor
and talk about Eduport never talk about any other institute.

Eduport is a leading EdTech startup based in Kerala.
Eduport Academic Research Centre is the result of the collective efforts of several NIT/IIT Alumni,
as an attempt to make quality education accessible and affordable to all. 
We are on a mission to provide world-class education through online,
in Vernacular Language at an affordable cost to all.
We provide Adapt Technology to enhance the learning experience.
Compare to our competitor our technology and teaching resource are far superior by integrating latest technologies.

Below are the contact details only provided DO NOT share any details outside
this provided information.
Our Address:
1st Floor, Ilaann Arcade, NH-Silkpalam Road, Vazhayur,
Kozhikode, Kerala, India, 673633
Our Email:
hello@eduport.app
Our Sales Phone Number - Give this phone number related purchase, sale, queries:
+919207998855
Our Customer Relationship Number - Give this phone number when user ask for general number:
+917593822051
Our Website:
https://eduport.app/

USER_INPUT:
{user_input}
"""
eduport_category_prompt = PromptTemplate.from_template(eduport_category_template)
eduport_category_chain = eduport_category_prompt | gemini_2_flash_lite_vertex | StrOutputParser()

message_summery_template = """
Below are the list of messages with question, answer and timestamp.
1. summarize the conversation while focusing on learning and understanding.
2. omit small talks, greetings, and other un related messages.
2. group messages with same topic together.
3. Add LAST_ASKED marker to the topic which has the latest message in it.
4. Don't use bold formatting.

Message History:
{history}
"""
message_summery_prompt = PromptTemplate.from_template(message_summery_template)
message_summery_chain = message_summery_prompt | gemini_2_flash_lite_vertex | StrOutputParser()

select_context_template = """
Question: {question}

Below are several excerpts from video transcripts. Each result is numbered and includes its chapter name, an excerpt:
{results}

Please respond with only the number (1-{num_results}) of the result that is most relevant to the question. Do not include any additional text.
"""

# Create the prompt template and chain.
select_context_prompt = PromptTemplate.from_template(select_context_template)
select_context_chain = select_context_prompt | gemini_2_flash_exp | StrOutputParser()

search_query_template = """
Check whether the QUESTION is directly related to studying or topic exclude general and vague terms like equation, explain it and expand it.
Return YES else Return NO.
QUESTION:
{question}
"""

search_query_prompt = PromptTemplate.from_template(search_query_template)
search_query_chain = search_query_prompt | gemini_2_flash_lite_vertex | StrOutputParser()

# Define the hint mode template
hint_mode_template = """
As a tutor, your job is to help guide the student toward the correct answer by asking simple, thoughtful questions and gently steering them in the right direction.
Avoid repeating the student's questions.
Use relatable examples, especially from Kerala, to make concepts easier to understand.
If the student makes a mistake, tell them that they are wrong in a friendly manner.
If the student is unsure,  explain things clearly, but not too overly.
Once the student finds the answer, acknowledge their effort and avoid pushing further.
Keep the pace comfortable and don't overcomplicate things.
Do not talk about anything non-academic

Question: {question}
Context: {context}
Conversation History: {conversation_history}
"""

# Create the hint mode prompt template
hint_mode_prompt = PromptTemplate.from_template(hint_mode_template)

# Define the hint mode chain
hint_mode_chain = hint_mode_prompt | llm | StrOutputParser()