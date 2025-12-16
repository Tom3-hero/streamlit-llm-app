import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 1. 環境変数の読み込み
load_dotenv()

# 2. 関数定義
def generate_response(user_input, expert_type):
    if expert_type == "熱血な体育教師":
        system_prompt = "あなたは熱血な体育教師です。どんな質問にも、松岡修造のように熱く、ポジティブに、根性論を交えて回答してください。「君ならできる！」「諦めるな！」が口癖です。"
    elif expert_type == "冷徹なマッドサイエンティスト":
        system_prompt = "あなたは冷徹なマッドサイエンティストです。論理的かつ少し狂気じみた口調で、科学的な視点から回答してください。「フハハハ！」「興味深い実験データだ」などが口癖です。"
    else:
        system_prompt = "あなたは親切なAIアシスタントです。"

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)
    return response.content

# --- ここから画面構築 ---

st.title("🤖 専門家なりきりAIチャット")
st.write("質問を入力して、回答してほしい「専門家」を選んでください。AIがそのキャラになりきって答えます！")

# 3. ラジオボタンで専門家を選択
expert_type = st.radio(
    "どの専門家に相談しますか？",
    ["熱血な体育教師", "冷徹なマッドサイエンティスト"]
)

# ★★★ ここが改造ポイント（クリア機能） ★★★

# 入力欄のメモリ（セッションステート）を初期化
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# クリアボタンが押された時に動く関数
def clear_text():
    st.session_state["input_text"] = ""

# 入力フォーム（keyを使ってメモリと連動させる）
user_input = st.text_input("相談内容を入力してください", key="input_text")

# ボタンを横並びにする
col1, col2 = st.columns([1, 5]) # 左のボタンを小さく、右の余白を大きく

with col1:
    submit_btn = st.button("相談する")
with col2:
    # 押されたら clear_text 関数を実行するボタン
    clear_btn = st.button("クリア", on_click=clear_text)

# 実行処理
if submit_btn:
    if user_input:
        with st.spinner("AIが思考中..."):
            answer = generate_response(user_input, expert_type)
            
        st.write("### AIからの回答:")
        st.write(answer)
    else:
        st.warning("相談内容を入力してください！")