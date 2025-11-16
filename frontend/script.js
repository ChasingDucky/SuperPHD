// API Base URL - change this to your backend URL
const API_BASE_URL = 'http://localhost:5001/api';

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadStats();

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

    return `
        <div class="university-name">${uni.name}</div>
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
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}
