# 📊 CSV AI Dashboard  
### *AI-Powered Data Exploration & Insights Platform*

> Turn raw CSV files into meaningful insights using **AI + interactive analytics**.

---

## ✨ Overview

**CSV AI Dashboard** is an intelligent Business Intelligence (BI) web application that allows users to upload CSV files, explore datasets visually, and ask **natural language questions** to extract insights — without writing a single line of SQL or code.

This project bridges the gap between **traditional EDA** and **AI-driven analytics**, making data exploration accessible to everyone.

---

## 🚀 Key Features

✅ Upload & preview CSV files  
✅ Automatic dataset summary (shape, columns, data types)  
✅ Missing value & basic statistical analysis  
✅ Natural language querying using AI  
✅ Interactive data visualizations  
✅ Download processed / filtered data  
✅ Clean, modular, and extensible backend  

---

## 🧠 Example Queries

- *“Show top 5 products by revenue”*  
- *“Plot monthly sales trend”*  
- *“Which column has the most missing values?”*  
- *“Give a short summary of this dataset”*

---

## 🧰 Tech Stack

### 🔹 Backend
- **Python**
- **Flask**

### 🔹 Data Processing
- **Pandas**
- **NumPy**

### 🔹 AI Layer
- **OpenAI API** (LLM-based reasoning over tabular data)

### 🔹 Frontend
- **HTML**
- **CSS**
- **JavaScript**
- **Bootstrap / Tailwind (optional extension)**

### 🔹 DevOps & Tools
- **Docker**
- **Git & GitHub**

---

## 📁 Project Structure

```
CSV_AI_DASHBOARD_
│
├── app.py              # Main Flask application
├── helper.py           # Data processing & AI helper logic
├── requirements.txt    # Project dependencies
├── templates/          # HTML templates
├── static/             # CSS, JS, assets
├── uploads/            # Uploaded CSV files
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ishvit23/CSV_AI_DASHBOARD_.git
cd CSV_AI_DASHBOARD_
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
```

> ⚠️ Never commit `.env` files to GitHub.

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser at:

```
http://localhost:5000
```

---

## 🔄 How the System Works

1️⃣ User uploads a CSV file  
2️⃣ Data is loaded and processed using Pandas  
3️⃣ Automated EDA is generated  
4️⃣ User asks a question in plain English  
5️⃣ AI interprets the query with dataset context  
6️⃣ Insights are returned as text or visualizations  

---

## 🧩 Future Enhancements

- Excel & JSON file support  
- Advanced EDA reports  
- SQL-style querying  
- Authentication & user history  
- Cloud deployment (AWS / Render / Heroku)  
- Export charts as images  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a new branch  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes  
4. Push and open a Pull Request  

---

## 📄 License

No license specified yet.  
You may add **MIT** or **Apache 2.0** for open-source usage.

---

## 👤 Author

**Ishvit Khajuria**  
AI • Data • Full-Stack • Machine Learning  

---

⭐ *If you found this project useful, consider giving it a star!*
