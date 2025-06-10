from flask import Flask, request, jsonify
from seo_fetcher import get_seo_data
from ai_generator import generate_blog_post
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_post():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword parameter is required'}), 400
    
    try:
        # Get SEO data
        seo_data = get_seo_data(keyword)
        
        # Generate blog post
        blog_post = generate_blog_post(keyword, seo_data)
        
        return jsonify({
            'keyword': keyword,
            'seo_data': seo_data,
            'blog_post': blog_post
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)