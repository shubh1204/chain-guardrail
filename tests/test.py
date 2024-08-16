from langchain_community.chat_models import ChatOllama
from src.chain_guardrail.main import ChainValidator

model = ChatOllama(
    base_url='http://localhost:11434',
    model="llama3",
    temperature=0,
)
validator_obj = ChainValidator()

chain = model | validator_obj.static_validator
print(chain.invoke(
    "Return the following text as it is : TEXT:  You are an Asshole. He was calling me an ASSHole, hahaha. My name is Rio Asher-James and my mobile is +91-7053654462"))
