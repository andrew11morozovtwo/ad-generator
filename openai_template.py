from openai import OpenAI

client = OpenAI(
    api_key="<КЛЮЧ>",
    base_url="https://api.proxyapi.ru/openai/v1",
)

response = client.responses.create(
    model="gpt-4o", 
    input="Привет!"
)