# 快速开始指南 / Quick Start Guide

## 安装依赖 / Installation

### 1. 安装Python依赖 / Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动后端服务器 / Start Backend Server

```bash
cd backend
python app.py
```

服务器将在 `http://localhost:5001` 启动
The server will start at `http://localhost:5001`

### 3. 打开前端页面 / Open Frontend

直接在浏览器中打开 `frontend/index.html` 文件
Simply open the `frontend/index.html` file in your browser

或者使用简单的HTTP服务器（推荐）:
Or use a simple HTTP server (recommended):

```bash
cd frontend
python -m http.server 8000
```

然后访问 `http://localhost:8000`
Then visit `http://localhost:8000`

## 使用方法 / Usage

### 搜索大学 / Search Universities

1. 在搜索框中输入大学名称（支持中英文）
   Enter university name in the search box (Chinese and English supported)

2. 点击"搜索"按钮或按回车键
   Click the "Search" button or press Enter

3. 查看各个排名榜单中的数据
   View data from different ranking sources

### 计算平均排名 / Calculate Average Ranking

1. 勾选想要包含在平均计算中的排名来源
   Check the ranking sources you want to include in the average

2. （可选）在搜索框中输入大学名称以过滤结果
   (Optional) Enter university name in search box to filter results

3. 点击"计算平均排名"按钮
   Click the "Calculate Average" button

4. 系统会显示按平均排名排序的结果
   The system will display results sorted by average ranking

### 更新排名数据 / Update Rankings Data

点击"更新数据"按钮从各个来源重新抓取最新排名数据
Click the "Update Data" button to re-scrape latest rankings from all sources

注意：这可能需要几分钟时间
Note: This may take a few minutes

## 排名来源 / Ranking Sources

- **QS**: QS World University Rankings
- **THE**: Times Higher Education World University Rankings
- **US News**: US News Best Global Universities
- **软科 (ARWU)**: Academic Ranking of World Universities (Shanghai Ranking)
- **CS Rankings**: Computer Science Rankings (csrankings.org)

## 常见问题 / FAQ

### Q: macOS上遇到"Address already in use"或"Port 5001 is in use"错误怎么办？
**A**: 如果端口5001也被占用，您可以修改 `backend/config.py` 中的 `FLASK_PORT` 为其他端口（如5002），然后同时修改 `frontend/script.js` 中的 `API_BASE_URL` 为相应端口。

### Q: What if I get "Address already in use" or "Port 5001 is in use" error on macOS?
**A**: If port 5001 is also occupied, you can modify `FLASK_PORT` in `backend/config.py` to another port (e.g., 5002), and also update `API_BASE_URL` in `frontend/script.js` to match.

### Q: 为什么某些大学在某个排名中没有数据？
**A**: 不同的排名系统可能不包括所有大学，或者该大学在该排名中未上榜。

### Q: Why doesn't a university have data in certain rankings?
**A**: Different ranking systems may not include all universities, or the university may not be ranked in that particular system.

### Q: 数据多久更新一次？
**A**: 默认使用示例数据。您可以点击"更新数据"按钮手动更新（需要访问互联网）。

### Q: How often is the data updated?
**A**: Sample data is used by default. You can manually update by clicking the "Update Data" button (requires internet access).

### Q: 平均排名是如何计算的？
**A**: 平均排名是所选排名来源中该大学排名的算术平均值。只有在该排名中有数据的来源才会被计入计算。

### Q: How is the average ranking calculated?
**A**: The average ranking is the arithmetic mean of the university's rankings in the selected sources. Only sources where the university has a ranking are included in the calculation.

## 技术支持 / Technical Support

如果遇到问题，请检查：
If you encounter issues, please check:

1. Python 3.7+ 已安装 / Python 3.7+ is installed
2. 所有依赖已正确安装 / All dependencies are properly installed
3. 后端服务器正在运行 / Backend server is running
4. 浏览器控制台没有错误 / Browser console shows no errors

## 注意事项 / Important Notes

⚠️ **免责声明 / Disclaimer**:

- 本工具仅供学习和参考使用
  This tool is for educational and reference purposes only

- 网络爬虫可能受到网站服务条款的限制
  Web scraping may be subject to website terms of service

- 排名数据的准确性取决于源网站
  The accuracy of ranking data depends on the source websites

- 请合理使用，避免频繁请求
  Please use responsibly and avoid frequent requests
