import json
import os

def fix_json_format():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    print(f"Reading JSON file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any trailing commas and extra whitespace
    content = content.strip()
    
    # Find all article entries by looking for patterns
    articles = []
    current_article = ""
    brace_count = 0
    in_article = False
    
    for char in content:
        if char == '{':
            brace_count += 1
            in_article = True
        elif char == '}':
            brace_count -= 1
            current_article += char
            if brace_count == 0 and in_article:
                try:
                    article_json = json.loads(current_article)
                    articles.append(article_json)
                except json.JSONDecodeError as e:
                    print(f"Error parsing article: {e}")
                    print(f"Problematic JSON: {current_article}")
                current_article = ""
                in_article = False
        elif in_article:
            current_article += char
    
    print(f"Found {len(articles)} articles")
    
    # Write the properly formatted JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print("JSON file has been reformatted and saved")

if __name__ == "__main__":
    fix_json_format()
