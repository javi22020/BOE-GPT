import openai

client = openai.OpenAI(base_url="http://localhost:4550/v1")

for r in client.chat.completions.create(
    model="phi-3.5-mini-instruct",
    messages=[
        {
            "role": "user",
            "content": "Write a poem"
        }
    ],
    stream=True
):
    if r.choices[0].delta.content is not None:
        print(r.choices[0].delta.content, end="")