import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import json


def search_web(query, num_results=3):
    search_results = []
    
    try:
        search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = soup.find_all('div', class_='result')
        
        for result in results[:num_results]:
            try:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if link and link.startswith('http'):
                        search_results.append({
                            'title': title,
                            'url': link,
                            'snippet': snippet
                        })
            except Exception as e:
                continue
        
        if not search_results:
            try:
                api_url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"
                response = requests.get(api_url, timeout=10)
                data = response.json()
                
                if data.get('AbstractText'):
                    search_results.append({
                        'title': data.get('Heading', 'DuckDuckGo Result'),
                        'url': data.get('AbstractURL', 'https://duckduckgo.com'),
                        'snippet': data.get('AbstractText', '')
                    })
                
                for topic in data.get('RelatedTopics', [])[:2]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        search_results.append({
                            'title': topic.get('Text', '')[:100],
                            'url': topic.get('FirstURL', 'https://duckduckgo.com'),
                            'snippet': topic.get('Text', '')
                        })
            except Exception as e:
                print(f"API fallback error: {e}")
                
    except Exception as e:
        print(f"Web search error: {e}")
    
    return search_results


def extract_web_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:3000]
    except Exception as e:
        return ""


def get_web_context(query):
    search_results = search_web(query)
    
    if not search_results:
        return "", []
    
    web_context = ""
    references = []
    
    for result in search_results:
        snippet = result['snippet']
        content = extract_web_content(result['url'])
        
        if content:
            web_context += f"\n\nFrom {result['title']}:\n{content[:1000]}\n"
        else:
            web_context += f"\n\nFrom {result['title']}:\n{snippet}\n"
        
        references.append({
            'title': result['title'],
            'url': result['url']
        })
    
    return web_context, references
