import json
from anthropic import Anthropic
from app.core.config import settings
from typing import Optional, List


class AIService:
    def __init__(self):
        self.client = Anthropic()
        self.model = settings.DEFAULT_AI_MODEL

    def summarize_article(self, title: str, content: str) -> str:
        """Generate a concise, high-quality summary of an article."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a knowledge curator focused on continuous learning and intellectual growth.
Summarize the following article in 2-3 sentences, emphasizing the most important insights and learnings.
Focus on knowledge value, avoid gossip or superficial information.

Title: {title}

Content: {content}

Provide a concise, insightful summary."""
                }
            ]
        )
        return message.content[0].text

    def detect_contradictions(self, articles: List[dict]) -> Optional[dict]:
        """Detect contradictions across multiple sources reporting the same story."""
        if len(articles) < 2:
            return None

        articles_text = "\n\n".join(
            [f"Source: {a.get('source', 'Unknown')}\nContent: {a.get('content', '')}" for a in articles]
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze the following articles about the same topic from different sources and identify any contradictions or conflicting claims.

{articles_text}

If contradictions exist, list them in JSON format with the following structure:
{{
    "has_contradictions": true/false,
    "contradictions": [
        {{
            "claim_a": "Source A says...",
            "claim_b": "Source B says...",
            "conflict_description": "The contradiction is..."
        }}
    ]
}}

If no contradictions, return {{"has_contradictions": false}}"""
                }
            ]
        )

        try:
            return json.loads(message.content[0].text)
        except json.JSONDecodeError:
            return None

    def assess_content_quality(self, title: str, content: str) -> bool:
        """Assess if content is high-quality and knowledge-focused (not gossip)."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": f"""Rate if this article contains valuable knowledge/learning content vs gossip/low-value content.
Only respond with 'HIGH' or 'LOW'.

Title: {title}
Content: {content}"""
                }
            ]
        )
        response = message.content[0].text.strip().upper()
        return response == "HIGH"

    def batch_summarize(self, articles: List[dict]) -> dict:
        """Summarize multiple articles efficiently."""
        summaries = {}
        for article in articles:
            try:
                summary = self.summarize_article(article["title"], article["content"])
                summaries[article["id"]] = summary
            except Exception as e:
                print(f"Error summarizing article {article.get('id')}: {e}")
                summaries[article["id"]] = None

        return summaries
