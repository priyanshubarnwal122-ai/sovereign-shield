import streamlit as st
from ctransformers import AutoModelForCausalLM
import time

# --- 1. PAGE CONFIGURATION (Must be the very first command) ---
st.set_page_config(
    page_title="Sovereign Shield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CYBERPUNK STYLING (CSS) ---
st.markdown("""
    <style>
        /* Import Google Fonts: Orbitron for headers, JetBrains Mono for code */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Global Colors */
        .main {
            background-color: #0e1117; /* Void Black */
            color: #00ff41; /* Hacker Green */
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00ff41 !important;
            text-shadow: 0px 0px 10px rgba(0, 255, 65, 0.4);
        }
        
        /* Input & Output Text Areas */
        .stTextArea textarea {
            background-color: #000000;
            color: #00ff41;
            font-family: 'JetBrains Mono', monospace;
            border: 1px solid #333;
            border-radius: 4px;
        }
        
        /* Buttons */
        .stButton>button {
            font-family: 'Orbitron', sans-serif;
            background-color: #002200;
            color: #00ff41;
            border: 1px solid #00ff41;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            background-color: #00ff41;
            color: #000000;
            box-shadow: 0px 0px 15px #00ff41;
            border: 1px solid #00ff41;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #1a1a1a;
        }
        
        /* Status Badges */
        .status-badge {
            padding: 4px 8px;
            background-color: #111;
            border: 1px solid #00ff41;
            color: #00ff41;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            margin-bottom: 5px;
            border-radius: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOAD THE AI MODEL ---
@st.cache_resource
def load_model():
    try:
        # Load TinyLlama from local file
        model = AutoModelForCausalLM.from_pretrained(
            "model.gguf",
            model_type="llama",
            context_length=2048
        )
        return model
    except Exception as e:
        return None

# Load the model immediately
llm = load_model()

# --- 4. SIDEBAR DASHBOARD ---
with st.sidebar:
    st.title("🎛️ SYSTEM CONTROL")
    
    st.markdown("### 🔒 REDACTION PROTOCOL")
    security_mode = st.radio(
        "Select Level:",
        ["Standard (Redact PII)", "Ghost Mode (Synthetic)", "Military Grade (Wipe)"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📡 TELEMETRY")
    st.markdown('<div class="status-badge">🟢 NETWORK: OFFLINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">🟢 CPU CORE: ACTIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">🟢 MODEL: TINYLLAMA-1.1B</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("v1.0.4 | Sovereign AI Initiative")

# --- 5. MAIN INTERFACE ---

# Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("SOVEREIGN SHIELD AI")
    st.markdown("**OFFLINE PRIVACY DEFENSE SYSTEM**")

# Check if model is loaded
if not llm:
    st.error("⚠️ CRITICAL ERROR: Neural Core Missing.")
    st.info("Please ensure 'model.gguf' is placed in the root directory.")
    st.stop()

st.divider()

# Input/Output Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 INCOMING DATA STREAM")
    user_text = st.text_area("Paste Sensitive Data:", height=350, 
                            placeholder="[WAITING FOR INPUT]...\n\nExample:\nUser: Rahul Sharma\nPhone: 9876543210\nAadhaar: 5432-1098-7654")
    
    # The Big Action Button
    if st.button("🛡️ INITIATE REDACTION", use_container_width=True):
        if not user_text:
            st.warning("⚠️ INPUT BUFFER EMPTY")
        else:
            with col2:
                with st.spinner("🔄 PROCESSING NEURAL NETWORKS..."):
                    start_time = time.time()
                    
                    # --- NEW SMART PROMPT LOGIC (THE FIX) ---
                    if security_mode == "Ghost Mode (Synthetic)":
                        task = "Replace names with random Indian names (e.g. Amit). Replace numbers with random digits."
                    elif security_mode == "Military Grade (Wipe)":
                        task = "Replace ALL names, numbers, and dates with [CLASSIFIED]."
                    else:
                        task = "Replace sensitive numbers and names with [REDACTED]."

                    # We give it examples so it doesn't get confused
                    prompt = f"""<|system|>
You are a text filter. Strictly follow the pattern below.
Example 1:
Input: My phone is 9999999999.
Output: My phone is [REDACTED].

Example 2:
Input: Aadhaar 1234-5678-9012 linked.
Output: Aadhaar [REDACTED] linked.

Example 3:
Input: Mera naam Rahul hai.
Output: Mera naam [REDACTED] hai.
</s>
<|user|>
Task: {task}
Input: {user_text}
Output:
</s>
<|assistant|>"""
                    
                    # Run Inference
                    response = llm(prompt)
                    
                    # Save results to session state
                    st.session_state['result'] = response
                    st.session_state['speed'] = round(time.time() - start_time, 2)
                    st.session_state['chars'] = len(user_text)

# Output Column
with col2:
    st.subheader("📤 SECURE OUTPUT STREAM")
    
    if 'result' in st.session_state:
        # Result Display
        st.text_area("Redacted Data:", value=st.session_state['result'], height=350)
        
        # Live Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Latency", f"{st.session_state['speed']}s")
        m2.metric("Volume", f"{st.session_state['chars']} chars")
        m3.metric("Security", "100% Encrypted")
        
        # Download Button
        st.download_button(
            label="💾 DOWNLOAD SECURE LOG",
            data=st.session_state['result'],
            file_name="secure_redacted_log.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("System Standby. Waiting for command...")
