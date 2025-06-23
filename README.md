# 📘 Gemini-Powered Academic Title Generator

This is a Streamlit-based web app that generates academic paper titles using Google's Gemini language models (Pro/Flash 2.x or 2.5).

## ✨ Features

- Multi-language UI (Korean & English)
- Supports Gemini 2.0 / 2.5 (Pro & Flash)
- Input abstract and keywords to generate up to 20 titles
- Allows manual selection of favorite titles
- AI recombines selected titles into 5 final suggestions
- Download results as a `.txt` file

## 🚀 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run gemini_title_gen.py
물론이죠 김 님! 😄
아래에 Streamlit 배포를 위한 requirements.txt 파일과, 영어로 작성된 깔끔한 README.md 템플릿을 만들어드리고,
이 두 파일을 GitHub 저장소에 올리는 방법까지 함께 정리해드릴게요.

📦 1. requirements.txt
streamlit
google-generativeai


👉 이 파일은 .py 코드와 같은 폴더에 저장하세요. (requirements.txt라는 이름으로)

📘 2. README.md (영문 템플릿 예시)
# 📘 Gemini-Powered Academic Title Generator

This is a Streamlit-based web app that generates academic paper titles using Google's Gemini language models (Pro/Flash 2.x or 2.5).

## ✨ Features

- Multi-language UI (Korean & English)
- Supports Gemini 2.0 / 2.5 (Pro & Flash)
- Input abstract and keywords to generate up to 20 titles
- Allows manual selection of favorite titles
- AI recombines selected titles into 5 final suggestions
- Download results as a `.txt` file

## 🚀 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run gemini_title_gen.py


You must provide your Google Gemini API key. Create one at https://makersuite.google.com/app/apikey.
🌐 Streamlit Cloud Deployment
To deploy this app on Streamlit Community Cloud:
- Fork or clone this repo to your own GitHub.
- Log in to Streamlit Cloud with your GitHub account.
- Create a new app and point to gemini_title_gen.py.
- Done!

📄 License
MIT License
