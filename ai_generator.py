from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict
import re
import textwrap

# Load environment variables
load_dotenv()

# Get OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_blog_post(keyword: str, seo_data: Dict) -> str:
    """
    Generates a blog post using OpenAI's API based on the keyword and SEO data.
    Includes placeholder affiliate links and a structured format.
    """
    related_keywords = ', '.join(seo_data.get('related_keywords', [])[:3])
    search_volume = seo_data.get('search_volume', 'N/A')
    keyword_difficulty = seo_data.get('keyword_difficulty', 'N/A')

    prompt = f"""
    Write a comprehensive, SEO-optimized blog post about '{keyword}' with the following structure:

    1. Engaging title (include the keyword)
    2. Introduction paragraph (hook the reader)
    3. Benefits/Features section (3-5 items)
    4. Comparison section (if applicable)
    5. Buying guide section
    6. Conclusion

    SEO Considerations:
    - Search volume: {search_volume}
    - Keyword difficulty: {keyword_difficulty}
    - Related keywords: {related_keywords}

    Include 3-5 placeholder affiliate links marked as {{AFF_LINK_1}}, {{AFF_LINK_2}}, etc.
    Write in a professional, informative tone for an educated audience.
    Return the content in Markdown format.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional content writer specializing in SEO-optimized blog posts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        content = response.choices[0].message.content

        # Replace placeholders like {AFF_LINK_1} with dummy affiliate URLs
        placeholders = set(re.findall(r"\{AFF_LINK_(\d+)\}", content))
        for ph in placeholders:
            dummy_url = f"https://example.com/affiliate/{keyword.replace(' ', '-')}-{ph}"
            content = content.replace(f"{{AFF_LINK_{ph}}}", dummy_url)

        return textwrap.dedent(content).strip()

    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")
