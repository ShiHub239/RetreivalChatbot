
from youtube import youtube_search
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



load_dotenv()

llm = OpenAI()

conversation = ConversationChain(
    llm = llm,
    memory = ConversationSummaryBufferMemory(llm = llm),
    verbose = True
)

while (True):
    user_input = input("Please enter some text: \n")
    user_input = user_input.lower().strip()
    if user_input == "exit":
        break
    if "youtube" in user_input and "search" in user_input:
        video_list =youtube_search(user_input, 25)
        print(video_list)
    else:
        response = conversation.predict(input = user_input)
        print(response)



