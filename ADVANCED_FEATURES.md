# Advanced Features Guide / 高级功能指南

本指南介绍系统的高级功能特性。

This guide introduces the advanced features of the system.

---

## 🆕 新增功能 / New Features

### 1. 📊 结果排序 / Result Sorting

**功能描述 / Description:**
- 支持按不同排名源或名称排序搜索结果
- Supports sorting search results by different ranking sources or name

**使用方法 / How to Use:**
1. 在筛选栏找到"排序 / Sort by"下拉菜单
2. 选择排序方式：
   - 默认 / Default - 原始顺序
   - 名称 / Name - 按字母顺序
   - QS Rank - 按QS排名
   - THE Rank - 按THE排名
   - US News - 按US News排名
   - ARWU - 按ARWU排名
   - CS Rank - 按CS排名
3. 结果会自动重新排序

**技术实现 / Technical Implementation:**
- 前端JavaScript实时排序
- 支持数字和字符串排序
- 无排名的大学排在末尾

---

### 2. 🔍 高级筛选 / Advanced Filtering

**功能描述 / Description:**
- 支持按排名范围筛选大学
- Supports filtering universities by ranking range

**使用方法 / How to Use:**
1. 在筛选栏找到"排名范围 / Rank Range"下拉菜单
2. 选择范围：
   - 所有 / All
   - Top 10 - 前10名
   - Top 20 - 前20名
   - Top 50 - 前50名
   - Top 100 - 前100名
3. 系统自动筛选并显示结果

**技术实现 / Technical Implementation:**
- 后端API支持min_rank和max_rank参数
- 基于平均排名进行筛选
- 可与国家筛选组合使用

**API示例 / API Example:**
```bash
# 查询Top 50大学
curl "http://localhost:5001/api/filter?min_rank=1&max_rank=50"

# 查询美国Top 20大学
curl "http://localhost:5001/api/filter?country=United%20States&min_rank=1&max_rank=20"
```

---

### 3. ⭐ 收藏功能 / Favorites Feature

**功能描述 / Description:**
- 收藏感兴趣的大学，方便后续查看
- Bookmark universities of interest for easy access later

**使用方法 / How to Use:**

**收藏大学 / Bookmark a University:**
1. 搜索并找到目标大学
2. 点击大学卡片上的"⭐ 收藏"按钮
3. 按钮变为"★ 已收藏"表示成功

**取消收藏 / Remove from Favorites:**
1. 再次点击"★ 已收藏"按钮
2. 按钮变回"⭐ 收藏"

**查看所有收藏 / View All Favorites:**
1. 点击筛选栏的"⭐ 收藏 / Favorites (X)"按钮
2. 系统显示所有已收藏的大学
3. 可以对收藏结果进行排序

**技术实现 / Technical Implementation:**
- 使用localStorage本地存储
- 数据格式：`{name: string, addedAt: timestamp}`
- 实时更新收藏计数
- 自动持久化，刷新页面不丢失

**数据结构 / Data Structure:**
```javascript
[
  {
    "name": "Massachusetts Institute of Technology (MIT)",
    "addedAt": "2025-11-18T22:30:00.000Z"
  },
  {
    "name": "Stanford University",
    "addedAt": "2025-11-18T22:31:00.000Z"
  }
]
```

---

### 4. 🌙 暗色模式 / Dark Mode

**功能描述 / Description:**
- 护眼的暗色主题
- Eye-friendly dark theme

**使用方法 / How to Use:**
1. 点击导航栏右上角的主题切换按钮（🌙 或 ☀️）
2. 主题立即切换
3. 设置自动保存，下次访问自动应用

**主题特性 / Theme Features:**
- **亮色模式 / Light Mode:**
  - 白色背景，深色文字
  - 渐变彩色背景
  - 适合白天使用

- **暗色模式 / Dark Mode:**
  - 深色背景，浅色文字
  - 降低蓝光
  - 适合夜间使用

**技术实现 / Technical Implementation:**
- CSS变量系统自动切换配色
- localStorage保存主题偏好
- 平滑过渡动画
- 所有组件完整支持

**CSS变量示例 / CSS Variables Example:**
```css
/* 亮色模式 */
:root {
  --bg-primary: #ffffff;
  --gray-900: #111827;
}

/* 暗色模式 */
[data-theme="dark"] {
  --bg-primary: #111827;
  --gray-900: #f9fafb;
}
```

---

## 🎯 功能组合使用 / Combined Usage

### 场景1：查找美国Top 20 CS专业大学

1. **国家筛选**: 选择"United States"
2. **排名范围**: 选择"Top 20"
3. **排序**: 选择"CS Rank"
4. **收藏**: 对感兴趣的大学点击收藏
5. **导出**: 点击"导出CSV"保存结果

### 场景2：夜间浏览已收藏的大学

1. **暗色模式**: 点击🌙切换到暗色主题
2. **查看收藏**: 点击"⭐ 收藏"按钮
3. **排序**: 按QS Rank排序查看
4. **对比**: 选择几所进行详细对比

---

## 📱 响应式支持 / Responsive Support

所有新功能完全支持移动设备：
- 筛选栏自动换行
- 触摸友好的按钮尺寸
- 优化的移动端布局

All new features fully support mobile devices:
- Filter bar auto-wraps
- Touch-friendly button sizes
- Optimized mobile layout

---

## 💾 数据持久化 / Data Persistence

### 收藏数据 / Favorites Data
- 存储位置：localStorage
- 键名：`universityFavorites`
- 自动保存，无需手动操作

### 主题设置 / Theme Settings
- 存储位置：localStorage
- 键名：`theme`
- 值：`'light'` 或 `'dark'`

### 清除数据 / Clear Data
```javascript
// 清除收藏
localStorage.removeItem('universityFavorites');

// 重置主题
localStorage.removeItem('theme');
```

---

## 🚀 性能优化 / Performance Optimization

1. **排序**: 客户端排序，无需服务器请求
2. **收藏**: localStorage访问速度快
3. **主题切换**: CSS变量实时生效，无需重新渲染
4. **筛选**: 服务端筛选，减少数据传输

---

## 🔧 故障排除 / Troubleshooting

### 收藏不显示
- 检查浏览器是否启用localStorage
- 清除浏览器缓存后重试

### 暗色模式不生效
- 刷新页面
- 检查浏览器是否支持CSS变量

### 排序不工作
- 确保有搜索结果
- 尝试重新搜索

---

## 📊 使用统计 / Usage Analytics

系统现在支持：
- ✅ 5种排序方式
- ✅ 5种排名范围筛选
- ✅ 无限收藏容量（受localStorage限制，约5MB）
- ✅ 2种主题模式

---

**Enjoy the enhanced features! / 享受增强的功能体验！** 🎉
