
## 📖 專案簡介 (Introduction)

在資訊爆炸的時代，我們每天都面臨「閱讀焦慮」。看到感興趣的技術文章或新聞，往往因為篇幅太長而放入待讀清單，卻再也沒打開過。

**Podcast AI Studio** 是一個利用生成式 AI (Generative AI) 技術解決此痛點的工具。它能自動爬取網頁內容，利用 LLM 改寫為廣播腳本，並透過高品質語音合成技術，生成「專家 vs. 小白」的雙人對談 MP3。讓使用者用「聽」的來吸收新知。

## ✨ 核心功能 (Key Features)

* **🔗 智能爬蟲 (RAG):** 輸入網址，自動去除廣告與雜訊，提取核心內容。
* **📝 雙人腳本生成:** 由 GPT-4o 扮演「理性專家 Alex」與「幽默小白 Jamie」，將枯燥文字轉化為對話。
* **🗣️ 高擬真語音 (TTS):** 整合 Microsoft Edge-TTS，提供免費且極度自然的中文/英文語音。
* **💬 視覺化預覽:** 類似通訊軟體的 Chat UI，在合成語音前可先預覽並檢查對話內容。
* **⚙️ 高度客製化:** 支援選擇不同國家語言與性別聲線。

## 🛠️ 技術架構 (Tech Stack)

本專案採用 Python 開發，強調輕量化與高效率：

| 元件 | 技術選型 | 選擇理由 |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | 極速開發 MVP，內建豐富的互動元件 (Chat UI, Audio Player)。 |
| **Crawler** | **Jina Reader API** | 專為 LLM 設計，直接將 HTML 轉為乾淨的 Markdown，節省 Token。 |
| **Brain (LLM)** | **OpenAI GPT-4o** | 強大的角色扮演 (Role-play) 能力與穩定的 JSON 格式輸出。 |
| **Voice (TTS)** | **Edge-TTS** | 免費、無需 Key，且語音品質媲美付費商業軟體。 |
| **Audio Processing** | **Pydub / FFmpeg** | 處理音訊拼接、格式轉換與靜音控制。 |

## 🚀 快速開始 (Quick Start)

### 1. 環境準備
確保你的系統已安裝 Python 3.9+ 以及 **FFmpeg** (音訊處理核心)。

### 2. 安裝依賴套件
pip install streamlit openai edge-tts pydub requests python-dotenv
=======
## 📖 專案簡介 (Introduction)

在資訊爆炸的時代，我們每天都面臨「閱讀焦慮」。看到感興趣的技術文章或新聞，往往因為篇幅太長而放入待讀清單，卻再也沒打開過。

**Podcast AI Studio** 是一個利用生成式 AI (Generative AI) 技術解決此痛點的工具。它能自動爬取網頁內容，利用 LLM 改寫為廣播腳本，並透過高品質語音合成技術，生成「專家 vs. 小白」的雙人對談 MP3。讓使用者用「聽」的來吸收新知。

## ✨ 核心功能 (Key Features)

* **🔗 智能爬蟲 (RAG):** 輸入網址，自動去除廣告與雜訊，提取核心內容。
* **📝 雙人腳本生成:** 由 GPT-4o 扮演「理性專家 Alex」與「幽默小白 Jamie」，將枯燥文字轉化為對話。
* **🗣️ 高擬真語音 (TTS):** 整合 Microsoft Edge-TTS，提供免費且極度自然的中文/英文語音。
* **💬 視覺化預覽:** 類似通訊軟體的 Chat UI，在合成語音前可先預覽並檢查對話內容。
* **⚙️ 高度客製化:** 支援選擇不同國家語言與性別聲線。

## 🛠️ 技術架構 (Tech Stack)

本專案採用 Python 開發，強調輕量化與高效率：

| 元件 | 技術選型 | 選擇理由 |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | 極速開發 MVP，內建豐富的互動元件 (Chat UI, Audio Player)。 |
| **Crawler** | **Jina Reader API** | 專為 LLM 設計，直接將 HTML 轉為乾淨的 Markdown，節省 Token。 |
| **Brain (LLM)** | **OpenAI GPT-4o** | 強大的角色扮演 (Role-play) 能力與穩定的 JSON 格式輸出。 |
| **Voice (TTS)** | **Edge-TTS** | 免費、無需 Key，且語音品質媲美付費商業軟體。 |
| **Audio Processing** | **Pydub / FFmpeg** | 處理音訊拼接、格式轉換與靜音控制。 |

## 🚀 快速開始 (Quick Start)

### 1. 環境準備
確保你的系統已安裝 Python 3.9+ 以及 **FFmpeg** (音訊處理核心)。

### 2. 安裝依賴套件
pip install streamlit openai edge-tts pydub requests python-dotenv
