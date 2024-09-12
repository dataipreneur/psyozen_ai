from langchain.prompts import PromptTemplate
from bot_config import summary_kb, response_kb, question_kb, recommendation_kb

## Prompt templates

summary_prompt = PromptTemplate(
    input_variables=["current_summary", "prompt", "text", "emotion"],
    template=f"Use the following examples as a guide to generate a new summary and pass it to response:\n{summary_kb} based on identified emotions {{emotion}}.\nCurrent Summary: {{current_summary}}\nPrompt: {{prompt}}\nText: {{text}}\nNew Summary:"
)


response_prompt = PromptTemplate(
    input_variables=["current_summary", "text", "emotion"],
    template=f"""The following is a conversation with an AI therapist. The therapist is empathetic, helpful, creative, clever, and very friendly. Use these examples as a guide:

{response_kb}

Please address the person by name only if he/she/they introduce themselves.
Now, generate a response for:
Current Summary: {{current_summary}}
Text: {{text}}
Identified emotions: {{emotion}} Please be mindful of persons's emotion and empatheic while generating the response.
Response:"""
)

question_prompt = PromptTemplate(
    input_variables=["text", "response", "emotion"],
    template=f"""Use these examples as a guide to generate a follow-up question considering {{emotion}} too:

{question_kb}

Now, generate a question for:
Text: {{text}}
Response: {{response}}
Please me mindful and empathetic while generating a question.
Question:"""
)

recommendation_prompt = PromptTemplate(
    input_variables=["user", "assistant"],
    template=f"""Following is a sample of converastion with corresponding recommendation:

{recommendation_kb}

Now, generate a recommendation for the following conversation in bullet points and keep it brief:
User: {{user}}
Assistant: {{assistant}}
Recommendation:"""
)

