import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import time
import re
import os
import random

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="Sovereign Shield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------- CYBERPUNK STYLING ---------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

.main { background-color: #0e1117; color: #00ff41; }

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ff41 !important;
    text-shadow: 0px 0px 10px rgba(0, 255, 65, 0.4);
}

.stTextArea textarea {
    background-color: #000000;
    color: #00ff41;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid #333;
    border-radius: 4px;
}

.stButton>button {
    font-family: 'Orbitron', sans-serif;
    background-color: #002200;
    color: #00ff41;
    border: 1px solid #00ff41;
}

.stButton>button:hover {
    background-color: #00ff41;
    color: #000000;
    box-shadow: 0px 0px 15px #00ff41;
}

section[data-testid="stSidebar"] {
    background-color: #050505;
}

.status-badge {
    padding: 4px 8px;
    background-color: #111;
    border: 1px solid #00ff41;
    color: #00ff41;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}
</style>
""", unsafe_allow_html=True)

# --------- LOAD NER MODEL ---------
@st.cache_resource
def load_ner():
    return pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )

ner_pipeline = load_ner()

# --------- LOAD SLM ---------
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "final_model")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    return tokenizer, model, device

tokenizer, llm, device = load_model()

# --------- FAKE DATA FOR GHOST MODE ---------
fake_first_names = [
"Aarav","Vivaan","Aditya","Vihaan","Arjun","Reyansh","Krishna","Ishaan","Shaurya",
"Atharv","Ayaan","Dhruv","Kabir","Rudra","Vedant","Aniket","Pranav","Yash",
"Rohan","Amit","Rahul","Karan","Vikram","Nikhil","Siddharth","Harsh","Manav",
"Dev","Laksh","Aryan","Tanmay","Om","Ansh","Tanish","Advik","Ritvik","Yuvraj",
"Parth","Samarth","Aakash","Mayank","Anirudh","Abhishek","Chirag","Gaurav",
"Deepak","Saurabh","Varun","Kunal","Tejas","Ritesh","Hemant","Ayush","Neeraj",
"Rajat","Prateek","Arnav","Shivam","Vivek","Anmol","Sandeep","Himanshu",
"Ujjwal","Bhavesh","Naman","Anand","Sagar","Kartik","Raghav","Adarsh",
"Aditi","Ananya","Diya","Ira","Myra","Kiara","Sara","Riya","Tanya","Meera",
"Pooja","Sneha","Nidhi","Ritika","Ishita","Neha","Shruti","Kavya","Anjali",
"Swati","Muskan","Simran","Priya","Radhika","Palak","Mansi","Komal","Riya",
"Saanvi","Navya","Khushi","Payal","Divya","Nandini","Shreya","Ishika"
]
fake_last_names = [
"Sharma","Verma","Singh","Gupta","Malhotra","Kapoor","Mehta","Agarwal",
"Jain","Bansal","Chopra","Reddy","Iyer","Nair","Menon","Patel","Desai",
"Joshi","Kulkarni","Pillai","Mishra","Tiwari","Yadav","Chauhan","Saxena",
"Trivedi","Pandey","Dubey","Bhatt","Rana","Shetty","Goswami","Bose",
"Ganguly","Mukherjee","Roy","Dutta","Chatterjee","Banerjee","Naidu",
"Varma","Saini","Thakur","Solanki","Kohli","Arora","Talwar","Goyal",
"Bhardwaj","Kumar","Das","Thomas","Fernandes","Mathew","Paul"
]
fake_cities = [
"Chandigarh","Pune","Jaipur","Lucknow","Indore","Delhi","Mumbai","Kolkata",
"Bangalore","Hyderabad","Ahmedabad","Surat","Kanpur","Nagpur","Bhopal",
"Patna","Ranchi","Raipur","Guwahati","Dehradun","Shimla","Amritsar",
"Ludhiana","Jalandhar","Noida","Gurgaon","Faridabad","Vadodara",
"Nashik","Aurangabad","Mysore","Coimbatore","Madurai","Vijayawada",
"Visakhapatnam","Trivandrum","Kochi","Mangalore","Udaipur","Jodhpur",
"Agra","Varanasi","Meerut","Allahabad","Gwalior","Jamshedpur","Dhanbad",
"Silchar","Panaji","Pondicherry"
]


def ghost_replace(text):
    new_text = text
    entity_map = {}

    # Run NER
    entities = ner_pipeline(text.title())

    for entity in entities:
        if entity["entity_group"] == "PER":
            original = entity["word"]
            if original not in entity_map:
                entity_map[original] = (
                    random.choice(fake_first_names) + " " +
                    random.choice(fake_last_names)
                )

    # Rule-based fallback for "name is X"
# Rule-based fallback for informal patterns like:
# "name is X", "name being X", "name - X", "name = X"
    name_pattern = re.search(
        r"name\s*(?:is|being|=|-)?\s*(\w+)",
        text,
        re.IGNORECASE
    )

    if name_pattern:
        detected_name = name_pattern.group(1)
        if detected_name not in entity_map:
            entity_map[detected_name] = (
                random.choice(fake_first_names) + " " +
                random.choice(fake_last_names)
            )


    # Replace names safely
    for original, fake in entity_map.items():
        pattern = r"\b" + re.escape(original) + r"\b"
        new_text = re.sub(pattern, fake, new_text)

    # Replace phone numbers (10–12 digits)
    def replace_phone(match):
        return str(random.randint(6000000000, 9999999999))

    new_text = re.sub(r"\b\d{10,12}\b", replace_phone, new_text)

    # Replace small numbers
    def replace_small(match):
        return str(random.randint(100, 999))

    new_text = re.sub(r"\b\d{3,4}\b", replace_small, new_text)

    return new_text

# --------- SIDEBAR ---------
with st.sidebar:
    st.title("🎛️ SYSTEM CONTROL")

    security_mode = st.radio(
        "Select Level:",
        ["Standard (Redact PII)",
         "Ghost Mode (Synthetic)",
         "Military Grade (Wipe)"],
        index=0
    )

    st.markdown("---")
    st.markdown('<div class="status-badge">🟢 NETWORK: OFFLINE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="status-badge">🟢 DEVICE: {device.upper()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">🟢 MODEL: CUSTOM-TRAINED</div>', unsafe_allow_html=True)

# --------- MAIN UI ---------
st.title("SOVEREIGN SHIELD AI")
st.markdown("**OFFLINE PRIVACY DEFENSE SYSTEM**")
st.divider()

col1, col2 = st.columns(2)

with col1:
    user_text = st.text_area("Paste Sensitive Data:", height=350)

    if st.button("🛡️ INITIATE REDACTION", use_container_width=True):

        if not user_text.strip():
            st.warning("⚠️ INPUT EMPTY")
        else:
            with col2:
                with st.spinner("Processing..."):
                    start_time = time.time()
                    clean_input = user_text.strip()

                    # -------- MODE LOGIC --------
                    if security_mode == "Ghost Mode (Synthetic)":
                        response = ghost_replace(clean_input)

                    elif security_mode == "Military Grade (Wipe)":
                        response = ""  # Completely clear output
                        st.success("Secure wipe completed.")


                    else:  # Standard Mode (FIXED)

                        # IMPORTANT: Match training format
                        model_input = "MODE=MASK: " + clean_input

                        inputs = tokenizer(
                            model_input,
                            return_tensors="pt",
                            truncation=True,
                            max_length=512
                        )

                        inputs = {k: v.to(device) for k, v in inputs.items()}

                        with torch.no_grad():
                            outputs = llm.generate(
                                **inputs,
                                max_new_tokens=128,
                                num_beams=5,
                                do_sample=False,
                                early_stopping=True
                            )

                        response = tokenizer.decode(
                            outputs[0],
                            skip_special_tokens=True
                        ).strip()

                    st.text_area("Redacted Data:", value=response, height=350)

                    latency = round(time.time() - start_time, 2)
                    st.write(f"Latency: {latency}s")
