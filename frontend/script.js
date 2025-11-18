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
    const statsDiv = document.getElementById('stats');
    let html = `<p>数据库中共有 <span id="totalUniversities">${stats.total_universities}</span> 所大学</p>`;

    if (stats.by_source) {
        html += `
            <div class="stats-detail">
                <strong>各排名系统大学数量 / Universities by Ranking:</strong>
                <div class="stats-grid">
                    <span>QS: ${stats.by_source.qs}</span>
                    <span>THE: ${stats.by_source.the}</span>
                    <span>US News: ${stats.by_source.usnews}</span>
                    <span>ARWU: ${stats.by_source.arwu}</span>
                    <span>CS: ${stats.by_source.cs}</span>
                </div>
            </div>
        `;
    }

    statsDiv.innerHTML = html;
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
