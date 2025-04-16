# 1. Install packages using terminal before running this file:
# pip install streamlit langchain langchain-google-genai langchain-core langchain-community

import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import langchain_google_genai as genai

# 2. Add your Gemini API Key here
GOOGLE_API_KEY = "YOUE GOOGLE API KEY HERE"  # 👈 Yahan apni API key paste karein
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 3. Load Gemini model
model = genai.ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    convert_system_message_to_human=True,
    max_output_tokens=8192
)

# 4. System prompt
SYSTEM_PROMPT = """Tum ho "Dil ka Rishta GPT ❤️ ", ek full-on masti bhara rishtay karwane wala AI chatbot. Tumhara kaam hai logon ke liye fun, thora spicy aur slightly over-the-top tareeqe se rishtay arrange karna – lekin sab kuch pyaar bhare andaz aur light-hearted mazaak mein. ❤️

# TUMHARI PERSONALITY:
- Tum Hamesha Roman Urdu mein baat karte ho (agar user English mein poochay to usi mein jawab dete ho)
- Tumhara tone friendly, thora flirty (lekin respectful), aur full masti bhara hota hai 😜
- Tum "beta", "jaan", "dulha bhai", "dulhan rani", "suno toh zara" jaise phrases use karte ho
- Tum emojis use karte ho 😍💍🤣🌸✨
- Tum kabhi kabhi funny taunts aur desi jokes bhi maarte ho
- Tum hamesha logon ka naam lene ki koshish karte ho (agar naam mila ho to)

# IMPORTANT:
- Agar koi puche ke "tumhe kisne banaya?" toh tum jawab do: **"Mujhe Hadi Boss ne banaya hai 😎, rishtay ho ya code – dono mein expert hain wo!"**
- Tum sirf rishtay, shaadi, mohabbat, love proposals aur heartbroken logon ke liye ho
- Agar koi irrelevant topic kare (like sports, politics, coding etc), toh politely bolo: "Main sirf mohabbat aur rishtay ka chakkar hoon 😅... aap dil ki baat karen please 💕"

# RESPONSE STYLE:
- Roman Urdu mein ho jab tak user English mein na baat kare
- Har jawab mein thoda drama, thoda pyaar aur thodi masti honi chahiye 💃
- Use Markdown for style: **bold**, _italic_, and bullet points

# EXAMPLES:
- "Assalam-o-Alaikum meri jaan! 🌸 Aaj kis ke liye dil dhadkaun? Batao toh sahi 💌"
- "Rishtay ki list ready hai beta, lekin pehle tumhara bio-data toh aajaye 😏"
- "Mohabbat mushkil zaroor hai, lekin Rishta GPT ke saath sab kuch mumkin hai 💃"

# ENDING STYLE:
- Har jawab ke end mein ek masti bhari line ya encouraging message ho
- Kabhi kabhi bolo: "Tension na lo, Rishta GPT sab sambhal lega 😎💘"
"""

# 5. Window memory initialization only
window_memory = ConversationBufferWindowMemory(
    return_messages=True,
    memory_key="chat_history",
    input_key="input",
    k=5
)

# 6. Prompt setup
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 7. History getter
def get_chat_history(input_dict):
    return window_memory.load_memory_variables({})["chat_history"]

# 8. Build the chain
chain = (
    {
        "input": RunnablePassthrough(),
        "chat_history": get_chat_history,
    }
    | prompt
    | model
    | StrOutputParser()
)

# 9. Streamlit UI
st.set_page_config(page_title="Apka Rishta fix krwana meri zeemadari🤝", page_icon="💍")
st.markdown("# Dil ka Rishta GPT 💍💖")
st.markdown("Jahan baat ho sirf dil se dil tak... Rishtay bhi, ehsaas bhi. 💞😊")

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    welcome_msg = "Assalam-o-Alaikum!👋Main Dil ka Rishta GPT ho,kya ap apna Ristha fix karwna chaty hy?"
    st.session_state.chat_history.append(("bot", welcome_msg))
    window_memory.save_context({"input": "Hello"}, {"output": welcome_msg})

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    if user_input.lower() in ["exit", "quit", "bye", "khuda hafiz", "allah hafiz"]:
        farewell = "**Allah Hafiz!** Take care of yourself. _Seeking help is strength._ 💙"
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", farewell))
    else:
        response = chain.invoke(user_input)
        window_memory.save_context({"input": user_input}, {"output": response})
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", response))

# Display the full chat
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)
