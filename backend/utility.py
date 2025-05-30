import os
import openai
import dotenv
from pydantic import BaseModel
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import  OpenAIEmbeddings

dotenv.load_dotenv(".env")


class OutputModel(BaseModel):
    llm_response: str
    
openai_client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)

embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_BASE_URL"], model=os.environ["EMBEDDING_MODEL_NAME"]
)

vector_store = AzureSearch(
    azure_search_endpoint=os.environ["SEARCH_SERVICE_ENDPOINT"],
    azure_search_key=os.environ["SEARCHKEY"],
    index_name=os.environ["SEARCH_INDEX"],
    embedding_function=embeddings.embed_query,
)
def llm_call_structured(system_prompt, prompt, model, response_format = OutputModel):

        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        completion = openai_client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format,
        )
        
        return completion