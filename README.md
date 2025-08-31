# CSV AI Dashboard 🚀

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

**CSV AI Dashboard** is an AI-powered Business Intelligence (BI) web application that allows users to upload CSV files, explore datasets, generate insights, visualize trends, and perform AI-assisted queries with natural language.  

---

## 🌟 Features

- Upload CSV files and explore data instantly  
- View dataset statistics: shape, column types, missing values  
- AI-powered natural language queries on your data  
- Generate dynamic visualizations: bar charts, line charts, histograms  
- Download processed or filtered datasets  
- Modular design, easy to extend and maintain  

---

## 🎨 Demo

> Screenshot / GIF showing the dashboard interface:

![Dashboard Screenshot](screenshots/dashboard.png)  
*Example: Upload CSV, ask AI queries, view visualizations.*

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **AI/ML:** OpenAI API, Pandas, Numpy  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap/Tailwind  
- **Deployment:** Docker, Docker Compose  
- **Version Control:** Git, GitHub  

---

##⚡ Installation

**Clone the repository**

git clone https://github.com/<your-username>/CSV_AI_Dashboard.git
cd CSV_AI_Dashboard
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Configure environment variables

Create a .env file in the project root:

env
Copy code
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
Important: .env is ignored in .gitignore to protect your secrets.

Run the application

bash
Copy code
python app.py
Open the dashboard

Go to http://localhost:5000 in your browser.




💡 Usage
Open the dashboard in your browser.

Upload a CSV file.

Explore dataset: check column types, missing values, and summary statistics.

Ask AI questions in natural language, such as:

"Show top 5 products by sales"

"Generate a line chart for monthly revenue"

Download filtered or analyzed datasets if needed.

🤝 Contributing
We welcome contributions!

Fork the repository

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -m "Add feature"

Push to branch: git push origin feature-name

Open a Pull Request



🙌 Acknowledgements
Built with ❤️ using Flask, Python, and OpenAI API

Thanks to all open-source contributors for libraries like Pandas, Numpy, and Bootstrap

Inspired by modern BI dashboards and AI-powered tools
