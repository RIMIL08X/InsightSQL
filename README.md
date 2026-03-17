# InsightSQL — Natural Language Database Chatbot

InsightSQL is a **local LLM-powered database assistant** that allows users to query a PostgreSQL database using **natural language**.

Instead of writing SQL manually, users can ask questions and the system will:

* Generate SQL queries automatically
* Execute them safely on the database
* Return results along with a clear explanation

The entire system runs **locally**, enabling privacy-friendly analytics without external APIs. 🚀

---

# System Architecture

```
User (Browser)
        │
        ▼
Frontend (Next.js Application)
        │
        ▼
API Requests
        │
        ▼
FastAPI Backend
        │
        ▼
LLM Layer (Ollama Runtime)
        │
        ├── DeepSeek Coder 6.7B
        └── Mistral 7B Instruct
        │
        ▼
SQL Guard / Validation
        │
        ▼
SQLAlchemy Engine
        │
        ▼
PostgreSQL Database
```

---

# Key Features

* Natural Language → SQL conversion
* Local LLM inference using Ollama
* Secure query validation layer
* Real-time database querying
* Clean analytics interface
* Fully offline capable environment

---

# Application Interface

The following screenshots demonstrate the **InsightSQL interface executing real database queries**.

## Revenue Insight Query

![Revenue Query](Screenshots/x.png)

The interface converts a natural language business question into SQL, executes it against the database, and presents the resulting insight in a structured format.

---

## Order Payment Data

![Orders Query](Screenshots/y.png)

The application displays the generated SQL alongside the resulting dataset, allowing users to inspect database outputs directly from the interface.

---

# Technology Stack

## Frontend

* Next.js
* JavaScript / TypeScript
* Fetch API

## Backend

* FastAPI
* Python
* SQLAlchemy

## AI Layer

* Ollama Runtime
* DeepSeek Coder 6.7B
* Mistral 7B Instruct

## Database

* PostgreSQL

---

# Installation

## Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/insightsql.git
cd insightsql
```

---

# Backend Setup

Install Python dependencies:

```
pip install -r requirements.txt
```

Start the FastAPI server:

```
uvicorn main:app --reload
```

Backend server will run at:

```
http://127.0.0.1:8000
```

---

# Frontend Setup

Navigate to the frontend directory:

```
cd sql-ai-frontend
```

Install dependencies:

```
npm install
```

Start the development server:

```
npm run dev
```

Frontend will run at:

```
http://localhost:3000
```

---

# PostgreSQL Configuration ⚙️

Ensure PostgreSQL is installed and running before launching the application.

Database connection format:

```
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

Example configuration:

```
postgresql://username:password@localhost:5432/mydb
```

Before running the system verify that:

* PostgreSQL service is running
* The database exists
* Credentials are correct
* Tables are populated
* Port `5432` is accessible

Users should **update the database URL according to their local PostgreSQL configuration** before connecting.

---

# API Usage

## Connect Database

```
POST /connect
```

Used to initialize a connection between the application and a PostgreSQL database.

---

## Ask Questions

```
POST /ask
```

Accepts a natural language query and returns:

* Generated SQL
* Query results
* Explanation

---

# Security

The system includes safeguards to prevent unsafe database operations:

* Read-only query enforcement
* SQL validation layer
* Backend-restricted database access

These measures ensure the chatbot interacts with the database **safely and predictably**.

---

# Project Structure

```
NV-finals
│
├── .git/                     # Git repository metadata
├── .venv/                    # Python virtual environment
├── __pycache__/              # Python bytecode cache
│
├── cheatsheet/               # Query examples and development notes
├── sample databases/         # Sample PostgreSQL datasets for testing
│
├── sql-ai-frontend/          # Next.js frontend application
│
├── db.py                     # Database connection and query execution logic
├── llm.py                    # LLM integration (Ollama model interaction)
├── main.py                   # FastAPI backend entry point
├── prompts.py                # Prompt templates for SQL generation
├── sql_guard.py              # SQL validation and safety checks
│
├── requirements.txt          # Python dependencies
├── process_flow.odt          # System architecture documentation
│
└── README.md                 # Project documentation
```

---

# Overview

InsightSQL demonstrates how **local LLMs can be integrated with traditional databases** to create a modern analytics interface.

The project combines:

* Natural language processing
* safe SQL generation
* real-time data retrieval
* a modern full-stack architecture

to enable **intuitive exploration of structured data**. 📊
