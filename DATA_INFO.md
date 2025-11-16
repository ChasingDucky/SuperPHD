# 数据说明 / Data Information

## 当前数据状态 / Current Data Status

本系统目前使用**示例数据**用于演示目的。示例数据包含约50所顶尖大学的排名信息。

The system currently uses **sample data** for demonstration purposes. The sample data contains ranking information for approximately 50 top universities.

## 为什么使用示例数据？/ Why Sample Data?

大多数大学排名网站使用JavaScript动态加载数据，并设有反爬虫机制，因此：

Most university ranking websites use JavaScript to dynamically load data and have anti-scraping measures, therefore:

1. **技术限制** / Technical Limitations
   - 需要使用Selenium等浏览器自动化工具
   - 需要处理CAPTCHA验证
   - 可能需要代理IP池

2. **法律和道德考虑** / Legal and Ethical Considerations
   - 遵守网站的服务条款 / Respect website terms of service
   - 避免过度请求影响网站 / Avoid excessive requests
   - 尊重版权和数据所有权 / Respect copyright and data ownership

## 数据来源 / Data Sources

示例数据来自以下公开排名（2023-2024年数据）：

Sample data is from the following public rankings (2023-2024 data):

- **QS**: QS World University Rankings
- **THE**: Times Higher Education World University Rankings
- **US News**: US News Best Global Universities
- **软科 (ARWU)**: Academic Ranking of World Universities
- **CS Rankings**: csrankings.org Computer Science Rankings

## 如何获取更多数据？/ How to Get More Data?

### 方法 1: 使用CSV导入 / Method 1: Import from CSV

您可以创建自己的CSV文件并导入系统：

You can create your own CSV file and import it into the system:

1. **准备CSV文件**：参考 `backend/data/sample_rankings.csv` 的格式

   **Prepare CSV file**: Follow the format of `backend/data/sample_rankings.csv`

   格式 / Format:
   ```csv
   university,country,qs_rank,qs_score,the_rank,the_score,usnews_rank,usnews_score,arwu_rank,arwu_score,cs_rank,cs_score
   MIT,United States,1,100.0,3,95.2,2,98.5,3,73.8,2,6.8
   ```

2. **导入数据**：
   ```bash
   cd backend
   python import_data.py your_data.csv
   ```

3. **验证导入**：
   ```bash
   python app.py
   ```

### 方法 2: 手动从官方网站获取 / Method 2: Manual Collection from Official Websites

1. 访问各排名官方网站
2. 手动记录排名数据
3. 创建CSV文件
4. 使用上述导入方法

### 方法 3: 使用官方API（如有）/ Method 3: Use Official APIs (if available)

某些排名组织可能提供官方API或数据下载：

Some ranking organizations may provide official APIs or data downloads:

- 检查官网是否有数据下载选项
- 申请API访问权限
- 使用官方工具

### 方法 4: 改进爬虫 / Method 4: Improve Scrapers

如果您有技术能力，可以改进爬虫：

If you have technical skills, you can improve the scrapers:

1. **使用Selenium**：
   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome.options import Options

   options = Options()
   options.add_argument('--headless')
   driver = webdriver.Chrome(options=options)
   driver.get(url)
   # 提取数据...
   ```

2. **使用Playwright**：
   ```python
   from playwright.sync_api import sync_playwright

   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       page.goto(url)
       # 提取数据...
   ```

3. **使用API端点**：
   - 检查网站的网络请求
   - 找到API端点
   - 直接调用API获取JSON数据

## 数据更新频率 / Data Update Frequency

**示例数据**基于2023-2024年的排名，每年更新一次。

**Sample data** is based on 2023-2024 rankings and updates annually.

官方排名通常的更新时间：

Official rankings typically update:

- **QS**: 每年6月 / June annually
- **THE**: 每年10月 / October annually
- **US News**: 每年10月 / October annually
- **软科 (ARWU)**: 每年8月 / August annually
- **CS Rankings**: 持续更新 / Continuously updated

## 数据质量说明 / Data Quality Notes

### 示例数据的局限性 / Limitations of Sample Data

1. **覆盖范围有限** / Limited Coverage
   - 仅包含约50所大学 / Only ~50 universities included
   - 主要是顶尖大学 / Mainly top-ranked universities
   - 某些学校在某些榜单上没有数据 / Some universities missing from certain rankings

2. **可能不是最新** / May Not Be Latest
   - 基于2023-2024学年数据 / Based on 2023-2024 academic year
   - 排名可能已变化 / Rankings may have changed

3. **仅供参考** / For Reference Only
   - 不应作为申请决策的唯一依据 / Should not be sole basis for application decisions
   - 建议查看官方网站获取最新数据 / Recommend checking official websites for latest data

## 官方网站链接 / Official Website Links

- **QS**: https://www.topuniversities.com/world-university-rankings
- **THE**: https://www.timeshighereducation.com/world-university-rankings
- **US News**: https://www.usnews.com/education/best-global-universities
- **软科 (ARWU)**: https://www.shanghairanking.com/rankings/arwu/
- **CS Rankings**: https://csrankings.org/

## 免责声明 / Disclaimer

此工具仅用于教育和研究目的。排名数据的准确性取决于源网站。请访问官方网站获取最新和最准确的信息。

This tool is for educational and research purposes only. The accuracy of ranking data depends on the source websites. Please visit official websites for the latest and most accurate information.

## 贡献数据 / Contributing Data

如果您有更完整的排名数据，欢迎贡献：

If you have more complete ranking data, contributions are welcome:

1. Fork项目 / Fork the project
2. 添加数据到CSV文件 / Add data to CSV file
3. 测试导入 / Test the import
4. 提交Pull Request / Submit a Pull Request

## 技术支持 / Technical Support

如有数据导入或爬虫相关问题，请查看：

For data import or scraper-related questions, please see:

- `backend/import_data.py` - CSV导入脚本 / CSV import script
- `backend/test_scrapers.py` - 爬虫测试工具 / Scraper testing tool
- `backend/scrapers/` - 爬虫实现 / Scraper implementations
