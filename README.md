# 🛒 E-Commerce AI Assistant (FAQ + Product Query Bot)

A real-time, dual-mode AI assistant that answers:
- **General customer FAQs** using retrieval-based LLM answers
- **Product-specific queries** (like price, discount, rating) using natural language → SQL conversion over a product database

Built with:
- **LangChain-style RAG**
- **Groq LLM API**
- **Semantic Routing**
- **Streamlit UI**

---

## 📦 Features

- ✅ Ingest FAQ data into a vector store using `ChromaDB`
- ✅ Semantic routing between FAQ and SQL intent
- ✅ Converts natural language to SQL queries using Groq LLM
- ✅ Retrieves data from `SQLite` and converts to human-readable output
- ✅ Unified Streamlit-based chatbot UI

---

## 🧠 Tech Stack

| Component       | Technology                     |
|----------------|--------------------------------|
| LLM Backend     | [Groq](https://groq.com/) + Chat Completions |
| Embeddings      | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB       | `ChromaDB` (persistent client) |
| Semantic Routing| `semantic-router` w/ hybrid encoder |
| UI              | `Streamlit` (chat interface)   |
| Database        | `SQLite` (product table)       |
| Environment     | `.env` for secrets/config      |

---

## 📁 Project Structure

```
project-root/
├── main_streamlitUI.py          # Entry point UI
├── sql_pipeline.py              # SQL generation + execution + LLM response
├── faq_data_ings_pipeline.py    # Ingests FAQs and handles RAG logic
├── sql_faq_router.py            # Routes queries to either pipeline
├── resources/
│   └── faq_data.csv             # Raw FAQ dataset
├── db.sqlite                    # Product database (sample)
├── .env                         # Groq API key, model name
```

---

## ⚙️ Setup Instructions

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set environment variables**

Create a `.env` file in the root folder with:

```dotenv
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=your-groq-model-name  # e.g. mixtral-8x7b-32768
FAQ_COLLECTION_NAME=faq_file
```

3. **Add your data**

- `resources/faq_data.csv` should have `question`, `answer` columns
- `db.sqlite` must contain a `product` table with specified schema (see `sql_pipeline.py`)

4. **Run the Streamlit app**

```bash
streamlit run main_streamlitUI.py
```

---

## 💬 Example Queries

- **FAQ style**:
  - "What is the return policy of the products?"
  - "Do I get a discount with the HDFC credit card?"

- **Product-based (SQL)**:
  - "Show top 3 shoes in descending order of rating"
  - "Do you have formal shoes under Rs. 3000?"

The app intelligently routes the query based on intent using `semantic-router`.

---

## 🧪 Testing Locally

You can test individual pipelines by running:

```bash
python faq_data_ings_pipeline.py
python sql_pipeline.py
```

---

## 🔐 Notes

- Ensure Groq API access with appropriate usage limits.
- The embedding model can be swapped out if needed (`HuggingFaceEncoder` compatible).
- This is a prototype-level implementation; for production use:
  - Add logging, retries, and async support.
  - Use a scalable DB (e.g., Postgres) and deploy vector store remotely.
  - Secure `.env` and secrets properly.

---

## 📜 License

MIT License

---

## 🙋‍♂️ Contributing

Pull requests welcome. For major changes, please open an issue first to discuss what you’d like to change.
