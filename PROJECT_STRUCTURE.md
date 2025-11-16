# 项目结构 / Project Structure

```
SuperPHD/
│
├── README.md                          # 项目说明 / Project documentation
├── QUICKSTART.md                      # 快速开始指南 / Quick start guide
├── PROJECT_STRUCTURE.md               # 本文件 / This file
├── .gitignore                         # Git忽略文件 / Git ignore file
├── run.sh                            # Linux/Mac启动脚本 / Linux/Mac run script
├── run.bat                           # Windows启动脚本 / Windows run script
│
├── backend/                          # 后端目录 / Backend directory
│   ├── app.py                        # Flask应用主文件 / Flask app main file
│   ├── models.py                     # 数据库模型 / Database models
│   ├── requirements.txt              # Python依赖 / Python dependencies
│   ├── rankings.db                   # SQLite数据库（运行后生成）/ SQLite database (generated after running)
│   │
│   └── scrapers/                     # 爬虫模块目录 / Scrapers directory
│       ├── __init__.py               # 包初始化文件 / Package init file
│       ├── qs_scraper.py            # QS排名爬虫 / QS scraper
│       ├── the_scraper.py           # THE排名爬虫 / THE scraper
│       ├── usnews_scraper.py        # US News排名爬虫 / US News scraper
│       ├── arwu_scraper.py          # 软科排名爬虫 / ARWU scraper
│       └── csrankings_scraper.py    # CS Rankings爬虫 / CS Rankings scraper
│
└── frontend/                         # 前端目录 / Frontend directory
    ├── index.html                    # 主页面 / Main page
    ├── styles.css                    # 样式表 / Stylesheet
    └── script.js                     # JavaScript逻辑 / JavaScript logic
```

## 文件说明 / File Descriptions

### 后端文件 / Backend Files

#### `app.py`
Flask应用的主文件，包含：
- API路由定义 / API route definitions
- 数据库操作 / Database operations
- 爬虫调度 / Scraper scheduling
- 平均排名计算 / Average ranking calculation

主要API端点 / Main API endpoints:
- `GET /api/rankings` - 获取所有排名 / Get all rankings
- `GET /api/search?q=<query>` - 搜索大学 / Search universities
- `POST /api/average-ranking` - 计算平均排名 / Calculate average ranking
- `POST /api/update` - 更新排名数据 / Update rankings
- `GET /api/stats` - 获取统计信息 / Get statistics

#### `models.py`
数据库模型定义，包含：
- `University` 模型：存储大学信息和各个排名数据
- `Database` 类：提供数据库操作方法

字段说明 / Field descriptions:
- `name`: 大学名称 / University name
- `country`: 国家 / Country
- `qs_rank`, `qs_score`: QS排名和分数 / QS rank and score
- `the_rank`, `the_score`: THE排名和分数 / THE rank and score
- `usnews_rank`, `usnews_score`: US News排名和分数
- `arwu_rank`, `arwu_score`: 软科排名和分数 / ARWU rank and score
- `cs_rank`, `cs_score`: CS Rankings排名和分数

#### `scrapers/` 目录
包含各个排名网站的爬虫实现：

- **qs_scraper.py**:
  - 抓取QS世界大学排名
  - URL: https://www.topuniversities.com/world-university-rankings

- **the_scraper.py**:
  - 抓取THE世界大学排名
  - URL: https://www.timeshighereducation.com/world-university-rankings

- **usnews_scraper.py**:
  - 抓取US News全球最佳大学排名
  - URL: https://www.usnews.com/education/best-global-universities/rankings

- **arwu_scraper.py**:
  - 抓取软科世界大学学术排名
  - URL: https://www.shanghairanking.com/rankings/arwu

- **csrankings_scraper.py**:
  - 抓取计算机科学排名
  - URL: https://csrankings.org

每个爬虫都包含：
- `scrape()`: 主爬取方法 / Main scraping method
- `_get_sample_data()`: 示例数据（用于测试）/ Sample data (for testing)

### 前端文件 / Frontend Files

#### `index.html`
主页面，包含：
- 搜索框 / Search box
- 排名来源选择器 / Ranking source selector
- 结果显示区域 / Results display area
- 统计信息显示 / Statistics display

#### `styles.css`
样式表，定义了：
- 响应式布局 / Responsive layout
- 卡片样式 / Card styles
- 渐变背景 / Gradient background
- 动画效果 / Animation effects

#### `script.js`
前端逻辑，实现：
- API调用 / API calls
- 搜索功能 / Search functionality
- 平均排名计算 / Average ranking calculation
- 结果渲染 / Results rendering
- 错误处理 / Error handling

## 数据流 / Data Flow

```
用户界面 (Frontend)
    ↓ HTTP请求
Flask API (Backend)
    ↓ 调用
爬虫模块 (Scrapers)
    ↓ 获取数据
外部网站 (Ranking Websites)
    ↓ 返回数据
SQLite数据库 (Database)
    ↓ 查询结果
返回给用户 (Response to User)
```

## 技术栈 / Tech Stack

### 后端 / Backend
- **Python 3.7+**
- **Flask**: Web框架 / Web framework
- **SQLAlchemy**: ORM数据库操作 / ORM for database operations
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **Requests**: HTTP请求 / HTTP requests

### 前端 / Frontend
- **HTML5**: 页面结构 / Page structure
- **CSS3**: 样式和动画 / Styling and animations
- **Vanilla JavaScript**: 逻辑实现 / Logic implementation
- **Fetch API**: 异步HTTP请求 / Asynchronous HTTP requests

### 数据库 / Database
- **SQLite**: 轻量级关系数据库 / Lightweight relational database

## 扩展建议 / Extension Suggestions

1. **实时爬取**: 实现更健壮的网页爬虫，处理动态加载内容
   Real-time scraping: Implement more robust web scrapers to handle dynamically loaded content

2. **缓存机制**: 添加Redis缓存以提高性能
   Caching: Add Redis cache for better performance

3. **用户账户**: 添加用户系统，保存收藏的大学
   User accounts: Add user system to save favorite universities

4. **数据可视化**: 使用Chart.js等库添加图表
   Data visualization: Add charts using libraries like Chart.js

5. **移动应用**: 开发React Native或Flutter移动应用
   Mobile app: Develop React Native or Flutter mobile application

6. **定时任务**: 使用Celery实现定时自动更新排名
   Scheduled tasks: Use Celery for automatic ranking updates

7. **导出功能**: 支持导出为Excel或PDF
   Export feature: Support export to Excel or PDF

8. **多语言支持**: 添加更多语言界面
   Internationalization: Add more language interfaces

## 维护说明 / Maintenance Notes

### 更新爬虫 / Updating Scrapers
由于网站结构可能变化，爬虫代码可能需要定期更新。检查：
Website structures may change, scraper code may need periodic updates. Check:

1. HTML结构变化 / HTML structure changes
2. CSS类名变化 / CSS class name changes
3. API端点变化 / API endpoint changes
4. 反爬虫机制 / Anti-scraping measures

### 性能优化 / Performance Optimization
- 使用连接池 / Use connection pooling
- 实现请求限流 / Implement request rate limiting
- 添加数据库索引 / Add database indexes
- 压缩API响应 / Compress API responses

### 安全注意事项 / Security Considerations
- 验证用户输入 / Validate user input
- 防止SQL注入 / Prevent SQL injection
- 添加速率限制 / Add rate limiting
- 使用HTTPS / Use HTTPS
- 遵守网站爬取政策 / Respect website scraping policies
