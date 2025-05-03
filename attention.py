import streamlit as st
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
import networkx as nx
from pyvis.network import Network
import tempfile
import os

st.set_page_config(layout="wide")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased", output_attentions=True)
    return tokenizer, model

tokenizer, model = load_model()

if "sentence_tokens" not in st.session_state:
    st.session_state.sentence_tokens = []

st.title("🔁 Visual Attention Arrows - Intuitive BERT Demo")
st.markdown("""
This tool shows how **BERT attention** works without heatmaps!

➡️ Each word is a circle, and arrows show where that word looks (attends).

- Thicker arrows = stronger attention.
- Add words one-by-one to see how attention changes.
""")

with st.form("add_word_form"):
    new_word = st.text_input("Add a word to the sentence", "")
    submitted = st.form_submit_button("Add Word")
    if submitted and new_word.strip():
        st.session_state.sentence_tokens.append(new_word.strip())

if st.button("🔄 Reset"):
    st.session_state.sentence_tokens = []

if st.session_state.sentence_tokens:
    st.markdown("### Current Sentence:")
    sentence = " ".join(st.session_state.sentence_tokens)
    st.write(sentence)

    # Encode and run through model
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    attention = outputs.attentions[-1][0].mean(dim=0).numpy()  # Avg over heads

    # Build attention graph
    G = nx.DiGraph()
    for i, token in enumerate(tokens):
        G.add_node(i, label=token)

    threshold = 0.1  # Show only stronger attentions
    for i in range(len(tokens)):
        for j in range(len(tokens)):
            weight = attention[i][j]
            if weight > threshold:
                G.add_edge(i, j, weight=weight)

    # Visualize with PyVis
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)

    # Customize node layout (left-to-right)
    for i, node in enumerate(net.nodes):
        node["x"] = i * 150
        node["y"] = 0
        node["physics"] = False

    for edge in net.edges:
        weight = edge["value"]
        edge["width"] = weight * 5  # Make strong attention lines bolder
        edge["arrows"] = "to"

    # Save and display
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_path = tmp_file.name

    with open(tmp_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    st.components.v1.html(html_code, height=600, scrolling=True)

    os.remove(tmp_path)
else:
    st.info("Start typing words to build a sentence and see attention arrows!")
