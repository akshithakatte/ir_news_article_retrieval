import json
import os

def validate_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    print(f"Validating JSON file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"File size: {len(content)} bytes")
        
        try:
            articles = json.loads(content)
            print(f"Successfully parsed JSON")
            print(f"Number of articles: {len(articles)}")
            
            # Print first and last few articles
            print("\nFirst 2 articles:")
            for i, article in enumerate(articles[:2]):
                print(f"{i+1}. {article['headline']}")
            
            print("\nLast 2 articles:")
            for i, article in enumerate(articles[-2:]):
                print(f"{len(articles)-1+i}. {article['headline']}")
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            # Print the problematic area
            line_no = e.lineno
            col_no = e.colno
            print(f"\nError at line {line_no}, column {col_no}")
            
            # Show the problematic line and surrounding context
            lines = content.split('\n')
            start = max(0, line_no - 2)
            end = min(len(lines), line_no + 2)
            print("\nContext:")
            for i in range(start, end):
                prefix = "-> " if i == line_no - 1 else "   "
                print(f"{prefix}{i+1}: {lines[i]}")

if __name__ == "__main__":
    validate_json()
