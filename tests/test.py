from langchain_community.chat_models import ChatOllama
from src.chain_guardrail.main import ChainValidator

model = ChatOllama(
    base_url='http://localhost:11434',
    model="llama3",
    temperature=0,
)
validator_obj = ChainValidator()

chain = model | validator_obj.static_validator
print(chain.invoke("Return the following text as it is : Text : fuck this shit"))
