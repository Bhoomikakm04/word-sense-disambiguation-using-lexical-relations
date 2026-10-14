import streamlit as st
import pandas as pd
import re
from collections import Counter
from pathlib import Path

st.set_page_config(page_title="SenseLab | NLP Assignment 5", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# High-contrast palette; styles are scoped to avoid Streamlit theme overrides.
st.markdown("""
<style>
:root { color-scheme: light; }
html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
.stApp { background: #f4f7fb; color: #172033; }
[data-testid="stHeader"] { background: rgba(244,247,251,.96); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0c1730 0%, #14284a 100%); border-right: 1px solid #263b60; }
[data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1rem 1.5rem 1rem; }
[data-testid="stSidebar"] * { color: #f3f6ff !important; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #d5def2 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { line-height: 1.65; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 0.48rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(190,210,245,0.13);
    border-radius: 11px;
    padding: 0.56rem 0.72rem;
    margin: 0.1rem 0;
    transition: background 140ms ease, border-color 140ms ease, transform 140ms ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(74,133,221,0.20);
    border-color: rgba(145,184,250,0.45);
    transform: translateX(2px);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(50,103,190,0.42), rgba(53,190,181,0.13));
    border-color: #5e9be8;
}
.sidebar-brand {
    font-size: 1.4rem; font-weight: 850; letter-spacing: -0.025em;
    color: #ffffff !important; margin: 0.1rem 0 0.5rem 0;
}
.sidebar-section-label {
    color: #8faee7 !important; font-size: 0.72rem; font-weight: 850;
    letter-spacing: 0.12em; text-transform: uppercase; margin: 0.6rem 0 0.7rem 0;
}
.hero { background: linear-gradient(120deg,#12213f 0%,#263f73 60%,#286c82 100%); padding: 30px 32px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 12px 28px rgba(19,37,72,.16); }
.hero h1 { color: #ffffff !important; font-size: 2.15rem !important; margin: 0 0 8px 0; font-weight: 800; }
.hero p { color: #edf4ff !important; margin: 0; font-size: 1rem; }
.eyebrow { color:#a8e9e2 !important; text-transform:uppercase; letter-spacing:.13em; font-weight:800; font-size:.76rem; margin-bottom:8px; }
.section-title { color:#15264a !important; font-size:1.25rem; font-weight:800; margin: 8px 0 12px 0; }
.small-muted { color:#4c5b73 !important; font-size:.9rem; }
.metric-card { background:#ffffff; border:1px solid #dce4f0; border-radius:15px; padding:17px 18px; min-height:105px; box-shadow:0 4px 12px rgba(28,47,80,.04); }
.metric-label { color:#53627a !important; font-size:.82rem; font-weight:700; margin-bottom:8px; }
.metric-value { color:#172b50 !important; font-size:1.7rem; font-weight:850; line-height:1.1; }
.panel { background:#ffffff; border:1px solid #dce4f0; border-radius:16px; padding:20px; margin: 10px 0; }
.pill { display:inline-block; background:#e0f5f1; color:#075b56 !important; padding:5px 10px; border-radius:99px; font-weight:750; font-size:.78rem; }
.stButton>button { background:#1d4ed8; color:white !important; border:0; border-radius:10px; font-weight:750; min-height:2.7rem; }
.stButton>button:hover { background:#163eaf !important; color:#ffffff !important; border:0; }
.stButton>button,
.stButton>button *,
button[kind="primary"],
button[kind="primary"] *,
[data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stButton>button,
button[kind="primary"] {
    background: #1d4ed8 !important;
}
[data-testid="stDownloadButton"] button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: 1px solid #1d4ed8 !important;
    border-radius: 10px !important;
    font-weight: 750 !important;
    min-height: 2.7rem;
}
[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span,
[data-testid="stDownloadButton"] button div {
    color: #ffffff !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #163eaf !important;
    color: #ffffff !important;
    border-color: #163eaf !important;
}
button:hover, button:focus, button:active {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stDownloadButton"] button:focus {
    background: #163eaf !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] { background:#fff !important; color:#172033 !important; border-color:#b9c7da !important; }
div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li { color:#26354c; }
h2,h3,h4 { color:#172b50 !important; }
div[data-testid="stDataFrame"] { border:1px solid #dce4f0; border-radius:12px; overflow:hidden; }
a { color:#174bc4 !important; }
hr { border-color:#dce4f0; }
</style>
""", unsafe_allow_html=True)

SENSES = {
    "bank": [
        {"sense":"financial institution", "definition":"An organization that accepts deposits and provides financial services.", "examples":["She deposited her salary at the bank.","The bank approved a home loan."], "synonyms":["depository","lender"], "hypernym":"financial institution", "related":["account","loan","deposit"]},
        {"sense":"side of a river", "definition":"The land alongside or sloping down to a river or lake.", "examples":["They sat on the bank of the river.","The children played along the muddy bank."], "synonyms":["riverside","shore"], "hypernym":"landform", "related":["river","water","shore"]},
    ],
    "bat": [
        {"sense":"flying mammal", "definition":"A nocturnal mammal with wings formed from a membrane.", "examples":["A bat flew out of the cave.","The bat hunts insects at night."], "synonyms":["chiropteran"], "hypernym":"mammal", "related":["cave","wings","nocturnal"]},
        {"sense":"sports equipment", "definition":"A club-shaped implement used to hit a ball in games such as cricket or baseball.", "examples":["He swung the bat and hit a six.","She bought a new cricket bat."], "synonyms":["club"], "hypernym":"sports equipment", "related":["cricket","ball","hit"]},
    ],
    "light": [
        {"sense":"illumination", "definition":"The natural agent that makes things visible.", "examples":["Please turn on the light.","Sunlight entered through the window."], "synonyms":["illumination","brightness"], "hypernym":"visible energy", "related":["lamp","bright","dark"]},
        {"sense":"not heavy", "definition":"Having relatively little weight; easy to lift or carry.", "examples":["This bag is light enough to carry.","We packed light for the trip."], "synonyms":["lightweight"], "hypernym":"physical property", "related":["weight","carry","heavy"]},
    ],
    "plant": [
        {"sense":"living organism", "definition":"A living organism that typically grows in soil and uses sunlight for energy.", "examples":["The plant needs water and sunlight.","A small plant grew beside the wall."], "synonyms":["flora"], "hypernym":"living thing", "related":["soil","water","leaves"]},
        {"sense":"industrial facility", "definition":"A factory or facility where products are manufactured or processed.", "examples":["The car plant hired new workers.","The plant produces electric motors."], "synonyms":["factory","facility"], "hypernym":"industrial facility", "related":["factory","production","workers"]},
    ],
    "crane": [
        {"sense":"large bird", "definition":"A tall, long-legged bird, often found in wetlands.", "examples":["A crane stood in the marsh.","The crane flew over the lake."], "synonyms":["wading bird"], "hypernym":"bird", "related":["marsh","feathers","lake"]},
        {"sense":"lifting machine", "definition":"A tall machine used to lift and move heavy objects.", "examples":["The crane lifted steel beams.","A crane was working at the construction site."], "synonyms":["hoist"], "hypernym":"machine", "related":["construction","lift","steel"]},
    ],
    "apple": [
        {"sense":"fruit", "definition":"A round edible fruit produced by an apple tree.", "examples":["She ate an apple after lunch.","The apple was crisp and sweet."], "synonyms":["pome"], "hypernym":"fruit", "related":["sweet","tree","eat"]},
        {"sense":"technology company", "definition":"A company known for consumer electronics and software.", "examples":["Apple released a new phone.","He uses an Apple laptop for work."], "synonyms":["Apple Inc."], "hypernym":"company", "related":["phone","laptop","software"]},
    ],
}

SAMPLES = [
    ("The bank approved my loan after checking my account.", "bank", "financial institution"),
    ("We had a picnic on the bank beside the river.", "bank", "side of a river"),
    ("A bat flew silently out of the cave at dusk.", "bat", "flying mammal"),
    ("The batter swung the bat and hit the ball.", "bat", "sports equipment"),
    ("Please switch on the light because this room is dark.", "light", "illumination"),
    ("This suitcase is light, so I can carry it upstairs.", "light", "not heavy"),
    ("The plant needs rich soil, water, and sunlight.", "plant", "living organism"),
    ("The plant manufactures engines for electric vehicles.", "plant", "industrial facility"),
    ("A crane searched for fish in the wetland.", "crane", "large bird"),
    ("The crane lifted a steel beam at the building site.", "crane", "lifting machine"),
    ("She ate a sweet apple after lunch.", "apple", "fruit"),
    ("Apple announced a new laptop with updated software.", "apple", "technology company"),
]
STOPWORDS = set("a an the is are was were be been being to of for and or in on at by with after my your this that it she he we they i can so from into beside out".split())

def tokens(text):
    return re.findall(r"[a-z]+", text.lower())

def score_sense(sentence, target, sense):
    context = set(tokens(sentence)) - STOPWORDS - {target}
    cues = set(sense["related"] + tokens(sense["definition"]) + tokens(sense["sense"]))
    overlap = sorted(context & cues)
    return len(overlap), overlap

def disambiguate(sentence, target):
    key = target.lower().strip()
    if key not in SENSES:
        return None, []
    scored = []
    for s in SENSES[key]:
        score, overlap = score_sense(sentence, key, s)
        scored.append((score, s, overlap))
    scored.sort(key=lambda x: x[0], reverse=True)
    # Tie-break with the best overlap from sense-specific related words.
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        context = set(tokens(sentence)) - STOPWORDS
        for i, item in enumerate(scored):
            related_hits = len(context & set(item[1]["related"]))
            scored[i] = (item[0] + related_hits * 0.01, item[1], item[2])
        scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1], scored

def metric(label, value, sub):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="small-muted">{sub}</div></div>', unsafe_allow_html=True)

if "annotations" not in st.session_state:
    st.session_state.annotations = []

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🧠 SenseLab</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">Workspace</div>', unsafe_allow_html=True)
    page = st.radio("WORKSPACE", ["Overview", "WSD Lab", "Sense Inventory", "Lexical Relations", "Evaluation", "Analysis Report"], index=0, label_visibility="collapsed")

if page == "Overview":
    st.markdown('<div class="hero"><div class="eyebrow">NLP LAB · ASSIGNMENT 05</div><h1>Word Sense Disambiguation</h1><p>Give ambiguous words the right meaning by reading the context around them.</p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("Ambiguous words", len(SENSES), "curated sense pairs")
    with c2: metric("Sample sentences", len(SAMPLES), "synthetic labelled examples")
    with c3: metric("Sense candidates", sum(len(x) for x in SENSES.values()), "two senses per target")
    with c4: metric("Annotations saved", len(st.session_state.annotations), "this session")
    st.markdown('<div class="panel"><div class="section-title">What this website demonstrates</div>', unsafe_allow_html=True)
    a,b = st.columns(2)
    with a:
        st.markdown("**01 · Identify ambiguity**")
        st.write("Explore words such as *bank*, *bat*, *light*, *plant*, *crane*, and *apple*, each with two distinct meanings.")
        st.markdown("**02 · Run a WSD algorithm**")
        st.write("A transparent Lesk-inspired method compares sentence context with each sense's definition and related-word cues.")
        st.markdown("**03 · Explore lexical relations**")
        st.write("Inspect synonyms, broader categories (hypernyms), and associated context words.")
    with b:
        st.markdown("**04 · Inspect evidence**")
        st.write("See overlap scores and matching words, not just a black-box prediction.")
        st.markdown("**05 · Annotate examples**")
        st.write("Save predictions with the reference sense and compare them in the Evaluation workspace.")
        st.markdown("**06 · Export deliverables**")
        st.write("Download a sense inventory, annotated results, and a short analysis report.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("Teaching note: this is a self-contained demonstration using an artificial mini-lexicon. It is inspired by the Lesk algorithm; it does not require downloading the full NLTK WordNet corpus.")
    st.markdown("### Try a sample")
    sample_idx = st.selectbox("Choose an example", range(len(SAMPLES)), format_func=lambda i: SAMPLES[i][0])
    if st.button("Open this example in the WSD Lab"):
        st.session_state["preset_sentence"] = SAMPLES[sample_idx][0]
        st.session_state["preset_target"] = SAMPLES[sample_idx][1]
        st.session_state["jump_lab"] = True
        st.rerun()

elif page == "WSD Lab":
    st.markdown('<div class="hero"><div class="eyebrow">INTERACTIVE WORKSPACE</div><h1>WSD Lab</h1><p>Enter a sentence, choose the ambiguous word, and inspect the sense evidence.</p></div>', unsafe_allow_html=True)
    sentence_default = st.session_state.pop("preset_sentence", "The bank approved my loan after checking my account.")
    target_default = st.session_state.pop("preset_target", "bank")
    sentence = st.text_area("Sentence", value=sentence_default, height=95, help="Use a sentence containing one of the supported ambiguous words.")
    target = st.selectbox("Ambiguous target word", list(SENSES.keys()), index=list(SENSES.keys()).index(target_default) if target_default in SENSES else 0)
    run = st.button("Disambiguate word", type="primary")
    if run:
        pred, scored = disambiguate(sentence, target)
        if target not in tokens(sentence):
            st.warning(f'The target word "{target}" was not found in the sentence. The algorithm will still show candidate senses, but the result may not be meaningful.')
        if pred:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("### Predicted sense")
            st.markdown(f'<span class="pill">{pred["sense"]}</span>', unsafe_allow_html=True)
            st.write(pred["definition"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("### Candidate comparison")
            rows = []
            for score, sense, overlap in scored:
                rows.append({"Candidate sense":sense["sense"], "Overlap score":round(score,2), "Matched context words":", ".join(overlap) if overlap else "No direct overlap", "Definition":sense["definition"]})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption("Scoring: number of shared content words between the sentence context and sense cues (definition, sense label, and related words). A small related-word bonus breaks ties.")
            gold = st.selectbox("Reference / expected sense (for evaluation)", [x["sense"] for x in SENSES[target]], key="gold_sense")
            if st.button("Save annotation"):
                st.session_state.annotations.append({"sentence":sentence, "target":target, "predicted_sense":pred["sense"], "reference_sense":gold, "correct":pred["sense"] == gold})
                st.success("Annotation saved to this session.")
    st.markdown("### Labeled sample set")
    sample_df = pd.DataFrame([{"Sentence":s, "Target":t, "Reference sense":g} for s,t,g in SAMPLES])
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

elif page == "Sense Inventory":
    st.markdown('<div class="hero"><div class="eyebrow">DELIVERABLE 01</div><h1>Sense Inventory</h1><p>Candidate meanings and definitions for the ambiguous words in this mini-corpus.</p></div>', unsafe_allow_html=True)
    word = st.selectbox("Select a word", list(SENSES.keys()))
    for idx, sense in enumerate(SENSES[word], start=1):
        st.markdown(f'<div class="panel"><span class="pill">Sense {idx}</span><h3>{sense["sense"].title()}</h3><p>{sense["definition"]}</p><b>Example sentences</b><ul><li>{sense["examples"][0]}</li><li>{sense["examples"][1]}</li></ul></div>', unsafe_allow_html=True)
    inventory = []
    for w, senses in SENSES.items():
        for i,s in enumerate(senses,1):
            inventory.append({"word":w,"sense_id":f"{w}_{i}","sense_label":s["sense"],"definition":s["definition"],"synonyms":"; ".join(s["synonyms"]),"hypernym":s["hypernym"],"related_words":"; ".join(s["related"])})
    csv = pd.DataFrame(inventory).to_csv(index=False).encode("utf-8")
    st.download_button("Download sense_inventory.csv", csv, "sense_inventory.csv", "text/csv")

elif page == "Lexical Relations":
    st.markdown('<div class="hero"><div class="eyebrow">WORDNET CONCEPTS</div><h1>Lexical Relations Explorer</h1><p>Explore synonymy, hypernymy, and semantic associations for each candidate sense.</p></div>', unsafe_allow_html=True)
    word = st.selectbox("Word", list(SENSES.keys()), key="relation_word")
    senses = SENSES[word]
    selected = st.radio("Sense", [s["sense"] for s in senses], horizontal=True)
    sense = next(s for s in senses if s["sense"] == selected)
    x,y,z = st.columns(3)
    with x:
        st.markdown('<div class="panel"><div class="section-title">Synonyms</div>', unsafe_allow_html=True)
        for syn in sense["synonyms"]: st.markdown(f"- `{syn}`")
        st.markdown("</div>", unsafe_allow_html=True)
    with y:
        st.markdown('<div class="panel"><div class="section-title">Hypernym</div>', unsafe_allow_html=True)
        st.write(f"**{sense['hypernym']}**")
        st.caption("A broader category that this sense belongs to.")
        st.markdown("</div>", unsafe_allow_html=True)
    with z:
        st.markdown('<div class="panel"><div class="section-title">Related cues</div>', unsafe_allow_html=True)
        for term in sense["related"]: st.markdown(f"- {term}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Relation map")
    st.markdown(f"""
    <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;background:#fff;border:1px solid #dce4f0;border-radius:15px;padding:20px;color:#172033">
      <div style="background:#e5edff;border:1px solid #9db8f7;padding:12px 16px;border-radius:12px;color:#183c87;font-weight:800">{word} · {sense['sense']}</div>
      <div style="color:#52627a;font-weight:800">→ synonym</div>
      <div style="background:#e0f5f1;border:1px solid #9bded5;padding:12px 16px;border-radius:12px;color:#075b56">{", ".join(sense['synonyms'])}</div>
      <div style="color:#52627a;font-weight:800">→ hypernym</div>
      <div style="background:#fff0d8;border:1px solid #f1cd8c;padding:12px 16px;border-radius:12px;color:#74430a">{sense['hypernym']}</div>
    </div>""", unsafe_allow_html=True)
    st.caption("These relations are manually curated for the assignment demonstration and are WordNet-style, not a live query to the complete WordNet database.")

elif page == "Evaluation":
    st.markdown('<div class="hero"><div class="eyebrow">DELIVERABLE 02</div><h1>Evaluation & Annotation</h1><p>Compare algorithm predictions with reference labels and inspect errors.</p></div>', unsafe_allow_html=True)
    eval_rows = []
    for sentence, target, gold in SAMPLES:
        pred,_ = disambiguate(sentence,target)
        eval_rows.append({"sentence":sentence,"target":target,"reference":gold,"predicted":pred["sense"],"correct":pred["sense"] == gold})
    sample_eval = pd.DataFrame(eval_rows)
    if st.session_state.annotations:
        custom_eval = pd.DataFrame(st.session_state.annotations)
        all_eval = pd.concat([sample_eval, custom_eval.rename(columns={"reference_sense":"reference","predicted_sense":"predicted"})[["sentence","target","reference","predicted","correct"]]], ignore_index=True)
    else:
        all_eval = sample_eval
    accuracy = all_eval["correct"].mean() * 100
    c1,c2,c3 = st.columns(3)
    with c1: metric("Evaluated examples", len(all_eval), "sample + saved annotations")
    with c2: metric("Accuracy", f"{accuracy:.1f}%", "on the displayed reference labels")
    with c3: metric("Incorrect cases", int((~all_eval["correct"]).sum()), "use errors to improve cues")
    st.dataframe(all_eval, use_container_width=True, hide_index=True)
    st.download_button("Download annotated_results.csv", all_eval.to_csv(index=False).encode("utf-8"), "annotated_results.csv", "text/csv")
    st.warning("Accuracy is measured only on this small, hand-built dataset. It should not be interpreted as a benchmark result or general performance on real-world text.")
    if st.button("Clear session annotations"):
        st.session_state.annotations = []
        st.rerun()

elif page == "Analysis Report":
    st.markdown('<div class="hero"><div class="eyebrow">DELIVERABLE 03</div><h1>Short Analysis Report</h1><p>Method, observations, limitations, and possible improvements.</p></div>', unsafe_allow_html=True)
    sample_eval = []
    for sentence,target,gold in SAMPLES:
        pred,_ = disambiguate(sentence,target)
        sample_eval.append(pred["sense"] == gold)
    acc = sum(sample_eval)/len(sample_eval)*100
    st.markdown('<div class="panel"><h3>Objective</h3><p>Build a small Word Sense Disambiguation (WSD) website that identifies the intended meaning of ambiguous words by using sentence context and lexical information.</p><h3>Dataset</h3><p>A synthetic teaching dataset contains 6 target words—bank, bat, light, plant, crane, and apple—with two senses each and 12 labeled sample sentences. The mini-lexicon stores definitions, examples, synonyms, hypernyms, and related words.</p><h3>Method</h3><p>The system uses a transparent Lesk-inspired overlap algorithm. It tokenizes the input, removes common stopwords, compares context terms with each candidate sense definition and cue words, then chooses the candidate with the strongest overlap. The interface exposes scores and matching words so the prediction can be inspected.</p><h3>Observations</h3><p>The approach is easy to explain and works best when a sentence contains strong contextual cues such as “loan/account” for a financial bank or “river” for a river bank. It can fail when context is short, the vocabulary differs from the curated cues, or both candidates have similar overlap.</p><h3>Limitations</h3><p>The dataset and lexical relations are artificially created for this assignment. This is not a full WordNet integration, and the reported score is not evidence of general performance. The method does not use contextual embeddings or train a supervised classifier.</p><h3>Future improvements</h3><p>Connect the NLTK WordNet corpus, expand and validate a labeled corpus, add lemmatization and part-of-speech constraints, compare against supervised WSD, and evaluate on a held-out dataset with precision, recall, and F1-score.</p></div>', unsafe_allow_html=True)
    st.metric("Illustrative sample-set accuracy", f"{acc:.1f}%")
    st.caption("The displayed accuracy is generated from the included synthetic examples and is intended only for classroom demonstration.")
    report = f"""NLP ASSIGNMENT 5: WORD SENSE DISAMBIGUATION

Objective
Build a small WSD website that identifies the intended meaning of ambiguous words using context and lexical information.

Dataset
A synthetic teaching dataset contains 6 target words (bank, bat, light, plant, crane, apple), two senses per word, and 12 labeled sample sentences. Each sense includes a definition, examples, synonyms, a hypernym, and related cue words.

Method
A Lesk-inspired lexical-overlap algorithm tokenizes the sentence, removes common stopwords, compares context terms against each candidate sense's definition and cue words, and chooses the candidate with the highest overlap. The interface displays scores and matched terms for transparency.

Observations
The method is interpretable and works best when context contains strong clues. It may fail on short sentences, unseen vocabulary, or ties between candidate senses.

Limitations
The mini-lexicon and relations are artificially curated for this assignment; this is not a live/full WordNet implementation. Synthetic-data accuracy must not be treated as general model performance.

Future improvements
Integrate NLTK WordNet, expand and validate the labeled corpus, add lemmatization and POS constraints, compare with a supervised or transformer-based model, and evaluate on a held-out dataset using precision, recall, and F1-score.
"""
    st.download_button("Download analysis_report.txt", report, "analysis_report.txt", "text/plain")

st.markdown("---")
st.markdown('<p style="text-align:center;color:#58677e;font-size:.82rem">SenseLab · NLP Assignment 05 · Word Sense Disambiguation · Synthetic educational dataset</p>', unsafe_allow_html=True)
