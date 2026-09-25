# 🎬 CineSage — AI-Powered Movie Information Extractor

**CineSage** is an end-to-end information extraction web application that converts unstructured text paragraphs and movie discussions into strictly validated, production-ready JSON data. Built with **Streamlit**, **LangChain**, and **Groq**, it uses Pydantic schema validation to extract detailed movie attributes without hallucinations or schema drift.

---

## 📌 Features

* **Multi-Entity Extraction:** Identifies and isolates multiple distinct movies mentioned across unstructured paragraphs without merging records.
* **Strict Type Enforcement:** Leverages LangChain's `PydanticOutputParser` to enforce schema constraints across 7 attributes: `title`, `release_year`, `genre`, `director`, `cast`, `rating`, and `summary`.
* **Low-Latency Inference:** Powered by Groq's high-speed compute engine running the `openai/gpt-oss-20b` model.
* **Deterministic Fallback Logic:** Uses defensive prompt constraints to guarantee structured fallback values (`null`, `[]`, or `""`) when specific film attributes are omitted from source texts.
* **Glassmorphic UI & Instant Export:** Features a custom dark-mode interface with live JSON tree rendering and one-click `movies.json` file downloads.

---

## 🛠️ Tech Stack

* **Framework / UI:** Streamlit
* **LLM Orchestration:** LangChain Core, LangChain Groq
* **Model Inference:** Groq API (`openai/gpt-oss-20b`)
* **Data Validation:** Pydantic
* **Environment Management:** Python Dotenv

---

## 📂 Project Structure

```text
cinesage-movie-extractor/
├── app.py              # Main Streamlit application and extraction pipeline
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Files ignored by Git (.env, cache, etc.)
└── README.md           # Documentation

---

## ⚙️ Quickstart & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/isultan1111/cinesage-movie-extractor.git](https://github.com/isultan1111/cinesage-movie-extractor.git)
cd cinesage-movie-extractor
```

### 2. Create and Activate a Virtual Environment
* **Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory[cite: 2]:
```bash
touch .env
```
Add your Groq API key[cite: 1, 3]:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Run the Application
Launch the Streamlit server[cite: 3]:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to interact with the application.

---

## 🧩 Output Schema

Extracted data outputs strictly conform to the following JSON structure[cite: 3]:

```json
{
  "movies": [
    {
      "title": "The Dark Knight",
      "release_year": 2008,
      "genre": ["Action", "Crime", "Drama"],
      "director": "Christopher Nolan",
      "cast": ["Christian Bale", "Heath Ledger"],
      "rating": 9.0,
      "summary": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    }
  ]
}
```

---

## 👤 Author

* **Md Irfan**[cite: 4]
* **GitHub:** [@isultan1111](https://github.com/isultan1111)
* **LinkedIn:** [md-irfan-99bb16280](https://linkedin.com/in/md-irfan-99bb16280)
