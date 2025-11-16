# University Rankings Scraper

A web application that scrapes and aggregates university rankings from multiple sources:
- QS World University Rankings
- THE (Times Higher Education) World University Rankings
- US News Best Global Universities
- ARWU (Shanghai Ranking/软科)
- CS Rankings

## Features

- 🔍 Search universities by name
- 📊 View rankings from multiple sources
- 📈 Calculate average rankings across selected sources
- 🌐 Web interface for easy access

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

```bash
cd backend
python app.py
```

Then open `frontend/index.html` in your browser.

## Usage

1. **Search**: Enter a university name in the search box
2. **Select Rankings**: Check/uncheck ranking sources to include in average calculation
3. **View Results**: See individual rankings and calculated averages

## Tech Stack

- **Backend**: Python, Flask, BeautifulSoup, Requests
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: SQLite

## Note

Web scraping may be subject to website terms of service. This tool is for educational purposes only.
