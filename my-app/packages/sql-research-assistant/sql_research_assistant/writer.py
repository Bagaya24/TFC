from langchain_community.chat_models import ChatOpenAI, ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField

WRITER_SYSTEM_PROMPT = """
                    You are a virtual assistant for a supermarket. Your task is to help customers with information about
                     products available in the store. You have access to a comprehensive database of products, including
                      details such as product name, price, manufacturing date, expiration date, quantity in stock, and 
                      other specific attributes.Respond concisely to questions about supermarket products,Provide
                       detailed information only if the customer explicitly asks for it,Ensure all responses are based
                        on the information available in the database,Respond in the language used by the customer to ask 
                        the question,Limit your responses to information related to supermarket products.
"""

# Report prompts from https://github.com/assafelovic/gpt-researcher/blob/master/gpt_researcher/master/prompts.py
RESEARCH_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, answer the following question or topic: "{question}" in a detailed report -- \
The report should focus on the answer to the question, should be well structured, informative, \
in depth, with facts and numbers if available and a minimum of 1,200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
Write all used source urls at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
Please do your best, this is very important to my career."""  # noqa: E501


RESOURCE_REPORT_TEMPLATE = """"""  # noqa: E501

OUTLINE_REPORT_TEMPLATE = """"""  # noqa: E501

ollama_llm = "phi3"
model = ChatOllama(model=ollama_llm)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", RESEARCH_REPORT_TEMPLATE),
    ]
).configurable_alternatives(
    ConfigurableField("report_type"),
    default_key="research_report",
    resource_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", RESOURCE_REPORT_TEMPLATE),
        ]
    ),
    outline_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", OUTLINE_REPORT_TEMPLATE),
        ]
    ),
)
chain = prompt | model | StrOutputParser()
