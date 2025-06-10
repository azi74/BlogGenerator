import openai
import os
from typing import Dict

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_blog_post(keyword: str, seo_data: Dict) -> str:
    """
    Generates a blog post using OpenAI's API based on the keyword and SEO data.
    Includes placeholder affiliate links and a structured format.
    """
    prompt = f"""
    Write a comprehensive, SEO-optimized blog post about '{keyword}' with the following structure:
    
    1. Engaging title (include the keyword)
    2. Introduction paragraph (hook the reader)
    3. Benefits/Features section (3-5 items)
    4. Comparison section (if applicable)
    5. Buying guide section
    6. Conclusion
    
    SEO Considerations:
    - Search volume: {seo_data['search_volume']}
    - Keyword difficulty: {seo_data['keyword_difficulty']}
    - Related keywords: {', '.join(seo_data['related_keywords'][:3])}
    
    Include 3-5 placeholder affiliate links marked as {{AFF_LINK_1}}, {{AFF_LINK_2}}, etc.
    Write in a professional, informative tone for an educated audience.
    Return the content in Markdown format.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional content writer specializing in SEO-optimized blog posts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        # Replace affiliate link placeholders with dummy URLs
        for i in range(1, 6):
            content = content.replace(
                f"{{AFF_LINK_{i}}}", 
                f"https://example.com/affiliate/{keyword.replace(' ', '-')}-{i}"
            )
        
        return content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")