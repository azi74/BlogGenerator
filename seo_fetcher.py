import random
from typing import Dict

def get_seo_data(keyword: str) -> Dict:
    """
    Mock SEO data fetcher. In a real implementation, this would call an SEO API.
    Returns search volume, keyword difficulty, and average CPC.
    """
    # Mock data generation with some randomness
    return {
        'search_volume': random.randint(100, 10000),
        'keyword_difficulty': random.randint(1, 100),
        'avg_cpc': round(random.uniform(0.1, 10.0), 2),
        'related_keywords': [
            f"{keyword} reviews",
            f"best {keyword}",
            f"buy {keyword} online",
            f"{keyword} vs competitor"
        ]
    }