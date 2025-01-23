import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import string

class NewsIRSystem:
    def __init__(self):
        """Initialize the News IR System"""
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('omw-1.4')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=10000,  # Increased from 5000
            max_df=0.85,  # Decreased from 0.95 to remove more common terms
            min_df=1,  # Changed from 2 to keep rare but potentially important terms
            ngram_range=(1, 2)  # Added bigrams for better context
        )
        self.documents = []
        self.headlines = []
        self.categories = []
        self.descriptions = []
        self.dates = []
        self.links = []
        self.tfidf_matrix = None
        
    def preprocess_text(self, text):
        """Clean and preprocess the text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens if t not in self.stop_words]
        
        # Remove very short tokens and numbers
        tokens = [t for t in tokens if len(t) > 2 and not t.isnumeric()]
        
        return ' '.join(tokens)
    
    def load_articles_from_json(self, json_path):
        """Load articles from JSON file"""
        print(f"Loading articles from: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"Found {len(articles)} articles")
        
        for article in articles:
            # Combine headline and description with different weights
            headline = article['headline'] + " " + article['headline']  # Duplicate headline for more weight
            description = article['short_description']
            category = article['category']
            full_text = f"{headline} {description} {category}"
            
            self.documents.append(self.preprocess_text(full_text))
            self.headlines.append(article['headline'])
            self.categories.append(article['category'])
            self.descriptions.append(article['short_description'])
            self.dates.append(article['date'])
            self.links.append(article['link'])
        
        print(f"Loaded {len(self.documents)} articles")
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        print(f"Created TF-IDF matrix with shape: {self.tfidf_matrix.shape}")
    
    def search(self, query, top_k=5):
        """
        Search for articles based on the query
        Args:
            query (str): Search query
            top_k (int): Number of top results to return
        Returns:
            list: List of (document_index, similarity_score) tuples
        """
        # Preprocess query
        processed_query = self.preprocess_text(query)
        
        # Transform query to TF-IDF space
        query_vector = self.vectorizer.transform([processed_query])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Get top-k documents with scores above threshold
        threshold = 0.01  # Minimum similarity score
        top_indices = np.argsort(similarity_scores)[::-1]
        
        # Filter results above threshold
        results = []
        for idx in top_indices:
            if similarity_scores[idx] >= threshold:
                results.append((idx, similarity_scores[idx]))
            if len(results) >= top_k:
                break
        
        return results

def main():
    # Initialize the IR system
    ir_system = NewsIRSystem()
    
    # Get the absolute path to the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    
    # Load articles from JSON
    ir_system.load_articles_from_json(json_path)
    
    print("News IR System")
    print("-" * 50)
    print("Enter your search query (or 'quit' to exit)")
    
    while True:
        # Get query from user
        query = input("\nEnter your query: ").strip()
        
        if query.lower() == 'quit':
            break
        
        if not query:
            print("Please enter a valid query")
            continue
        
        # Get the most relevant documents
        results = ir_system.search(query, top_k=5)
        
        if not results:
            print("No relevant articles found.")
            continue
        
        # Display the most relevant articles
        print("\nSearch Results:")
        for i, (idx, score) in enumerate(results, 1):
            print(f"\n{i}. {ir_system.headlines[idx]}")
            print(f"   {ir_system.descriptions[idx]}")
            print(f"   Category: {ir_system.categories[idx]}")
            print(f"   Date: {ir_system.dates[idx]}")
            print(f"   Relevance Score: {score:.4f}")
            print(f"   Link: {ir_system.links[idx]}")

if __name__ == "__main__":
    main()
