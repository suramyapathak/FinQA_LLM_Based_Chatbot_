#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openai
import streamlit as st
import toml
from streamlit_chat import message


# In[2]:


secrets = toml.load("secrets.toml")


# In[3]:


api_key=st.secrets["key"]


# In[10]:


client = openai.OpenAI(
    api_key=api_key,
)
def get_completion_from_messages(prompt, model='gpt-3.5-turbo'):
    message=[{'role':'user', 'content':str(prompt),}]
    response=client.chat.completions.create(
    model=model,
    messages=message,
    temperature=0)
    return response.choices[0].message.content


# In[ ]:





# In[11]:


def get_initial_message():
    text = f"""
five-year performance comparison 2013 the following graph provides an indicator of cumulative total\
shareholder returns for the corporation as compared to the peer group index ( described above ) , \
the dj trans , and the s&p 500 . the graph assumes that $ 100 was invested in the common stock of \
union pacific corporation and each index on december 31 , 2011 and that all dividends were \
reinvested . the information below is historical in nature and is not necessarily indicative of \
future performance . purchases of equity securities 2013 during 2016 , we repurchased 35686529 \
shares of our common stock at an average price of $ 88.36 . the following table presents common \
stock repurchases during each month for the fourth quarter of 2016 : period total number of shares \
purchased [a] average price paid per share total number of shares purchased as part of a publicly \
announced plan or program [b] maximum number of shares remaining under the plan or program [b] . \
period the oct . 1 through oct . 31 of total number of shares purchased [a] is 3501308 ; the oct . 1\
 through oct . 31 of average price paid per share is $ 92.89 ; the oct . 1 through oct . 31 of total\
 number of shares purchased as part of a publicly announcedplan or program [b] is 3452500 ; the oct\
 . 1 through oct . 31 of maximum number of shares remaining under the plan or program [b] is \
23769426 ; period the nov . 1 through nov . 30 of total number of shares purchased [a] is 2901167 ;\
 the nov . 1 through nov . 30 of average price paid per share is 95.68 ; the nov . 1 through nov . \
30 of total number of shares purchased as part of a publicly announcedplan or program [b] is 2876067\
 ; the nov . 1 through nov . 30 of maximum number of shares remaining under the plan or program [b] \
is 20893359 ; period the dec . 1 through dec . 31 of total number of shares purchased [a] is 3296652\
 ; the dec . 1 through dec . 31 of average price paid per share is 104.30 ; the dec . 1 through dec \
. 31 of total number of shares purchased as part of a publicly announcedplan or program [b] is \
3296100 ; the dec . 1 through dec . 31 of maximum number of shares remaining under the plan or \
program [b] is 17597259 ; period the total of total number of shares purchased [a] is 9699127 ; the \
total of average price paid per share is $ 97.60 ; the total of total number of shares purchased as\
 part of a publicly announcedplan or program [b] is 9624667 ; the total of maximum number of shares\
 remaining under the plan or program [b] is n\a ; [a] total number of shares purchased during the \
quarter includes approximately 74460 shares delivered or attested to upc by employees to pay stock\
 option exercise prices , satisfy excess tax withholding obligations for stock option exercises or\
 vesting of retention units , and pay withholding obligations for vesting of retention shares . [b] \
effective january 1 , 2014 , our board of directors authorized the repurchase of up to 120 million \
shares of our common stock by december 31 , 2017 . these repurchases may be made on the open market \
or through other transactions . our management has sole discretion with respect to determining the \
timing and amount of these transactions . on november 17 , 2016 , our board of directors approved \
the early renewal of the share repurchase program , authorizing the repurchase of up to 120 million \
shares of our common stock by december 31 , 2020 . the new authorization was effective january 1 ,\
 2017 , and replaces the previous authorization , which expired on december 31 , 2016."""

    messages=[ {'role':'system', 'content':f"""
you are a chatbot, ask user for the question. go through the given the information in '''{text}''' to answer the question: """
} ]
    return messages


# In[12]:


def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


# In[15]:


st.set_page_config(page_title="FinQA Chatbot using Prompt Engineering (GPT-3.5)")
st.title("FinQA Chatbot using Prompt Engineering (GPT-3.5)")
st.sidebar.markdown("Current Version: 0.0.1")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []
    
query = st.text_input("Question: ", "Say Hello ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
    
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_completion_from_messages(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')






