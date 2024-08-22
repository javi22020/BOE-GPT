import openai

client = openai.OpenAI(base_url="http://localhost:4550/v1")

resp = client.chat.completions.create(
    model="phi-3.5-mini-instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
)

print(resp)