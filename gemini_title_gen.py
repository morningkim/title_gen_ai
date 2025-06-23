import streamlit as st
import google.generativeai as genai
import datetime

st.set_page_config(page_title="📘 논문 제목 생성기", page_icon="📘")

# 초기 상태 설정
defaults = {
    "lang": "ko",
    "api_key": "",
    "generated_titles": [],
    "selected_titles": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# 언어 선택 (오른쪽 상단)
top1, top2 = st.columns([7, 1])
with top2:
    lang_flag = st.selectbox(" ", ["🇰🇷", "🇺🇸"], label_visibility="collapsed")
    st.session_state["lang"] = "ko" if "🇰🇷" in lang_flag else "en"
is_ko = st.session_state.lang == "ko"

# 텍스트 다국어 대응
T = {
    "title": "📘 논문 제목 생성기" if is_ko else "📘 Academic Title Generator",
    "api_key": "Gemini API 키 입력" if is_ko else "Enter Gemini API Key",
    "api_help": "[API 키 발급 링크](https://makersuite.google.com/app/apikey)",
    "model": "Gemini 모델 선택",
    "abs_lang": "초록 언어" if is_ko else "Abstract Language",
    "title_lang": "제목 생성 언어" if is_ko else "Title Output Language",
    "rules": "1️⃣ 제목 생성 규칙",
    "word_limit": "최대 단어 수",
    "style": "제목 스타일",
    "guide": "제목 가이드라인",
    "examples": "2️⃣ 예제 입력",
    "num_examples": "예제 개수",
    "new_input": "3️⃣ 새 초록 및 키워드 입력",
    "abstract": "초록",
    "keywords": "키워드 (쉼표로 구분)",
    "title_input": "제목",
    "generate": "🚀 제목 생성 (최대 20개)",
    "select_titles": "✅ 생성된 제목 중 선택",
    "combine_titles": "🔁 선택한 제목들 조합하여 5개 추천",
    "result": "🎯 최종 추천 제목",
    "download": "📥 다운로드 (.txt)",
    "warning": "⚠️왼쪽 입력창에Gemini API 키를 입력해주세요." if is_ko else "Please enter your Gemini API key in the left sidebar."
}
style_opts = ["학술적", "간결한", "창의적인"] if is_ko else ["Academic", "Concise", "Creative"]

# 사이드바 구성
st.sidebar.header("⚙️ 설정")
model_id = st.sidebar.selectbox(T["model"], [
    "gemini-2.5-pro-preview-06-05",
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.0-pro",
    "gemini-2.0-flash"
])
st.sidebar.markdown(T["api_help"])
st.session_state.api_key = st.sidebar.text_input(
    T["api_key"], type="password", value=st.session_state.api_key)
if not st.session_state.api_key:
    st.warning(T["warning"])
    st.stop()
genai.configure(api_key=st.session_state.api_key)

# 페이지 제목
st.markdown(f"<h1 style='font-size:38px; text-align:center; margin-bottom:20px;'>{T['title']}</h1>", unsafe_allow_html=True)

# 1️⃣ 제목 생성 규칙
st.markdown(f"<h3 style='font-size:26px;'>{T['rules']}</h3>", unsafe_allow_html=True)
abs_lang = st.radio(T["abs_lang"], ["🇰🇷 한국어", "🇺🇸 English"], horizontal=True)
title_lang = st.radio(T["title_lang"], ["🇰🇷 한국어", "🇺🇸 English"], horizontal=True)
title_lang_code = "Korean" if "🇰🇷" in title_lang else "English"
max_words = st.number_input(T["word_limit"], min_value=1, value=12)
style = st.selectbox(T["style"], style_opts)
guide = st.text_input(T["guide"])

# 2️⃣ 예제 입력
st.markdown(f"<h3 style='font-size:26px; margin-top:30px;'>{T['examples']}</h3>", unsafe_allow_html=True)
num_examples = st.number_input(T["num_examples"], min_value=1, max_value=10, value=3)
examples = []
for i in range(int(num_examples)):
    with st.expander(f"📄 예제 {i+1}"):
        t = st.text_input(f"{T['title_input']}", key=f"t_{i}")
        a = st.text_area(f"{T['abstract']}", key=f"a_{i}", height=120)
        k = st.text_input(f"{T['keywords']}", key=f"k_{i}")
        if t and a:
            examples.append((t, a, k))

# 3️⃣ 새 초록 입력
st.markdown(f"<h3 style='font-size:26px; margin-top:30px;'>{T['new_input']}</h3>", unsafe_allow_html=True)
new_abs = st.text_area(T["abstract"], height=180)
new_kw = st.text_input(T["keywords"])

# 🚀 제목 생성 버튼
if st.button(T["generate"]):
    prompt = (
        f"You are a professional academic paper title assistant.\n"
        f"Generate up to 20 creative and clear titles in {title_lang_code}.\n"
        f"Style: {style}\nMax word count: {max_words}\n"
    )
    if guide:
        prompt += f"Guideline: {guide}\n"
    prompt += "\n### Examples:\n"
    for t, a, k in examples:
        prompt += f"Abstract: {a}\nKeywords: {k}\nTitle: {t}\n\n"
    prompt += "\n### NEW TASK:\n"
    prompt += f"Abstract: {new_abs.strip()}\nKeywords: {new_kw.strip()}\nTitle:"

    try:
        model = genai.GenerativeModel(model_id)
        res = model.generate_content(prompt)
        titles = [line.strip("•- ") for line in res.text.splitlines() if line.strip()]
        st.session_state.generated_titles = titles
        st.session_state.selected_titles = []
    except Exception as e:
        st.error(f"Gemini 오류: {e}")

# ✅ 생성된 제목 목록 & 체크 선택
if st.session_state.generated_titles:
    st.markdown(f"### {T['select_titles']}")
    selected = []

    for i, title in enumerate(st.session_state.generated_titles):
        key = f"title_chk_{i}"
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.write(f"**{i+1}. {title}**")
        with col2:
            checked = st.checkbox("✔", value=st.session_state.get(key, False), key=key)
            if checked:
                selected.append(title)

    st.session_state.selected_titles = selected


# 🔁 선택된 제목 조합 요청
if st.session_state.selected_titles and st.button(T["combine_titles"]):
    prompt = (
        f"You are an academic paper title generator.\n"
        f"Analyze the following {len(st.session_state.selected_titles)} selected titles.\n"
        f"Combine their strengths, structure, and style to generate 5 creative and high-quality paper titles in {title_lang_code}.\n\n"
    )
    for t in st.session_state.selected_titles:
        prompt += f"- {t}\n"
    prompt += "\nOnly return 5 distinct titles."

    try:
        model = genai.GenerativeModel(model_id)
        res2 = model.generate_content(prompt)
        final_titles = res2.text.strip()

        st.markdown(f"<h3 style='font-size:24px; margin-top:30px;'>{T['result']}</h3>", unsafe_allow_html=True)
        st.text(final_titles)

        filename = f"titles_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{title_lang_code}.txt"
        st.download_button(T["download"], data=final_titles, file_name=filename)

    except Exception as e:
        st.error(f"Gemini 오류: {e}")
