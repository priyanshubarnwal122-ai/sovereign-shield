import streamlit as st
from ctransformers import AutoModelForCausalLM
import time
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sovereign Shield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CYBERPUNK STYLING (CSS) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
        .main { background-color: #0e1117; color: #00ff41; }
        h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #00ff41 !important; text-shadow: 0px 0px 10px rgba(0, 255, 65, 0.4); }
        .stTextArea textarea { background-color: #000000; color: #00ff41; font-family: 'JetBrains Mono', monospace; border: 1px solid #333; }
        .stButton>button { font-family: 'Orbitron', sans-serif; background-color: #002200; color: #00ff41; border: 1px solid #00ff41; transition: all 0.3s ease; text-transform: uppercase; }
        .stButton>button:hover { background-color: #00ff41; color: #000000; box-shadow: 0px 0px 15px #00ff41; }
        section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #1a1a1a; }
        .status-badge { padding: 4px 8px; background-color: #111; border: 1px solid #00ff41; color: #00ff41; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 5px; border-radius: 2px; }
    </style>
""", unsafe_allow_html=True)


# --- 3. LOAD THE AI MODEL ---
@st.cache_resource
def load_model():
    try:
        model = AutoModelForCausalLM.from_pretrained(
            "model.gguf",
            model_type="llama",
            context_length=2048
        )
        return model
    except Exception:
        return None

llm = load_model()


# --- 4. SMART REDACTION LOGIC (Updated with Checkboxes) ---
def rule_based_redact(text, mode, f_names, f_phones, f_aadhaar, f_locs):
    if not text: return text

    # -- MILITARY WIPE (Overrules everything) --
    if mode == "Military Grade (Wipe)":
        return re.sub(r"\d", "X", text)

    # -- STANDARD / GHOST LOGIC (Respects Checkboxes) --
    
    # 1. AADHAAR & PAN
    if f_aadhaar:
        text = re.sub(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[REDACTED_AADHAAR]", text)
        text = re.sub(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", "[REDACTED_PAN]", text)

    # 2. PHONES & ACCOUNTS
    if f_phones:
        text = re.sub(r"\b[6-9]\d{9}\b", "[REDACTED_PHONE]", text)
        text = re.sub(r"\b\d{9,18}\b", "[REDACTED_ACCOUNT]", text)
        text = re.sub(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", "[REDACTED_EMAIL]", text)

    # 3. LOCATIONS / DATES (Basic regex for dates)
    if f_locs:
        text = re.sub(r"\b\d{6}\b", "[REDACTED_PIN]", text) # 6 digit pin code
        # Dates
        text = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "[REDACTED_DATE]", text)

    # -- GHOST MODE REPLACEMENT (If selected) --
    if "Ghost" in mode:
        text = text.replace("[REDACTED_PHONE]", "9988776655")
        text = text.replace("[REDACTED_AADHAAR]", "5485-5000-8000")
        text = text.replace("[REDACTED_PAN]", "ABCDE1234F")
        text = text.replace("[REDACTED_EMAIL]", "ghost_user@secure.com")
        text = text.replace("[REDACTED_ACCOUNT]", "000000000000")
        text = text.replace("[REDACTED_PIN]", "110001")

    return text

# --- 5. DYNAMIC LLM PROMPT (For Names & Context) ---
def build_system_prompt(mode, f_names):
    task = "REPLACE detected names with realistic FAKE Indian names (e.g., Amit, Priya)" if "Ghost" in mode else "REPLACE names with [REDACTED_NAME]"
    
    if not f_names:
        return None # Don't use AI if names are unchecked
        
    return f"""<|system|>
You are a PII redaction engine.
Task: {task}.
Rules:
- Only target PERSON NAMES.
- Keep the rest of the text exactly as provided.
- Do NOT output 'Input:' or 'Output:'.
</s>
<|user|>
Process this text:
"""


# --- 6. SIDEBAR DASHBOARD (Updated) ---
with st.sidebar:
    st.title("🎛️ CONFIGURATION")
    
    st.markdown("### 🔒 MODE SELECTION")
    mode = st.radio("Operation Mode:", ["Standard Redaction", "Ghost Mode (Synthetic)", "Military Grade (Wipe)"])
    
    st.markdown("---")
    st.markdown("### ✅ SELECT PII TO TARGET")
    # THE TICKPOINTS (Granular Control)
    filter_names = st.checkbox("👤 Indian Names", value=True)
    filter_phones = st.checkbox("📞 Phone / Email", value=True)
    filter_aadhaar = st.checkbox("🆔 Aadhaar / PAN", value=True)
    filter_locs = st.checkbox("📍 Dates / Pin Codes", value=False)
    
    st.markdown("---")
    st.caption("v2.0 | Sovereign AI | Offline")

# --- 7. MAIN INTERFACE ---
st.title("🛡️ SOVEREIGN SHIELD AI")
st.markdown(f"**CURRENT MODE: {mode.upper()}**")

if not llm:
    st.error("⚠️ CRITICAL ERROR: 'model.gguf' not found.")
    st.stop()

# Initialize session state so the box exists on load
if 'result' not in st.session_state:
    st.session_state['result'] = ""
if 'speed' not in st.session_state:
    st.session_state['speed'] = 0.00
if 'chars' not in st.session_state:
    st.session_state['chars'] = 0

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 INCOMING DATA STREAM")
    user_text = st.text_area("Paste Data:", height=350, placeholder="User: Rahul Sharma\nPhone: 9876543210")

    if st.button("🛡️ EXECUTE PROCESS", use_container_width=True):
        if not user_text:
            st.warning("⚠️ INPUT BUFFER EMPTY")
        else:
            with st.spinner("🔄 NEURAL PROCESSING..."):
                start_time = time.time()
                
                # A. Run Regex Rule-Based (Fast) - Respects checkboxes
                processed_text = rule_based_redact(user_text, mode, filter_names, filter_phones, filter_aadhaar, filter_locs)
                
                # B. Run LLM (Smart) - Only if 'Names' is ticked
                final_output = processed_text
                if filter_names:
                    # Only call the heavy AI model if we really need to replace names intelligently
                    try:
                        prompt_sys = build_system_prompt(mode, filter_names)
                        if prompt_sys:
                            full_prompt = f"{prompt_sys}\n{processed_text}\n</s>\n<|assistant|>"
                            response = llm(full_prompt)
                            # Cleanup Output
                            final_output = response.replace("Input:", "").replace("Output:", "").replace("```", "").strip()
                    except Exception as e:
                        # Fallback to regex result if AI fails
                        pass
                
                # Save results to session state
                st.session_state['result'] = final_output
                st.session_state['speed'] = round(time.time() - start_time, 2)
                st.session_state['chars'] = len(user_text)
                
                # Rerun to update the UI instantly
                st.rerun()

with col2:
    st.subheader("📤 SECURE OUTPUT STREAM")
    # This box is now OUTSIDE the 'if' block, so it is always visible
    st.text_area("Redacted Data:", value=st.session_state['result'], height=350)
    
    # Metrics appear below
    m1, m2, m3 = st.columns(3)
    m1.metric("Latency", f"{st.session_state['speed']}s")
    m2.metric("Volume", f"{st.session_state['chars']} chars")
    
    if st.session_state['result']:
        m3.metric("Security", "Active ✅")
        st.download_button("💾 DOWNLOAD LOG", st.session_state['result'], "log.txt", use_container_width=True)
    else:
        m3.metric("Security", "Standby ⚠️")
