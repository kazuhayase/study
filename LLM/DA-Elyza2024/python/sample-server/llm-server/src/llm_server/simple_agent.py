from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI


def ask_question(question: str) -> str:
    llm = OpenAI(temperature=0.9)
    template = """Question: {question}

    Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    chain = prompt | llm

    answer = chain.invoke({"question": question})
    return answer
