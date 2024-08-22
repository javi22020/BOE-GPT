from langgraph.prebuilt import create_react_agent
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
agent = create_react_agent(
    model=ChatOpenAI(
        base_url="http://llm:4550/v1",
        streaming=True
    ),
    tools=[
        WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper()
        )
    ]
)

if __name__ == "__main__":
    for m in agent.stream(input={"messages": [{"role": "user", "content": "What is the population of the capital of France? Search in Wikipedia."}]}):
        print(m)