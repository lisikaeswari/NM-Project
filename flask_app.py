from flask import Flask, render_template_string, request
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>News Category Predictor</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .container { 
            background: #f5f5f5; 
            padding: 20px; 
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        textarea { 
            width: 100%; 
            height: 150px; 
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background: #0066cc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #0052a3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e8f4ff;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>News Category Predictor</h1>
        <form method="POST">
            <textarea name="text" placeholder="Enter your news article here...">{{text}}</textarea>
            <br>
            <button type="submit">Predict Category</button>
        </form>
        {% if prediction %}
        <div class="result">
            <h3>Predicted Category: {{prediction}}</h3>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def create_dummy_model():
    # Create simple dummy data
    texts = [
        "Technology news about the latest gadgets",
        "Sports update from the recent match",
        "Business report on stock market"
    ]
    labels = ['Technology', 'Sports', 'Business']
    
    # Create and fit vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    
    # Create and fit model
    model = LogisticRegression()
    model.fit(X, labels)
    
    return model, vectorizer

# Create dummy model
model, vectorizer = create_dummy_model()

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    text = ''
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            # Transform the input text
            X = vectorizer.transform([text])
            # Get prediction
            prediction = model.predict(X)[0]
    
    return render_template_string(HTML_TEMPLATE, prediction=prediction, text=text)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
