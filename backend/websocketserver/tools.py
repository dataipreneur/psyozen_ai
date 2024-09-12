from langchain.llms import OpenAI
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import LLMChain
from langchain.llms import Ollama
from prompt_template import summary_prompt, response_prompt, question_prompt, recommendation_prompt
import os
import dotenv

dotenv.load_dotenv()

llm = OpenAI(temperature=0.7, openai_api_key = os.getenv("OPENAI_API_KEY"))

#llm = Ollama(model="stablelm-zephyr", base_url="http://127.0.0.1:11434")

tracer = LangChainTracer(project_name="PsyOzen")

## With LangSMith Tracer

summary_chain = LLMChain(llm=llm, prompt=summary_prompt, callbacks=[tracer])
response_chain = LLMChain(llm=llm, prompt=response_prompt, callbacks=[tracer])
question_chain = LLMChain(llm=llm, prompt=question_prompt, callbacks=[tracer])
recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt, callbacks=[tracer])
