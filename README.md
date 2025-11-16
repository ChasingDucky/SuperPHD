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

## 数据说明 / Data Information

### 当前状态 / Current Status

- ✅ **ARWU (软科)**: 可以抓取真实数据（约30所大学）/ Can scrape real data (~30 universities)
- 📊 **其他排名**: 使用高质量示例数据（50所大学）/ Others use high-quality sample data (50 universities)
- 📥 **自定义数据**: 支持CSV导入 / Supports CSV import

### 快速测试 / Quick Test

```bash
cd backend
python quick_test.py  # 测试ARWU爬虫 / Test ARWU scraper
python test_scrapers.py  # 完整诊断 / Full diagnostics
```

### 数据导入 / Data Import

```bash
cd backend
python import_data.py data/sample_rankings.csv
```

查看 `DATA_INFO.md` 了解更多信息 / See `DATA_INFO.md` for more information

## Note

Web scraping may be subject to website terms of service. This tool is for educational purposes only.
