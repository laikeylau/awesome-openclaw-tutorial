---
layout: default
title: 搜索
---

<div class="search-container">
  <div class="search-box">
    <input type="text" id="search-input" placeholder="搜索标题、内容、关键词..." autocomplete="off">
    <button id="search-button">🔍 搜索</button>
  </div>

  <div id="search-results">
    <p class="search-hint">💡 输入关键词搜索教程内容（支持标题、摘要、全文搜索）</p>
  </div>
</div>

<style>
.search-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

#search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 2px solid #159957;
  border-right: none;
  outline: none;
  transition: all 0.3s;
}

#search-input:focus {
  border-color: #155799;
  box-shadow: 0 0 0 3px rgba(21, 153, 87, 0.1);
}

#search-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: linear-gradient(120deg, #155799, #159957);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
}

#search-button:hover {
  background: linear-gradient(120deg, #0d3f6f, #0f7a3f);
  transform: scale(1.05);
}

#search-button:active {
  transform: scale(0.98);
}

#search-results {
  min-height: 200px;
}

.search-hint {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  padding: 4rem 0;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

.search-result-item {
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: #ffffff;
  border: 1px solid #e1e4e8;
  border-left: 4px solid #159957;
  border-radius: 8px;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.search-result-item:hover {
  background: #f6f8fa;
  border-left-color: #155799;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.search-result-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.search-result-title a {
  color: #155799;
  text-decoration: none;
  transition: color 0.3s;
}

.search-result-title a:hover {
  color: #159957;
}

.search-result-excerpt {
  color: #586069;
  line-height: 1.6;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.search-result-url {
  font-size: 0.85rem;
  color: #159957;
  font-family: 'Courier New', monospace;
  opacity: 0.8;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  line-height: 1.8;
}

.no-results strong {
  color: #159957;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #159957;
  font-size: 1.2rem;
  font-weight: bold;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

mark {
  background-color: #fff3cd;
  padding: 0.1em 0.3em;
  border-radius: 3px;
  font-weight: bold;
  color: #856404;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-box {
    flex-direction: column;
  }
  
  #search-input {
    border: 2px solid #159957;
    border-radius: 8px 8px 0 0;
  }
  
  #search-button {
    border-radius: 0 0 8px 8px;
  }
  
  .search-result-item {
    padding: 1rem;
  }
  
  .search-result-title {
    font-size: 1.1rem;
  }
}
</style>

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script>
(function() {
  let searchIndex;
  let searchData;
  let loadAttempts = 0;
  const maxAttempts = 2;

  // HTML转义函数（防止XSS）
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // 尝试加载搜索数据
  function loadSearchData() {
    const searchFiles = [
      '{{ "/search.json" | relative_url }}',  // Jekyll生成的文件
      '{{ "/search-index.json" | relative_url }}'  // 静态备份文件
    ];
    
    const currentFile = searchFiles[loadAttempts];
    
    console.log(`🔍 尝试加载搜索索引 (${loadAttempts + 1}/${maxAttempts}): ${currentFile}`);
    
    fetch(currentFile)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (!data || data.length === 0) {
          throw new Error('搜索数据为空');
        }
        
        searchData = data;
        
        // 构建搜索索引（标题+摘要+内容）
        searchIndex = lunr(function() {
          this.ref('url');
          this.field('title', { boost: 10 });      // 标题权重最高
          this.field('excerpt', { boost: 3 });     // 摘要权重次之
          this.field('content', { boost: 1 });     // 内容权重较低

          // 添加中文分词支持
          this.pipeline.remove(lunr.stemmer);
          this.searchPipeline.remove(lunr.stemmer);

          data.forEach(doc => {
            this.add(doc);
          });
        });

        console.log('✅ 搜索索引已加载，共 ' + data.length + ' 个页面（标题+摘要+内容）');
        
        // 如果有URL参数，执行搜索
        const urlParams = new URLSearchParams(window.location.search);
        const queryParam = urlParams.get('q');
        if (queryParam) {
          document.getElementById('search-input').value = queryParam;
          performSearch(queryParam);
        }
      })
      .catch(error => {
        console.error(`❌ 加载失败 (${currentFile}):`, error);
        loadAttempts++;
        
        if (loadAttempts < maxAttempts) {
          // 尝试下一个文件
          setTimeout(loadSearchData, 500);
        } else {
          // 所有尝试都失败
          document.getElementById('search-results').innerHTML = `
            <div class="no-results">
              <p style="font-size: 1.2rem; margin-bottom: 1rem;">😕 搜索功能暂时不可用</p>
              <p style="margin-bottom: 1rem;">可能的原因：</p>
              <ul style="text-align: left; display: inline-block; margin-bottom: 1rem;">
                <li>网站正在构建中，请稍后再试</li>
                <li>网络连接问题</li>
                <li>浏览器缓存问题</li>
              </ul>
              <p>
                <button onclick="location.reload()" style="padding: 0.5rem 1rem; background: #159957; color: white; border: none; border-radius: 4px; cursor: pointer;">
                  🔄 刷新页面
                </button>
              </p>
              <p style="margin-top: 1.5rem; font-size: 0.9rem; color: #999;">
                或者直接查看 <a href="/" style="color: #159957;">教程目录</a>
              </p>
            </div>
          `;
        }
      });
  }
  
  // 开始加载
  loadSearchData();
  
  // 执行搜索
  function performSearch(query) {
    if (!searchIndex || !searchData) {
      document.getElementById('search-results').innerHTML = 
        '<p class="loading">⏳ 搜索索引加载中，请稍候...</p>';
      return;
    }
    
    if (!query || query.trim() === '') {
      document.getElementById('search-results').innerHTML = 
        '<p class="search-hint">💡 请输入搜索关键词</p>';
      return;
    }
    
    document.getElementById('search-results').innerHTML = 
      '<p class="loading">🔍 搜索中...</p>';
    
    try {
      // 执行搜索（多种策略）
      let results = [];

      // 策略1: 精确匹配
      results = searchIndex.search(query);

      // 策略2: 模糊匹配（通配符）
      if (results.length === 0) {
        results = searchIndex.search(query + '*');
      }

      // 策略3: 中文分词搜索
      if (results.length === 0 && /[\u4e00-\u9fa5]/.test(query)) {
        // 将查询拆分成字符，每个字符都模糊匹配
        const charQueries = [];
        for (let i = 0; i < query.length; i++) {
          const char = query[i];
          if (/[\u4e00-\u9fa5]/.test(char)) {
            charQueries.push(char);
          }
        }
        if (charQueries.length > 0) {
          const charQuery = charQueries.map(c => c + '~1').join(' ');
          results = searchIndex.search(charQuery);
        }
      }

      // 策略4: 双字符组合（中文大词匹配）
      if (results.length === 0 && /[\u4e00-\u9fa5]/.test(query) && query.length >= 2) {
        const bigrams = [];
        for (let i = 0; i < query.length - 1; i++) {
          bigrams.push(query.substr(i, 2));
        }
        if (bigrams.length > 0) {
          const bigramQuery = bigrams.map(b => b + '~2').join(' ');
          const bigramResults = searchIndex.search(bigramQuery);
          if (bigramResults.length > 0) {
            results = bigramResults;
          }
        }
      }

      // 策略5: 内容全文匹配（兜底方案）
      if (results.length === 0) {
        const queryLower = query.toLowerCase();
        const contentMatches = searchData.filter(doc => {
          const title = (doc.title || '').toLowerCase();
          const excerpt = (doc.excerpt || '').toLowerCase();
          const content = (doc.content || '').toLowerCase();
          return title.includes(queryLower) ||
                 excerpt.includes(queryLower) ||
                 content.includes(queryLower);
        }).map(doc => ({ ref: doc.url, score: 1 }));
        results = contentMatches;
      }

      const finalResults = results;
      
      if (finalResults.length === 0) {
        const noResultsDiv = document.createElement('div');
        noResultsDiv.className = 'no-results';
        noResultsDiv.innerHTML = `
          <p>😕 没有找到包含 "${escapeHtml(query)}" 的内容</p>
          <p>💡 搜索技巧：</p>
          <ul>
            <li>尝试使用更简���的关键词</li>
            <li>尝试同义词（如"安装"→"部署"）</li>
            <li>搜索英文关键词（如"API"、"Skills"）</li>
          </ul>
          <p>
            <a href="/">浏览教程目录</a> ·
            <a href="/appendix/A-command-reference.html">命令速查表</a>
          </p>
        `;
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = '';
        resultsContainer.appendChild(noResultsDiv);
        return;
      }
      
      // 显示结果
      let html = '<p style="margin-bottom: 1.5rem; color: #159957; font-weight: bold; font-size: 1.1rem;">✨ 找到 ' + finalResults.length + ' 个相关标题</p>';
      
      finalResults.slice(0, 30).forEach((result, index) => {
        const doc = searchData.find(d => d.url === result.ref);
        if (doc) {
          // 高亮标题中的关键词
          let title = doc.title || '无标题';
          const queryWords = query.split(/\s+/).filter(w => w.length > 0);
          
          // 高亮每个关键词
          queryWords.forEach(word => {
            const regex = new RegExp('(' + word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
            title = title.replace(regex, '<mark>$1</mark>');
          });
          
          // 显示摘要（优先显示包含关键词的内容片段）
          let excerpt = doc.excerpt || '';
          let content = doc.content || '';

          // 尝试在内容中找到包含关键词的片段
          if (content && queryWords.length > 0) {
            for (const word of queryWords) {
              const index = content.indexOf(word);
              if (index !== -1) {
                const start = Math.max(0, index - 40);
                const end = Math.min(content.length, index + word.length + 40);
                excerpt = (start > 0 ? '...' : '') + content.substring(start, end) + (end < content.length ? '...' : '');
                break;
              }
            }
          }

          if (excerpt.length > 200) {
            excerpt = excerpt.substring(0, 200) + '...';
          }
          
          // 分类标签
          let categoryBadge = '';
          if (doc.category) {
            const categoryMap = {
              'docs': '📚 文档',
              'appendix': '📖 附录',
              'examples': '💡 示例',
              'guide': '🎯 指南',
              'root': '🏠 首页'
            };
            const categoryName = categoryMap[doc.category] || doc.category;
            categoryBadge = `<span style="display: inline-block; padding: 0.2rem 0.5rem; background: #e1f5fe; color: #0277bd; border-radius: 3px; font-size: 0.85rem; margin-right: 0.5rem;">${categoryName}</span>`;
          }
          
          html += `
            <div class="search-result-item">
              <div class="search-result-title">
                <span style="color: #999; margin-right: 0.5rem;">${index + 1}.</span>
                ${categoryBadge}
                <a href="${doc.url}">${title}</a>
              </div>
              ${excerpt ? '<div class="search-result-excerpt">' + excerpt + '</div>' : ''}
              <div class="search-result-url">📄 ${doc.url}</div>
            </div>
          `;
        }
      });
      
      if (finalResults.length > 30) {
        html += '<p style="text-align: center; color: #666; margin-top: 2rem;">显示前 30 个结果，共 ' + finalResults.length + ' 个</p>';
      }
      
      document.getElementById('search-results').innerHTML = html;
    } catch (error) {
      console.error('❌ 搜索出错:', error);
      document.getElementById('search-results').innerHTML = 
        '<p class="no-results">搜索出错，请刷新页面重试</p>';
    }
  }
  
  // 绑定搜索事件
  document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value;
    performSearch(query);
  });
  
  document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      const query = this.value;
      performSearch(query);
    }
  });
  
  // 实时搜索（可选，输入时自动搜索）
  let searchTimeout;
  document.getElementById('search-input').addEventListener('input', function() {
    clearTimeout(searchTimeout);
    const query = this.value;
    if (query.length >= 2) { // 至少2个字符才开始搜索
      searchTimeout = setTimeout(() => performSearch(query), 300);
    } else if (query.length === 0) {
      document.getElementById('search-results').innerHTML = 
        '<p class="search-hint">💡 请输入搜索关键词</p>';
    }
  });
})();
</script>
