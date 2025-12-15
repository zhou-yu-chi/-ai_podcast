import streamlit as st
import openai
import os
import requests
import json
import asyncio
import edge_tts
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

# --- 頁面設定 ---
st.set_page_config(
    page_title="Podcast AI Studio",
    page_icon="🎙️",
    layout="wide"  # 改為寬版面，視覺更開闊
)

# --- CSS 優化 
st.markdown("""
<style>
    .stChatInput {position: fixed; bottom: 30px;}
    .main-header {font-size: 2.5rem; color: #FF4B4B; font-weight: 700;}
    .sub-header {font-size: 1.2rem; color: #555;}
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# --- 初始化 Session State
if 'script_data' not in st.session_state:
    st.session_state.script_data = None
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None

# --- 側邊欄：設定區 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2628/2628834.png", width=100)
    st.title("⚙️ 工作室設定")
    
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if openai_api_key:
        openai.api_key = openai_api_key

    st.markdown("---")
    st.subheader("🗣️ 聲音選角")
    
    # 讓使用者選擇聲音
    voice_options = {
        "台灣男聲 (Yunxi)": "zh-TW-YunxiNeural",
        "台灣女聲 (HsiaoChen)": "zh-TW-HsiaoChenNeural",
        "美國男聲 (Guy)": "en-US-GuyNeural",
        "美國女聲 (Aria)": "en-US-AriaNeural"
    }
    
    alex_voice_name = st.selectbox("主持人 Alex (專家)", options=list(voice_options.keys()), index=0)
    jamie_voice_name = st.selectbox("來賓 Jamie (小白)", options=list(voice_options.keys()), index=1)
    
    alex_voice = voice_options[alex_voice_name]
    jamie_voice = voice_options[jamie_voice_name]

# --- 核心功能
def get_web_content(url):
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url)
        return response.text
    except Exception as e:
        return None

def generate_script(text):
    system_prompt = """
    你是一位專業的 Podcast 腳本作家。請根據提供的文章內容，寫出一段對話腳本。
    
    角色：
    1. Alex: 專家，理性沈穩。
    2. Jamie: 好奇小白，幽默活潑。

    格式規定：
    務必回傳 JSON 物件，包含 "dialogue" 列表。
    範例：{"dialogue": [{"speaker": "Alex", "text": "..."}, {"speaker": "Jamie", "text": "..."}]}
    """
    try:
        client = openai.Client(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"文章內容：\n{text[:10000]}"} 
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"LLM Error: {e}")
        return None

async def text_to_speech_edge(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def process_audio(script_json, v_alex, v_jamie):
    combined = AudioSegment.empty()
    
    # 處理 JSON 格式容錯
    if isinstance(script_json, dict) and "dialogue" in script_json:
        data = script_json["dialogue"]
    elif isinstance(script_json, list):
        data = script_json
    else:
        # 單一物件容錯
        data = [script_json]

    total = len(data)
    my_bar = st.progress(0)
    temp_files = []

    for i, line in enumerate(data):
        speaker = line.get("speaker", "Alex")
        text = line.get("text", "")
        
        if not text: continue
        
        # 根據側邊欄選擇的聲音
        voice = v_alex if speaker == "Alex" else v_jamie
        
        with NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_files.append(f.name)
            
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(text_to_speech_edge(text, voice, temp_files[-1]))
            loop.close()
            
            seg = AudioSegment.from_file(temp_files[-1])
            combined += seg + AudioSegment.silent(duration=300)
        except:
            pass
        
        my_bar.progress((i + 1) / total)

    for f in temp_files:
        try: os.remove(f)
        except: pass
        
    return combined

# --- 主介面 Layout ---

st.markdown('<p class="main-header">🎙️ AI Podcast Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">將任何文章轉換為生動的雙人對談</p>', unsafe_allow_html=True)

# 步驟 1: 輸入與腳本生成
col1, col2 = st.columns([2, 1])

with col1:
    url_input = st.text_input("🔗 貼上文章連結", placeholder="https://...")

with col2:
    st.write("") # Spacer
    st.write("") 
    generate_btn = st.button("✨ 第一步：生成腳本")

if generate_btn and url_input and openai_api_key:
    with st.spinner("正在閱讀文章並撰寫劇本..."):
        content = get_web_content(url_input)
        if content:
            script = generate_script(content)
            st.session_state.script_data = script
            st.session_state.audio_file = None # 重置舊音檔
        else:
            st.error("無法讀取文章")

# 步驟 2: 腳本預覽與音訊合成 (使用 Chat UI)
if st.session_state.script_data:
    st.divider()
    st.subheader("📝 腳本預覽")
    
    # 使用 Chat Message UI 呈現對話
    dialogue = []
    # 處理各種 JSON 可能的結構
    raw_script = st.session_state.script_data
    if isinstance(raw_script, dict) and "dialogue" in raw_script:
        dialogue = raw_script["dialogue"]
    elif isinstance(raw_script, list):
        dialogue = raw_script
    else:
        dialogue = [raw_script]

    # 迴圈顯示對話
    for line in dialogue:
        speaker = line.get("speaker", "Alex")
        text = line.get("text", "")
        
        if speaker == "Alex":
            with st.chat_message("user", avatar="👨‍🏫"): # 專家頭像
                st.write(f"**Alex:** {text}")
        else:
            with st.chat_message("assistant", avatar="🙋"): # 小白頭像
                st.write(f"**Jamie:** {text}")

    st.divider()
    
    # 步驟 3: 合成按鈕 (置中)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        start_audio_btn = st.button("🎧 第二步：確認腳本並合成語音")

    if start_audio_btn:
        with st.spinner("正在錄音室合成中 (TTS)..."):
            final_audio = process_audio(st.session_state.script_data, alex_voice, jamie_voice)
            
            # 存到 session state 避免重新整理後不見
            out_file = "podcast_final.mp3"
            final_audio.export(out_file, format="mp3")
            st.session_state.audio_file = out_file
            st.rerun() # 重新整理頁面以顯示播放器

# 顯示播放器與下載
if st.session_state.audio_file:
    st.success("🎉 Podcast 製作完成！")
    st.audio(st.session_state.audio_file)
    
    with open(st.session_state.audio_file, "rb") as f:
        st.download_button("📥 下載 MP3", f, file_name="podcast.mp3")