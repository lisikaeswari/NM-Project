from flask import Flask, render_template_string, request
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# HTML template with Bootstrap for better styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Indian Express News Search</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .news-item {
            border-left: 4px solid #0d6efd;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <span class="navbar-brand mb-0 h1">Indian Express News Search</span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-3">
                <div class="card">
                    <div class="card-header">
                        Categories
                    </div>
                    <div class="card-body">
                        <form method="GET">
                            <select name="category" class="form-select mb-3" onchange="this.form.submit()">
                                <option value="">Select Category</option>
                                {% for cat in categories %}
                                <option value="{{ cat }}" {% if cat == selected_category %}selected{% endif %}>
                                    {{ cat }}
                                </option>
                                {% endfor %}
                            </select>
                        </form>
                    </div>
                </div>
            </div>

            <div class="col-md-9">
                <form method="GET" class="mb-4">
                    <input type="hidden" name="category" value="{{ selected_category }}">
                    <div class="input-group">
                        <input type="text" name="search" class="form-control" placeholder="Search articles..." 
                               value="{{ search_query }}">
                        <button class="btn btn-primary" type="submit">Search</button>
                    </div>
                </form>

                {% if articles %}
                    <h5>Found {{ articles|length }} articles</h5>
                    {% for article in articles %}
                        <div class="news-item">
                            <h4>{{ article.title }}</h4>
                            <p>{{ article.content[:300] }}...</p>
                            <small class="text-muted">Date: {{ article.date if article.date else 'N/A' }}</small>
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="alert alert-info">
                        {% if selected_category %}
                            No articles found. Try a different search term or category.
                        {% else %}
                            Please select a category to view articles.
                        {% endif %}
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

def load_news_data():
    """Load all news datasets"""
    data_files = {
        'Business': 'business_data.csv',
        'Education': 'education_data.csv',
        'Entertainment': 'entertainment_data.csv',
        'Sports': 'sports_data.csv',
        'Technology': 'technology_data.csv'
    }
    
    datasets = {}
    for category, filename in data_files.items():
        try:
            file_path = Path(filename)
            if file_path.exists():
                df = pd.read_csv(file_path)
                datasets[category] = df.to_dict('records')
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            # Create dummy data if file doesn't exist
            datasets[category] = [
                {
                    'title': f'Sample {category} Article 1',
                    'content': f'This is a sample {category.lower()} article content for demonstration.',
                    'date': '2024-05-06'
                }
            ]
    
    return datasets

# Load data once at startup
NEWS_DATA = load_news_data()

@app.route('/')
def home():
    # Get query parameters
    category = request.args.get('category', '')
    search_query = request.args.get('search', '').lower()
    
    # Get articles for selected category
    articles = NEWS_DATA.get(category, []) if category else []
    
    # Filter by search query if provided
    if search_query and articles:
        articles = [
            article for article in articles
            if search_query in article['title'].lower() or 
               search_query in article['content'].lower()
        ]
    
    return render_template_string(
        HTML_TEMPLATE,
        categories=list(NEWS_DATA.keys()),
        selected_category=category,
        search_query=search_query,
        articles=articles
    )

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
