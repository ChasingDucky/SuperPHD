// API Base URL - change this to your backend URL
const API_BASE_URL = 'http://localhost:5001/api';

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadCountries();

    // Add enter key support for search
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchUniversities();
        }
    });
});

// Show/hide loading indicator
function setLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// Display error message
function showError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="error">
            <strong>错误 / Error:</strong> ${message}
        </div>
    `;
}

// Display success message
function showSuccess(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="success">
            <strong>成功 / Success:</strong> ${message}
        </div>
    `;
}

// Search universities
async function searchUniversities() {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        showError('请输入大学名称 / Please enter a university name');
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error('搜索失败 / Search failed');
        }

        const universities = await response.json();
        displayResults(universities);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Calculate average ranking
async function calculateAverageRanking() {
    const query = document.getElementById('searchInput').value.trim();
    const selectedSources = getSelectedSources();

    if (selectedSources.length === 0) {
        showError('请至少选择一个排名来源 / Please select at least one ranking source');
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/average-ranking`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sources: selectedSources,
                query: query
            })
        });

        if (!response.ok) {
            throw new Error('计算失败 / Calculation failed');
        }

        const results = await response.json();
        displayAverageResults(results, selectedSources);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Get selected ranking sources
function getSelectedSources() {
    const sources = ['qs', 'the', 'usnews', 'arwu', 'cs'];
    return sources.filter(source => document.getElementById(source).checked);
}

// Display search results
function displayResults(universities) {
    const resultsDiv = document.getElementById('results');

    if (universities.length === 0) {
        resultsDiv.innerHTML = '<p class="no-data">未找到相关大学 / No universities found</p>';
        return;
    }

    let html = '<h2>搜索结果 / Search Results</h2>';

    universities.forEach(uni => {
        html += createUniversityCard(uni);
    });

    resultsDiv.innerHTML = html;
}

// Display average ranking results
function displayAverageResults(results, selectedSources) {
    const resultsDiv = document.getElementById('results');

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p class="no-data">未找到相关大学 / No universities found</p>';
        return;
    }

    const sourcesText = selectedSources.map(s => s.toUpperCase()).join(', ');
    let html = `<h2>平均排名结果 / Average Ranking Results (基于 / Based on: ${sourcesText})</h2>`;

    results.forEach((result, index) => {
        html += `
            <div class="university-card">
                <div class="average-rank">
                    <div class="ranking-label">平均排名 / Average Rank</div>
                    <div class="average-rank-value">#${result.average_rank}</div>
                    <div class="ranking-score">
                        基于 ${result.sources_count} / ${result.total_sources} 个排名来源
                        <br>Based on ${result.sources_count} of ${result.total_sources} sources
                    </div>
                </div>
                ${createUniversityCardContent(result.university)}
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
}

// Create university card
function createUniversityCard(uni) {
    return `
        <div class="university-card">
            ${createUniversityCardContent(uni)}
        </div>
    `;
}

// Create university card content
function createUniversityCardContent(uni) {
    const rankingLabels = {
        qs: 'QS',
        the: 'THE',
        usnews: 'US News',
        arwu: '软科 ARWU',
        cs: 'CS Rankings'
    };

    let rankingsHTML = '';
    for (const [key, label] of Object.entries(rankingLabels)) {
        const rank = uni.rankings[key].rank;
        const score = uni.rankings[key].score;

        if (rank !== null) {
            rankingsHTML += `
                <div class="ranking-item">
                    <div class="ranking-label">${label}</div>
                    <div class="ranking-value">#${rank}</div>
                    ${score !== null ? `<div class="ranking-score">${score}</div>` : ''}
                </div>
            `;
        } else {
            rankingsHTML += `
                <div class="ranking-item">
                    <div class="ranking-label">${label}</div>
                    <div class="ranking-value no-data">-</div>
                </div>
            `;
        }
    }

    const favorited = isFavorite(uni.name);
    const favoriteButtonText = favorited ? '★ 已收藏' : '⭐ 收藏';
    const favoriteButtonClass = favorited ? 'favorite-btn favorited' : 'favorite-btn';

    return `
        <div class="university-header">
            <div class="university-name">${uni.name}</div>
            <button class="${favoriteButtonClass}"
                    onclick="toggleFavorite('${uni.name.replace(/'/g, "\\'")}')"
                    data-university="${uni.name}">
                ${favoriteButtonText}
            </button>
        </div>
        ${uni.country ? `<div class="university-country">📍 ${uni.country}</div>` : ''}
        <div class="rankings-grid">
            ${rankingsHTML}
        </div>
    `;
}

// Update rankings from sources
async function updateRankings() {
    if (!confirm('确定要更新排名数据吗？这可能需要几分钟时间。\n\nAre you sure you want to update the rankings? This may take a few minutes.')) {
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/update`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('更新失败 / Update failed');
        }

        const result = await response.json();
        showSuccess('排名数据更新已开始，请稍后刷新页面查看最新数据。\n\nRanking update has started. Please refresh the page later to see the latest data.');

        // Reload stats after a delay
        setTimeout(loadStats, 5000);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Load database statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);

        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }

        const stats = await response.json();
        document.getElementById('totalUniversities').textContent = stats.total_universities;

        // Display detailed statistics if available
        if (stats.by_country || stats.by_source) {
            displayDetailedStats(stats);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display detailed statistics
function displayDetailedStats(stats) {
    const statsGrid = document.getElementById('statsGrid');
    let html = `
        <div class="stat-card">
            <div class="stat-icon">🎓</div>
            <div class="stat-value">${stats.total_universities}</div>
            <div class="stat-label">总大学数 / Total Universities</div>
        </div>
    `;

    if (stats.by_source) {
        html += `
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-value">${stats.by_source.qs}</div>
                <div class="stat-label">QS Rankings</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-value">${stats.by_source.the}</div>
                <div class="stat-label">THE Rankings</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🇺🇸</div>
                <div class="stat-value">${stats.by_source.usnews}</div>
                <div class="stat-label">US News</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎓</div>
                <div class="stat-value">${stats.by_source.arwu}</div>
                <div class="stat-label">ARWU/软科</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💻</div>
                <div class="stat-value">${stats.by_source.cs}</div>
                <div class="stat-label">CS Rankings</div>
            </div>
        `;
    }

    // Add country stats if available
    if (stats.by_country && stats.by_country.length > 0) {
        const topCountries = stats.by_country.slice(0, 5);
        topCountries.forEach((item, index) => {
            const flag = getFlagEmoji(item.country);
            html += `
                <div class="stat-card">
                    <div class="stat-icon">${flag}</div>
                    <div class="stat-value">${item.count}</div>
                    <div class="stat-label">${item.country}</div>
                </div>
            `;
        });
    }

    statsGrid.innerHTML = html;
}

// Helper function to get country flag emoji
function getFlagEmoji(country) {
    const flagMap = {
        'United States': '🇺🇸',
        'United Kingdom': '🇬🇧',
        'China': '🇨🇳',
        'Germany': '🇩🇪',
        'France': '🇫🇷',
        'Canada': '🇨🇦',
        'Australia': '🇦🇺',
        'Japan': '🇯🇵',
        'Switzerland': '🇨🇭',
        'Netherlands': '🇳🇱'
    };
    return flagMap[country] || '🌍';
}

// Load countries for filter
async function loadCountries() {
    try {
        const response = await fetch(`${API_BASE_URL}/countries`);

        if (!response.ok) {
            throw new Error('Failed to load countries');
        }

        const countries = await response.json();
        const select = document.getElementById('countryFilter');

        // Add options
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading countries:', error);
    }
}

// Filter by country
async function filterByCountry() {
    const country = document.getElementById('countryFilter').value;

    if (!country) {
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/filter?country=${encodeURIComponent(country)}`);

        if (!response.ok) {
            throw new Error('筛选失败 / Filter failed');
        }

        const universities = await response.json();
        displayResults(universities);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Export data as CSV
function exportData() {
    window.location.href = `${API_BASE_URL}/export`;
}

// Show compare dialog
function showCompareDialog() {
    document.getElementById('compareDialog').style.display = 'flex';
}

// Close compare dialog
function closeCompareDialog() {
    document.getElementById('compareDialog').style.display = 'none';
}

// Compare universities
async function compareUniversities() {
    const universities = [];

    // Collect university names from inputs
    for (let i = 1; i <= 5; i++) {
        const input = document.getElementById(`compare${i}`);
        if (input && input.value.trim()) {
            universities.push(input.value.trim());
        }
    }

    if (universities.length < 2) {
        alert('请至少输入2所大学名称 / Please enter at least 2 university names');
        return;
    }

    closeCompareDialog();
    setLoading(true);

    try {
        const selectedSources = getSelectedSources();

        const response = await fetch(`${API_BASE_URL}/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                universities: universities,
                sources: selectedSources
            })
        });

        if (!response.ok) {
            throw new Error('对比失败 / Comparison failed');
        }

        const results = await response.json();
        displayComparisonResults(results, selectedSources);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Display comparison results
function displayComparisonResults(results, sources) {
    const resultsDiv = document.getElementById('results');

    const sourcesText = sources.map(s => s.toUpperCase()).join(', ');
    let html = `<h2>大学对比结果 / University Comparison (${sourcesText})</h2>`;

    // Create comparison table
    html += `
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>大学 / University</th>
                    <th>平均排名 / Avg Rank</th>
                    ${sources.map(s => `<th>${s.toUpperCase()}</th>`).join('')}
                    <th>国家 / Country</th>
                </tr>
            </thead>
            <tbody>
    `;

    // Find best rank for each source
    const bestRanks = {};
    sources.forEach(source => {
        bestRanks[source] = Math.min(...results.map(r => {
            if (r.data && r.data.rankings[source].rank) {
                return r.data.rankings[source].rank;
            }
            return Infinity;
        }));
    });

    // Add rows
    results.forEach(result => {
        if (result.error) {
            html += `
                <tr>
                    <td class="university-name">${result.name}</td>
                    <td colspan="${sources.length + 2}" class="no-data">${result.error}</td>
                </tr>
            `;
        } else {
            html += `
                <tr>
                    <td class="university-name">${result.data.name}</td>
                    <td><strong>${result.average_rank || 'N/A'}</strong></td>
            `;

            sources.forEach(source => {
                const rank = result.data.rankings[source].rank;
                const isBest = rank && rank === bestRanks[source];
                html += `<td class="${isBest ? 'best-rank' : ''}">${rank || '-'}</td>`;
            });

            html += `
                    <td>${result.data.country || '-'}</td>
                </tr>
            `;
        }
    });

    html += `
            </tbody>
        </table>
    `;

    resultsDiv.innerHTML = html;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('compareDialog');
    if (event.target === modal) {
        closeCompareDialog();
    }
}

// ===== NEW FEATURES =====

// Global variable to store current results for sorting/filtering
let currentResults = [];
let currentResultsType = 'search'; // 'search', 'average', or 'favorites'

// === SORTING FUNCTIONALITY ===
function applySorting() {
    if (currentResults.length === 0) return;

    const sortBy = document.getElementById('sortBy').value;
    if (!sortBy) {
        displayCurrentResults();
        return;
    }

    const sorted = [...currentResults].sort((a, b) => {
        if (sortBy === 'name') {
            return a.name.localeCompare(b.name);
        } else {
            // Sort by ranking (lower rank number is better)
            const rankA = a.rankings?.[sortBy]?.rank || Infinity;
            const rankB = b.rankings?.[sortBy]?.rank || Infinity;
            return rankA - rankB;
        }
    });

    currentResults = sorted;
    displayCurrentResults();
}

// === ADVANCED FILTERING ===
function applyFilters() {
    const country = document.getElementById('countryFilter').value;
    const rankRange = document.getElementById('rankRangeFilter').value;

    // Build query parameters
    let params = new URLSearchParams();
    if (country) params.append('country', country);
    if (rankRange) {
        const [min, max] = rankRange.split('-').map(Number);
        params.append('min_rank', min);
        params.append('max_rank', max);
    }

    if (!country && !rankRange) {
        return;
    }

    setLoading(true);
    fetch(`${API_BASE_URL}/filter?${params.toString()}`)
        .then(response => response.json())
        .then(universities => {
            currentResults = universities;
            currentResultsType = 'search';
            displayCurrentResults();
        })
        .catch(error => showError(error.message))
        .finally(() => setLoading(false));
}

// === FAVORITES FUNCTIONALITY ===
function getFavorites() {
    const favorites = localStorage.getItem('universityFavorites');
    return favorites ? JSON.parse(favorites) : [];
}

function saveFavorites(favorites) {
    localStorage.setItem('universityFavorites', JSON.stringify(favorites));
    updateFavoritesCount();
}

function toggleFavorite(universityName) {
    let favorites = getFavorites();
    const index = favorites.findIndex(fav => fav.name === universityName);

    if (index > -1) {
        favorites.splice(index, 1);
    } else {
        // Add to favorites with timestamp
        favorites.push({
            name: universityName,
            addedAt: new Date().toISOString()
        });
    }

    saveFavorites(favorites);

    // Update UI
    const button = document.querySelector(`button[data-university="${universityName}"]`);
    if (button) {
        button.textContent = index > -1 ? '⭐ 收藏' : '★ 已收藏';
        button.classList.toggle('favorited');
    }
}

function isFavorite(universityName) {
    const favorites = getFavorites();
    return favorites.some(fav => fav.name === universityName);
}

function updateFavoritesCount() {
    const count = getFavorites().length;
    const countSpan = document.getElementById('favCount');
    if (countSpan) {
        countSpan.textContent = count;
    }
}

async function toggleFavoritesView() {
    const favorites = getFavorites();

    if (favorites.length === 0) {
        showError('没有收藏的大学 / No favorite universities');
        return;
    }

    setLoading(true);
    try {
        // Fetch details for all favorites
        const promises = favorites.map(fav =>
            fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(fav.name)}`)
                .then(r => r.json())
        );

        const results = await Promise.all(promises);
        const universities = results.flat().filter(u => u); // Remove nulls

        currentResults = universities;
        currentResultsType = 'favorites';
        displayCurrentResults();
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// === DARK MODE FUNCTIONALITY ===
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    // Update button icon
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
    }
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }
}

// === DISPLAY HELPERS ===
function displayCurrentResults() {
    if (currentResultsType === 'search' || currentResultsType === 'favorites') {
        displayResults(currentResults);
    } else if (currentResultsType === 'average') {
        const selectedSources = getSelectedSources();
        displayAverageResults(currentResults, selectedSources);
    }
}

// Update original display functions to store results
const originalDisplayResults = displayResults;
displayResults = function(universities) {
    currentResults = universities;
    currentResultsType = 'search';
    originalDisplayResults(universities);
}

const originalDisplayAverageResults = displayAverageResults;
displayAverageResults = function(results, selectedSources) {
    currentResults = results;
    currentResultsType = 'average';
    originalDisplayAverageResults(results, selectedSources);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    updateFavoritesCount();
});
