
from youtube import youtube_search
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

system_template = SystemMessagePromptTemplate.from_template("You are a helpful AI bot")
placeholder = MessagesPlaceholder(variable_name="chat_history", optional=True)
human_template = HumanMessagePromptTemplate.from_template("{input}")
scratchpad = MessagesPlaceholder(variable_name="agent_scratchpad")

agent_prompt = ChatPromptTemplate.from_messages(
    [
        system_template,
        placeholder,
        human_template,
        scratchpad
    ]
)

tool_list = [youtube_search]

agent = create_openai_tools_agent(
    llm=llm,
    tools=tool_list,
    prompt=agent_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tool_list,
    verbose=True
)

message_history = ChatMessageHistory()
agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

while (True):
    user_input = input("Please enter some text: \n")
    user_input = user_input.lower().strip()
    if user_input == "exit":
        break

    response = agent_with_history.invoke(
        {"input": user_input}, 
        config={"configurable": {"session_id": "<foo>"}}
    )



