
# 🧠 Word Embedding Visualizer

A simple Streamlit app to explore and visualize word embeddings using Sentence Transformers and PCA.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install streamlit sentence-transformers scikit-learn plotly numpy
```

### 2. Run the App
```bash
streamlit run word_embedding.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## ✨ Features

- Add words (e.g., `run`, `running`, `walk`, `king`, `queen`)
- View:
  - Single word → Bar chart of embedding dimensions
  - 2 words → 2D PCA scatter plot
  - 3+ words → 3D PCA scatter plot
- Clear all with one click

---

## 🔍 Explore Relationships Like

- Synonyms: `happy`, `joyful`, `glad`
- Analogies: `king` - `man` + `woman` ≈ `queen`
- Contexts: `bank` (river vs. financial)
- Antonyms: `hot`, `cold`

---

## 📁 File

- `word_embedding.py`: Main app file

---

## 🧑‍💻 Author

Built with ❤️ by Junaid
