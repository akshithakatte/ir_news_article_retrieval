import json
import os

def fix_json_v2():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    print(f"Reading JSON file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any trailing commas and extra whitespace
    content = content.strip()
    
    # Extract individual article objects
    articles = []
    lines = content.split('\n')
    current_article = {}
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and brackets
        if not line or line in ['[', ']']:
            continue
            
        # Check if this is the start of a new article
        if line.startswith('{'):
            current_article = {}
        
        # Parse the key-value pair
        if ':' in line:
            # Remove trailing comma if present
            if line.endswith(','):
                line = line[:-1]
                
            # Split into key and value
            key = line.split(':', 1)[0].strip().strip('"')
            value = line.split(':', 1)[1].strip().strip(',').strip()
            
            # Clean up the value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            # Add to current article
            if key in ["link", "headline", "category", "short_description", "authors", "date"]:
                current_article[key] = value
        
        # End of article
        if line.endswith('}'):
            if len(current_article) == 6:  # Make sure we have all fields
                articles.append(current_article)
            current_article = {}
    
    print(f"Found {len(articles)} articles")
    
    # Write the properly formatted JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print("JSON file has been reformatted and saved")

if __name__ == "__main__":
    fix_json_v2()
