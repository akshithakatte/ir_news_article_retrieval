import json
import os
import re

def fix_json_v3():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    print(f"Reading JSON file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, let's try to parse it normally
    try:
        articles = json.loads(content)
        print(f"JSON parsed successfully. Found {len(articles)} articles")
        return
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {str(e)}")
    
    # If that fails, let's try to fix it
    print("Attempting to fix JSON format...")
    
    # Find all article blocks using regex
    article_pattern = r'{[^}]+}'
    article_matches = re.finditer(article_pattern, content)
    
    articles = []
    for match in article_matches:
        article_str = match.group(0)
        
        # Extract fields using regex
        link_match = re.search(r'"link":\s*"([^"]+)"', article_str)
        headline_match = re.search(r'"headline":\s*"([^"]+)"', article_str)
        category_match = re.search(r'"category":\s*"([^"]+)"', article_str)
        desc_match = re.search(r'"short_description":\s*"([^"]+)"', article_str)
        authors_match = re.search(r'"authors":\s*"([^"]*)"', article_str)
        date_match = re.search(r'"date":\s*"([^"]+)"', article_str)
        
        if all([link_match, headline_match, category_match, desc_match, date_match]):
            article = {
                "link": link_match.group(1),
                "headline": headline_match.group(1),
                "category": category_match.group(1),
                "short_description": desc_match.group(1),
                "authors": authors_match.group(1) if authors_match else "",
                "date": date_match.group(1)
            }
            articles.append(article)
    
    print(f"Found {len(articles)} articles")
    
    if articles:
        # Write the properly formatted JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        print("JSON file has been reformatted and saved")
    else:
        print("No valid articles found. Please check the JSON file format.")

if __name__ == "__main__":
    fix_json_v3()
