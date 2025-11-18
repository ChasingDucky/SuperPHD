# 新功能使用指南 / New Features Guide

## 🎉 最新更新 / Latest Updates

系统新增了4个强大的功能，让您的大学排名查询体验更加完善！

The system now includes 4 powerful new features for an enhanced university ranking experience!

---

## 1. ⚖️ 大学对比功能 / University Comparison

### 如何使用 / How to Use

1. 点击页面上的 **"⚖️ 对比大学 / Compare"** 按钮
2. 在弹出的对话框中输入2-5所大学的名称
3. 点击 **"开始对比 / Start Comparison"**
4. 查看对比结果表格

### 功能特点 / Features

- ✅ 同时对比2-5所大学
- ✅ 自动高亮最佳排名（绿色背景）
- ✅ 显示平均排名
- ✅ 支持选择不同的排名源进行对比
- ✅ 清晰的表格展示，一目了然

### 示例 / Example

对比 "MIT", "Stanford", "Harvard" 的排名：

```
大学            平均排名    QS    THE    US News    ARWU    CS    国家
MIT             2.4        1     3      2          3       2     United States
Stanford        3.6        5     2      3          2       4     United States
Harvard         2.0        4     4      1          1       N/A   United States
```

最佳排名会以绿色背景高亮显示！

---

## 2. 🌍 国家筛选功能 / Country Filter

### 如何使用 / How to Use

1. 在搜索框下方找到 **"按国家筛选 / Filter by Country"** 下拉菜单
2. 选择您想查看的国家（如 "United States", "China", "United Kingdom" 等）
3. 系统自动显示该国家的所有大学

### 功能特点 / Features

- ✅ 动态加载所有国家列表
- ✅ 即时筛选，无需点击按钮
- ✅ 支持所有数据库中的国家
- ✅ 方便查看特定国家的大学排名

### 使用场景 / Use Cases

- 🎓 查看美国所有顶尖大学
- 🇨🇳 专注中国大学排名
- 🇬🇧 了解英国大学情况
- 🌏 对比不同国家的教育水平

---

## 3. 📥 数据导出功能 / CSV Export

### 如何使用 / How to Use

1. 点击页面上的 **"📥 导出CSV / Export CSV"** 按钮
2. 浏览器会自动下载 `university_rankings.csv` 文件
3. 使用Excel、Google Sheets或Numbers打开查看

### 导出内容 / Export Contents

导出的CSV文件包含：
- 所有大学名称
- 所在国家
- 5个排名系统的排名和分数：
  - QS Rank & Score
  - THE Rank & Score
  - US News Rank & Score
  - ARWU Rank & Score
  - CS Rank & Score

### 使用场景 / Use Cases

- 📊 在Excel中进行深度数据分析
- 📈 创建自定义图表和可视化
- 💾 备份当前数据
- 📧 分享数据给他人
- 🔬 用于研究和论文

---

## 4. 📊 增强统计面板 / Enhanced Statistics Dashboard

### 新增信息 / New Information

统计面板现在显示：

**各排名系统大学数量 / Universities by Ranking:**
- QS: 50所大学
- THE: 50所大学
- US News: 50所大学
- ARWU: 50所大学
- CS Rankings: 12所大学

**按国家统计（Top 10）:**
- 显示数据库中大学数量最多的前10个国家

### 价值 / Value

- 📈 了解数据库覆盖范围
- 🌍 查看各国大学分布
- 📊 验证数据完整性
- 🎯 发现数据更新状态

---

## 🎯 完整工作流示例 / Complete Workflow Example

### 场景：申请美国计算机科学研究生 / Scenario: Applying for CS Graduate Programs in USA

1. **筛选国家** 🌍
   - 在国家筛选下拉菜单选择 "United States"
   - 查看所有美国大学

2. **选择排名源** ✅
   - 勾选 QS、US News、CS Rankings
   - 取消勾选 THE 和 ARWU（专注CS相关排名）

3. **计算平均排名** 📊
   - 点击 "计算平均排名"
   - 查看综合排名最佳的美国大学

4. **对比目标学校** ⚖️
   - 选择3-5所感兴趣的大学
   - 点击 "对比大学"
   - 输入：MIT, Stanford, Carnegie Mellon, Berkeley, UIUC
   - 查看详细对比结果

5. **导出数据** 📥
   - 点击 "导出CSV"
   - 在Excel中进一步分析
   - 制作申请学校列表

---

## 💡 使用技巧 / Pro Tips

### 搜索技巧 / Search Tips

- 搜索支持部分匹配：输入 "MIT" 可以找到 "Massachusetts Institute of Technology (MIT)"
- 支持中英文：搜索 "清华" 或 "Tsinghua" 都可以
- 不区分大小写

### 对比技巧 / Comparison Tips

- 对比前先选择相关的排名源，这样结果更有针对性
- 可以只输入2所大学进行对比
- 绿色高亮的是每个排名中的最佳名次
- 平均排名越小越好

### 筛选技巧 / Filtering Tips

- 选择国家后，可以再进行搜索或计算平均排名
- 选择 "所有国家" 可以清除筛选
- 国家列表按字母顺序排列

### 导出技巧 / Export Tips

- 导出的CSV文件可以直接导入到其他分析工具
- 使用Excel的数据透视表功能进行深度分析
- 可以在导出前先筛选或搜索，只导出需要的数据

---

## ⚙️ API使用 / API Usage

如果您想直接使用API：

### 对比大学 / Compare Universities
```bash
curl -X POST http://localhost:5001/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "universities": ["MIT", "Stanford", "Harvard"],
    "sources": ["qs", "the", "usnews"]
  }'
```

### 按国家筛选 / Filter by Country
```bash
curl http://localhost:5001/api/filter?country=United%20States
```

### 导出CSV / Export CSV
```bash
curl http://localhost:5001/api/export > rankings.csv
```

### 获取国家列表 / Get Countries
```bash
curl http://localhost:5001/api/countries
```

---

## 🐛 常见问题 / FAQ

### Q: 对比功能找不到某所大学怎么办？
**A**: 确保大学名称拼写正确。可以先搜索该大学，然后复制准确的名称用于对比。

### Q: Can't find a university in comparison?
**A**: Make sure the spelling is correct. You can search for the university first, then copy the exact name for comparison.

### Q: 导出的CSV文件在哪里？
**A**: 通常在浏览器的默认下载文件夹。文件名为 `university_rankings.csv`。

### Q: Where is the exported CSV file?
**A**: Usually in your browser's default download folder. The filename is `university_rankings.csv`.

### Q: 可以同时对比超过5所大学吗？
**A**: 目前最多支持5所大学同时对比。如需对比更多，可以分批进行。

### Q: Can I compare more than 5 universities at once?
**A**: Currently limited to 5 universities. For more, you can do multiple comparisons.

---

## 🎓 最佳实践 / Best Practices

1. **明确目标** - 先确定您关注哪些排名指标
2. **多维对比** - 使用不同排名源组合获取全面视角
3. **数据导出** - 定期导出数据进行长期追踪
4. **国家筛选** - 先缩小范围再深入研究
5. **保存结果** - 重要的对比结果可以截图保存

---

## 📚 相关文档 / Related Documentation

- `README.md` - 项目总览和安装指南
- `QUICKSTART.md` - 快速开始指南
- `DATA_INFO.md` - 数据来源和更新说明
- `FEATURES.md` - 完整功能列表
- `PROJECT_STRUCTURE.md` - 项目结构说明

---

## 🚀 未来计划 / Future Plans

我们计划继续添加：
- 📈 可视化图表（排名趋势图）
- 💾 用户收藏功能
- 🔔 排名变化提醒
- 📱 移动应用
- 🌐 更多排名源

---

**享受使用！/ Enjoy!** 🎉

如有问题或建议，欢迎反馈！
If you have questions or suggestions, feel free to provide feedback!
