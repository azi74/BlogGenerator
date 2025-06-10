from flask import Flask, request, jsonify
from flask_cors import CORS
from seo_fetcher import get_seo_data
from ai_generator import generate_blog_post
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Check required environment variable
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing required environment variable: OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_post():
    data = request.get_json()
    keyword = data.get('keyword') if data else None

    if not keyword:
        return jsonify({'error': 'Keyword field is required in JSON body'}), 400

    try:
        app.logger.info(f"Received keyword: {keyword}")

        seo_data = get_seo_data(keyword)
        blog_post = generate_blog_post(keyword, seo_data)

        return jsonify({
            'keyword': keyword,
            'seo_data': seo_data,
            'blog_post': blog_post
        })
    except Exception as e:
        app.logger.error(f"Error generating post: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
