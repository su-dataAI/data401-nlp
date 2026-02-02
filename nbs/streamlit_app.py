"""NER manual-eval Streamlit app — extracted from nbs/_Tiny_Manual_Eval_POS_NER_Notebook.ipynb

Run:
    streamlit run streamlit_app.py --server.port 8501

Features:
- Loads `data/covidhoax_OR_notomasks_hashtag.csv` (falls back to tiny demo if missing)
- Loads spaCy `en_core_web_sm` (will attempt download if absent)
- Samples tweets, shows spaCy NER, lets a human mark correctness + label + notes
- Export results to CSV and shows a crude accuracy estimate

Requirements:
- streamlit, pandas, spacy, (en_core_web_sm)

Location: repo root (so path `data/...` is preserved)
"""
from pathlib import Path
import argparse
import io
from typing import List, Dict, Optional

import pandas as pd
import spacy
import streamlit as st

# ---- Config ----
DATA_PATH_DEFAULT = Path("data/covidhoax_OR_notomasks_hashtag.csv")
ENTITY_LABELS = [
    "ORG",
    "PERSON",
    "PRODUCT",
    "MONEY",
    "CARDINAL",
    "DATE",
    "NORP",
    "GPE",
    "FAC",
    "ORDINAL",
]

# ---- Helpers ----
@st.cache_resource
def load_spacy_model(name: str = "en_core_web_sm"):
    try:
        nlp = spacy.load(name)
        return nlp
    except OSError:
        # try to download the model if missing
        from spacy.cli import download

        download(name)
        return spacy.load(name)


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path!s}")
    df = pd.read_csv(path)
    df = df.dropna(subset=["tweet_text"]).reset_index(drop=True)
    return df


def extract_entities_from_sample(sample: pd.DataFrame, nlp) -> pd.DataFrame:
    results: List[Dict] = []
    for _, row in sample.iterrows():
        doc = nlp(row["tweet_text"])
        ents = [(ent.text, ent.label_) for ent in doc.ents]
        results.append({"tweet": row["tweet_text"], "entities": ents})
    return pd.DataFrame(results)


def flatten_entities(eval_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict] = []
    for idx, r in eval_df.iterrows():
        tweet = r["tweet"]
        entities = r["entities"]
        if not entities:
            rows.append(
                {
                    "tweet_id": int(idx),
                    "tweet_text": tweet,
                    "tagged_entity": None,
                    "entity_label": None,
                }
            )
        else:
            for ent_text, ent_label in entities:
                rows.append(
                    {
                        "tweet_id": int(idx),
                        "tweet_text": tweet,
                        "tagged_entity": ent_text,
                        "entity_label": ent_label,
                    }
                )
    return pd.DataFrame(rows)


def _default_session_key(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value


def _build_results_df_from_session(n_rows: int) -> pd.DataFrame:
    """Construct results DataFrame from current st.session_state for n_rows."""
    rows: List[Dict] = []
    for i in range(n_rows):
        human_label = st.session_state.get(f"r{i}__human_label")
        rows.append(
            {
                "tweet_id": i,
                "tweet_text": st.session_state.get(f"r{i}__tweet_text"),
                "tagged_entity": st.session_state.get(f"r{i}__tagged_entity"),
                "entity_label": st.session_state.get(f"r{i}__entity_label"),
                "correct_entities? (yes/no)": "yes" if st.session_state.get(f"r{i}__evaluation") else "no",
                "your label": None if human_label == "None" else human_label,
                "notes": st.session_state.get(f"r{i}__notes"),
            }
        )
    return pd.DataFrame(rows)


# ---- Streamlit UI ----

st.set_page_config(page_title="NER manual eval", layout="wide")
st.title("NER — tiny manual evaluation (tweets)")

with st.sidebar:
    st.header("Controls")
    data_path = st.text_input("Dataset path", value=str(DATA_PATH_DEFAULT))
    sample_size = st.number_input("Sample size", min_value=1, max_value=200, value=25)
    seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42)
    show_sample = st.checkbox("Show sampled tweets", value=False)
    st.markdown("---")
    st.markdown("When finished: use **Export → Download** to save your human labels.")

DATA_PATH = Path(data_path)

# Load data (with friendly fallback)
try:
    df_full = load_data(DATA_PATH)
except FileNotFoundError as e:
    # Always fall back to the tiny demo when the dataset is missing.
    st.warning(f"{e} — dataset not found; using tiny demo tweets instead.")
    demo = [
        "Wear a mask! #COVID",
        "No way I'm wearing a mask 😷",
        "CDC guidance updated today",
        "Pfizer announces new results",
    ]
    df_full = pd.DataFrame({"tweet_text": demo})

nlp = load_spacy_model()

# Sample
sample = df_full.sample(int(sample_size), random_state=int(seed))[['tweet_text']].reset_index(drop=True)
if show_sample:
    st.subheader("Sampled tweets")
    st.dataframe(sample)

# Extract & flatten
eval_df = extract_entities_from_sample(sample, nlp)
entities_table = flatten_entities(eval_df)

st.markdown("---")
st.subheader("Entity evaluation")

if entities_table.empty:
    st.info("No entities were detected in the sampled tweets. You can increase sample size or inspect the sample.")
else:
    # initialize session_state defaults for each row
    for i, row in entities_table.reset_index(drop=True).iterrows():
        base = f"r{i}"
        _default_session_key(base + "__tweet_text", row["tweet_text"])
        _default_session_key(base + "__tagged_entity", row["tagged_entity"])
        _default_session_key(base + "__entity_label", row["entity_label"])
        _default_session_key(base + "__evaluation", None)
        # default to the literal "None" (so the dropdown shows "None" first)
        _default_session_key(base + "__human_label", row["entity_label"] if row["entity_label"] else "None")
        _default_session_key(base + "__notes", "")

    # --- show updated entities table at the top (reflects current session_state) ---
    results_df = _build_results_df_from_session(len(entities_table))
    st.subheader("Updated entities table (current)")
    st.dataframe(results_df)

    # Export (download) + metrics placed under the updated table for immediate access
    csv_buf_top = io.StringIO()
    results_df.to_csv(csv_buf_top, index=False)
    csv_bytes_top = csv_buf_top.getvalue().encode("utf-8")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.download_button("Download CSV", data=csv_bytes_top, file_name="ner_manual_eval.csv", mime="text/csv")
    with c2:
        if results_df["correct_entities? (yes/no)"].notna().any():
            flags_top = results_df["correct_entities? (yes/no)"].str.lower().eq("yes")
            st.metric("Crude accuracy (sample)", f"{flags_top.mean():.2%}")

    st.markdown("---")

    # render interactive rows
    for i, row in entities_table.reset_index(drop=True).iterrows():
        st.markdown(f"**Tweet (id={i})**")
        tweet_text = st.session_state[f"r{i}__tweet_text"]
        tagged_entity = st.session_state[f"r{i}__tagged_entity"]
        entity_label = st.session_state[f"r{i}__entity_label"]

        # Highlight only the specific tagged entity in the tweet text
        if tagged_entity and tagged_entity in tweet_text:
            tweet_text = tweet_text.replace(tagged_entity, f"<span style='color: red; font-weight: bold;'>{tagged_entity}</span>", 1)  # Color highlighting, replace only the first occurrence

        st.markdown(tweet_text, unsafe_allow_html=True)  # Allow HTML rendering
        cols = st.columns([3, 1, 1, 2])
        with cols[0]:
            st.write("**Tagged entity**: ", st.session_state[f"r{i}__tagged_entity"])
            st.write("**spaCy label**: ", st.session_state[f"r{i}__entity_label"])
        with cols[1]:
            st.session_state[f"r{i}__evaluation"] = st.checkbox("Correct?", key=f"eval_{i}")
        with cols[2]:
            # compute selectbox index robustly (0 == "None")
            _cur = st.session_state[f"r{i}__human_label"]
            if _cur in (None, "None"):
                _idx = 0
            elif _cur in ENTITY_LABELS:
                _idx = ENTITY_LABELS.index(_cur) + 1
            else:
                _idx = 0

            st.session_state[f"r{i}__human_label"] = st.selectbox(
                "Correct label",
                options=["None"] + ENTITY_LABELS,
                index=_idx,
                key=f"label_{i}",
            )
        with cols[3]:
            st.session_state[f"r{i}__notes"] = st.text_input("Notes", key=f"notes_{i}")

        st.markdown("---")

# (export/metrics moved above the interactive rows)
st.markdown("---")
st.info("Run: `streamlit run streamlit_app.py` — open http://localhost:8501 in your browser.")


# Allow running with `python streamlit_app.py` for quick debugging (shows same UI via streamlit)
if __name__ == "__main__":
    parser = argparse.ArgumentParser("NER manual eval app")
    parser.add_argument("--data-path", default=str(DATA_PATH_DEFAULT))
    parser.add_argument("--sample-size", type=int, default=25)
    args = parser.parse_args()
    # When run with `python file.py` the Streamlit UI is still the primary surface — nothing to do here.
    print("This file is intended to be run with `streamlit run streamlit_app.py`.\nRun that command to start the app.")
