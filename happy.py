#!/usr/bin/env python3
"""
Happy - Quantum-Enhanced Entertainment Search Engine
Integrates real-world site data with Reddit to find powerful entertainment information
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import re
from flask import Flask, render_template_string, request as flask_request, jsonify

class HappySearchEngine:
    def __init__(self):
        self.reddit_base = "https://www.reddit.com"
        self.search_results = []
        
    def quantum_score(self, text: str) -> float:
        """
        Quantum-inspired scoring algorithm
        Uses the 1x-z zen 1/2 limit formula for relevance scoring
        """
        # Calculate quantum-inspired relevance score
        x = len(text.split())  # word count
        z = text.count('!')    # excitement factor
        
        # Apply the limit formula: 1/(1+x-z) with zen factor
        if x - z <= 0:
            score = 1.0
        else:
            score = 1.0 / (1.0 + (x - z) * 0.5)
        
        # Apply entertainment keywords boost
        entertainment_keywords = ['movie', 'show', 'game', 'music', 'video', 'series', 
                                 'film', 'entertainment', 'watch', 'play', 'stream']
        keyword_bonus = sum(1 for kw in entertainment_keywords if kw.lower() in text.lower())
        
        return min(score + (keyword_bonus * 0.1), 1.0)
    
    def search_reddit(self, query: str, subreddit: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Reddit for entertainment content
        """
        print(f"🔍 Searching Reddit for: {query}")
        
        try:
            # Use Reddit JSON API (no auth required for public data)
            url = f"{self.reddit_base}/r/{subreddit}/search.json"
            params = {
                'q': query,
                'limit': limit,
                'sort': 'relevance',
                'type': 'link'
            }
            headers = {'User-Agent': 'Happy/1.0'}
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for post in data['data']['children']:
                    post_data = post['data']
                    
                    # Calculate quantum relevance score
                    combined_text = f"{post_data['title']} {post_data.get('selftext', '')}"
                    quantum_score = self.quantum_score(combined_text)
                    
                    posts.append({
                        'title': post_data['title'],
                        'url': post_data['url'],
                        'subreddit': post_data['subreddit'],
                        'score': post_data['score'],
                        'quantum_relevance': round(quantum_score, 3),
                        'comments': post_data['num_comments'],
                        'created': datetime.fromtimestamp(post_data['created_utc']).strftime('%Y-%m-%d %H:%M')
                    })
                
                # Sort by quantum relevance score
                posts.sort(key=lambda x: x['quantum_relevance'], reverse=True)
                self.search_results = posts
                return posts
            else:
                print(f"❌ Error: Reddit API returned status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching Reddit: {e}")
            return []
    
    def display_results(self):
        """
        Display search results with quantum scores
        """
        if not self.search_results:
            print("No results found.")
            return
        
        print(f"\n{'='*80}")
        print(f"🎉 HAPPY SEARCH RESULTS (Quantum-Enhanced)")
        print(f"{'='*80}\n")
        
        for idx, result in enumerate(self.search_results[:10], 1):
            print(f"#{idx} | Quantum Score: {result['quantum_relevance']} | Reddit Score: {result['score']}")
            print(f"📌 {result['title']}")
            print(f"🔗 {result['url']}")
            print(f"💬 {result['comments']} comments | r/{result['subreddit']} | {result['created']}")
            print(f"{'-'*80}\n")
    
    def search_entertainment(self, query: str, categories: List[str] = None):
        """
        Multi-category entertainment search
        """
        if categories is None:
            categories = ['movies', 'television', 'gaming', 'music', 'entertainment']
        
        all_results = []
        
        for category in categories:
            print(f"\n🎬 Searching r/{category}...")
            results = self.search_reddit(query, subreddit=category, limit=5)
            all_results.extend(results)
        
        # Remove duplicates and sort by quantum score
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        unique_results.sort(key=lambda x: x['quantum_relevance'], reverse=True)
        self.search_results = unique_results
        
        return unique_results


def main():
    """
    Main entry point - start Flask server
    """
    app = Flask(__name__)
    engine = HappySearchEngine()
    
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Happy - Quantum Entertainment Search</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #2c3e50; }
            .search-box { display: flex; gap: 10px; margin: 20px 0; }
            input { flex: 1; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .result { border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 5px; background: #f9f9f9; }
            .score { display: inline-block; background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px; margin-right: 10px; }
            .title { font-weight: bold; font-size: 18px; color: #2c3e50; margin: 10px 0; }
            .url { color: #3498db; text-decoration: none; word-break: break-all; }
            .meta { color: #7f8c8d; font-size: 14px; margin-top: 10px; }
            .loading { text-align: center; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Happy - Quantum Entertainment Search 🌟</h1>
            <div class="search-box">
                <input type="text" id="query" placeholder="Enter entertainment search query..." value="best sci-fi">
                <button onclick="search()">Search</button>
            </div>
            <div id="results"></div>
        </div>
        <script>
            function search() {
                const query = document.getElementById('query').value;
                document.getElementById('results').innerHTML = '<p class="loading">Searching...</p>';
                fetch('/api/search?q=' + encodeURIComponent(query))
                    .then(r => r.json())
                    .then(data => {
                        let html = '<h2>Results (' + data.results.length + ' found)</h2>';
                        data.results.forEach((r, i) => {
                            html += `<div class="result">
                                <span class="score">Score: ${r.quantum_relevance}</span>
                                <div class="title">${i+1}. ${r.title}</div>
                                <a href="${r.url}" class="url" target="_blank">${r.url}</a>
                                <div class="meta">💬 ${r.comments} comments | r/${r.subreddit} | ${r.created}</div>
                            </div>`;
                        });
                        document.getElementById('results').innerHTML = html;
                    })
                    .catch(e => {
                        document.getElementById('results').innerHTML = '<p style="color: red;">Error: ' + e + '</p>';
                    });
            }
            // Auto-search on load
            window.onload = search;
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def home():
        return render_template_string(html_template)
    
    @app.route('/api/search')
    def api_search():
        query = flask_request.args.get('q', 'best sci-fi')
        categories = ['movies', 'television', 'gaming', 'music', 'entertainment']
        
        all_results = []
        for category in categories:
            results = engine.search_reddit(query, subreddit=category, limit=5)
            all_results.extend(results)
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        unique_results.sort(key=lambda x: x['quantum_relevance'], reverse=True)
        return jsonify({'results': unique_results})
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║      🌟 HAPPY - Quantum Entertainment Search Engine 🌟       ║
    ║                                                               ║
    ║    Powered by Quantum Algorithms + Reddit Intelligence       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print("🚀 Server running on http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()
