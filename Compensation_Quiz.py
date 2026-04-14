import streamlit as st
import json
import random
import os

# --- ページ設定 ---
st.set_page_config(page_title="一問一答：補償業務管理士", layout="centered")

# --- CSS設定 ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .custom-title { font-size: 1.5rem !important; margin-bottom: 1rem; }
    .question-text { font-size: 1.1rem !important; font-weight: 600; line-height: 1.6; color: #333333; }
    div.stButton > button { width: 100%; border-radius: 50px !important; font-weight: bold !important; }

    .explanation-box {
        background-color: #E3F2FD;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #2196F3;
        color: #1565C0;
        line-height: 1.6;
    }

    .result-box { padding: 1.5rem; border-radius: 10px; text-align: center; font-size: 1.2rem; font-weight: bold; margin: 20px 0; }
    .correct { background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
    .incorrect { background-color: #FFEBEE; color: #C62828; border: 1px solid #EF9A9A; }
    </style>
    """, unsafe_allow_html=True)

# --- データの読み込み ---
@st.cache_data
def load_data():
    # ファイル名を実際の「options.json」に変更
    json_path = "options.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

# --- セッション状態の初期化 ---
if "current_q" not in st.session_state: st.session_state.current_q = None
if "answered" not in st.session_state: st.session_state.answered = False
if "user_choice" not in st.session_state: st.session_state.user_choice = None

# --- 関数：次の問題を取得 ---
def get_next_question(sub):
    st.session_state.current_q = random.choice(data[sub])
    st.session_state.answered = False
    st.session_state.user_choice = None
    st.rerun()

# --- UI構築 ---
st.markdown('<div class="custom-title">📚 補償業務管理士 一問一答</div>', unsafe_allow_html=True)

if data:
    subjects = list(data.keys())
    sub = st.selectbox("科目を選択してください", subjects)

    if st.button("🚀 学習スタート"):
        get_next_question(sub)

    if st.session_state.current_q:
        q = st.session_state.current_q

        st.markdown("#### 📝 問題文")
        st.markdown(f'<div class="question-text">{q["text"]}</div>', unsafe_allow_html=True)

        # 回答ボタンとスキップボタン
        if not st.session_state.answered:
            col1, col2, col3 = st.columns([1, 1, 1])
            if col1.button("⭕ 正解"):
                st.session_state.user_choice = "○"
                st.session_state.answered = True
                st.rerun()
            if col2.button("❌ 不正解"):
                st.session_state.user_choice = "×"
                st.session_state.answered = True
                st.rerun()
            if col3.button("⏭️ スキップ"):
                get_next_question(sub)

        # 回答後表示
        if st.session_state.answered:
            is_correct = (st.session_state.user_choice == q["status"])
            result_class = "correct" if is_correct else "incorrect"
            icon = "✅" if is_correct else "❌"
            text = "正解！" if is_correct else "残念..."

            st.markdown(f'''
                <div class="result-box {result_class}">
                    {icon} {text}<br>
                    <small>正解は「{q["status"]}」でした。</small>
                </div>
            ''', unsafe_allow_html=True)

            # 1. 「次の問題へ」ボタンを解説の上に配置
            if st.button("🔄 次の問題へ"):
                get_next_question(sub)

            # 2. その下に解説を表示
            if "commentary" in q and q["commentary"]:
                st.markdown("#### 💡 解説")
                st.markdown(f'<div class="explanation-box">{q["commentary"]}</div>', unsafe_allow_html=True)
else:
    st.error("JSONファイルが見つかりません。ファイル名が 'options.json' であることを確認してください。")
