import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def main():
    model = load_model()

    if "words" not in st.session_state:
        st.session_state.words = []

    # Sidebar content
    with st.sidebar:
        st.title("🔍 Understanding Word Embeddings")

        st.sidebar.markdown("""
### 🧠 What are Word Embeddings?

Word embeddings are numerical representations of words that capture their **meaning** and **relationships** with other words. They place words in a **vector space**, where similar words are closer to each other.

They are foundational to **LLMs** (Large Language Models) like GPT and BERT, helping them understand the **semantic** (meaning-related) connections between words.

---

### 🤖 Why are Word Embeddings Important for LLMs?

LLMs learn from billions of words and use embeddings to:
- Understand context
- Predict next words
- Perform tasks like summarization, translation, and Q&A

Embeddings help LLMs *represent meaning mathematically*.

---

### 🔍 Types of Embedding Relationships

Here are different kinds of relationships embeddings can show:

**1. Semantic Similarity**
- _"happy" ↔ "joyful"_
- _"run" ↔ "jog"_

**2. Analogies**
- _king - man + woman ≈ queen_

**3. Contextual Meaning**
- _"bank" (money) vs "bank" (river)_

**4. Co-occurrence (Distributional)**
- _"cat" ↔ "dog" ↔ "kitten"_ appear in similar contexts

**5. Prediction-based (Word2Vec)**
- _"coffee" ↔ "tea"_ (based on usage patterns)

---

### 🚀 How to Use This App

**Step 1:** Enter a word or phrase in the input box  
**Step 2:** Click **"Add Word"**  
**Step 3:** Add 1, 2, or more words  
**Step 4:** Visualize:
- 1 word → bar chart of vector
- 2 words → 2D scatter plot
- 3+ words → 3D plot

**Step 5:** Click "Clear All Words" to start fresh.

---

### 💡 Suggested Word Examples

Try these to explore various relationships:

**🧬 Semantic Similarity**
- run, running, jog, walk, sprint

**🧠 Emotions**
- happy, sad, joyful, angry

**👑 Analogies**
- king, queen, man, woman

**🧾 Contextual**
- bank, river, deposit

**📚 Object vs Action**
- food, eat, drink

**🧍‍♂️ Human Relationships**
- teacher, student, principal, school

**💬 Slang/Formality**
- cool, awesome, impressive

---

### 🎮 Tips for the 3D Plot

- **Rotate**: Click and drag the plot
- **Zoom**: Use mouse scroll or pinch (on touchpad)
- **Pan**: Hold right-click or Ctrl + drag

Hover over points to see the **exact word**.

---

Enjoy visualizing how machines understand language! 🎯
""")

    # Main app UI
    st.title("🧠 Word Embedding Visualizer")
    st.write("Visualize how close words or phrases are in vector space using BERT-like embeddings.")

    with st.form("word_input_form"):
        word = st.text_input("Enter a word or phrase:")
        submitted = st.form_submit_button("Add Word")
        if submitted:
            if word and word not in st.session_state.words:
                st.session_state.words.append(word)

    if st.button("Clear All Words"):
        st.session_state.words.clear()

    if st.session_state.words:
        vectors = model.encode(st.session_state.words)

        if len(st.session_state.words) == 1:
            st.subheader(f"🔢 Embedding Vector for: `{st.session_state.words[0]}`")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=np.arange(len(vectors[0])),
                x=vectors[0],
                orientation='h',
                name=st.session_state.words[0]
            ))
            fig.update_layout(
                xaxis_title="Value",
                yaxis_title="Dimension Index",
                height=1200,
                width=1600,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        elif len(st.session_state.words) == 2:
            pca = PCA(n_components=2)
            reduced = pca.fit_transform(vectors)
            fig = px.scatter(
                x=reduced[:, 0],
                y=reduced[:, 1],
                text=st.session_state.words,
                labels={"x": "PC1", "y": "PC2"},
                title="📉 2D Projection of Word Embeddings"
            )
            fig.update_traces(marker=dict(size=10), textposition="top center")
            st.plotly_chart(fig, use_container_width=True)

        else:
            pca = PCA(n_components=3)
            reduced = pca.fit_transform(vectors)
            fig = px.scatter_3d(
                x=reduced[:, 0],
                y=reduced[:, 1],
                z=reduced[:, 2],
                text=st.session_state.words,
                labels={"x": "PC1", "y": "PC2", "z": "PC3"},
                color=st.session_state.words,
                width=800,
                height=600,
                title="🌐 3D Projection of Word Embeddings"
            )
            fig.update_traces(marker=dict(size=6), textposition='top center')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👉 Add a word or phrase in the form above to begin.")

if __name__ == "__main__":
    main()
