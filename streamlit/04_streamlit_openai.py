from openai import OpenAI
import streamlit as st 
import time

assistant_id = st.secrets["assistant_id"]
thread_id = st.secrets["thread_id"]

iframe_html = '''<iframe src="https://ads-partners.coupang.com/widgets.html?id=786033&template=banner&trackingCode=AF5361443&subId=&width=300&height=250" width="300" height="250" frameborder="0" scrolling="no" referrerpolicy="unsafe-url" browsingtopics></iframe>'''
bed_html = '''<a href="https://link.coupang.com/a/bGo0X5" target="_blank" referrerpolicy="unsafe-url"><img src="https://img5a.coupangcdn.com/image/affiliate/banner/7abc281112688ec0252dd6c8e9ab0828@2x.jpg" alt="무설치 낮잠 접이식침대 6단계 조정 대형 휴대용 야전침대 소음 없고 접이식 싱글침대" width="120" height="240"></a>'''
rick_html='''<iframe src="https://coupa.ng/cfCxDh" width="120" height="240" frameborder="0" scrolling="no" referrerpolicy="unsafe-url" browsingtopics></iframe>'''
    


with st.sidebar:

    openai_api_key = st.text_input("OpenAi API KEY", type="password")
    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID", value=thread_id )

    thread_make_btn = st.button("Create a new thread")
    if thread_make_btn:
        # 스레드 생성
        thread = client.beta.threads.create()
        thread_id = thread.id
        st.subheader(f"{thread_id}", divider ="rainbow")
        st.info("새로운 쓰레드가 생성되었습니다.")

    
    
    st.link_button("""고마..고마 한푼만 주이소..\n한푼만 주시믄 우리 아들 경식이가\n오늘 한끼를 먹을 수 있십니도...\n
                   (이곳을 클릭해 경식이 한끼 먹이기.)""","https://toss.me/profmin")
    
    st.markdown(iframe_html, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(bed_html, unsafe_allow_html=True)
    with col2:
        st.markdown(rick_html, unsafe_allow_html=True)
    st.info("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "반갑다냥 뭘 도와줄까냥" }]

print(f"st.session_state\n{st.session_state}")
print()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


prompt = st.chat_input()
if prompt:
    #client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role" : "user", "content": prompt})
    st.chat_message("user").write(prompt)

    #response = client.chat.completions.create(model='gpt-3.5-turbo', messages=st.session_state.messages)
    response = client.beta.threads.messages.create(thread_id = thread_id, role="user", content =prompt)

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed" :
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value
    st.session_state.messages.append({"role": "assistant", "content": assistant_content })
    st.chat_message("assistant").write(assistant_content)

    print(st.session_state.messages)
