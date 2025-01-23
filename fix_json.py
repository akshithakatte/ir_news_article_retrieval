import json
import os

def fix_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    print(f"Fixing JSON file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any trailing commas before closing brackets
    content = content.replace(',]', ']')
    content = content.replace(',}', '}')
    
    # Remove any extra whitespace
    content = content.strip()
    
    # Ensure the file ends with a single closing bracket
    if not content.endswith(']'):
        content = content.rstrip() + '\n]'
    
    try:
        # Parse the JSON to validate it
        articles = json.loads(content)
        print(f"Successfully fixed JSON")
        print(f"Number of articles: {len(articles)}")
        
        # Write the fixed content back to the file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print("Fixed JSON has been saved")
        
    except json.JSONDecodeError as e:
        print(f"Error fixing JSON: {str(e)}")
        print(f"Error at line {e.lineno}, column {e.colno}")
        print(f"Error message: {e.msg}")
        
        # Show the problematic area
        lines = content.split('\n')
        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 2)
        print("\nContext:")
        for i in range(start, end):
            prefix = "-> " if i == e.lineno - 1 else "   "
            print(f"{prefix}{i+1}: {lines[i]}")

if __name__ == "__main__":
    fix_json()
