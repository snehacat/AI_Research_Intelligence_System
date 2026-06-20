"""
OpenAI API Client
Used for paraphrasing, research suggestions, academic writing improvement
"""

import openai
import os
import json
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)


class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI Client
        """

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            logging.warning(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        else:
            openai.api_key = self.api_key

        self.model = "gpt-3.5-turbo"
        self.timeout = 30

    def is_configured(self) -> bool:
        """Check whether API key exists"""
        return bool(self.api_key)

    # ---------------------------------------------------------
    # Core Chat Request Function
    # ---------------------------------------------------------

    def _chat_request(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.5,
    ) -> str:
        """
        Centralized function to send request to OpenAI
        """

        if not self.is_configured():
            raise RuntimeError("OpenAI API key not configured")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                request_timeout=self.timeout,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logging.error(f"OpenAI API request failed: {e}")
            raise

    # ---------------------------------------------------------
    # Paraphrasing
    # ---------------------------------------------------------

    def paraphrase_text(self, text: str, academic_style: bool = True) -> str:
        if not self.is_configured():
            return "OpenAI API key not configured"

        style = (
            "Maintain formal academic tone."
            if academic_style
            else "Use simple language."
        )

        prompt = f"""
Paraphrase the following text while preserving its meaning.
{style}

Text:
{text}
"""

        try:
            return self._chat_request(
                "You are an expert academic paraphrasing assistant.",
                prompt,
                temperature=0.7,
            )
        except Exception as e:
            return f"Error paraphrasing text: {e}"

    # ---------------------------------------------------------
    # Academic Writing Improvement
    # ---------------------------------------------------------

    def improve_academic_writing(self, text: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {"error": "OpenAI API key not configured"}

        prompt = f"""
Analyze the academic writing quality of the following text.

Return result in JSON format:

{{
"academic_tone_score":1-10,
"clarity_score":1-10,
"grammar_score":1-10,
"overall_score":1-10,
"strengths":[...],
"improvements":[...]
}}

Text:
{text}
"""

        try:
            result = self._chat_request(
                "You are an academic editor returning structured JSON analysis.",
                prompt,
                temperature=0.3,
            )

            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"analysis": result}

        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    # ---------------------------------------------------------
    # Research Suggestions
    # ---------------------------------------------------------

    def generate_research_suggestions(
        self, topic: str, field: str = "computer science"
    ) -> Dict[str, Any]:
        if not self.is_configured():
            return {"error": "OpenAI API key not configured"}

        prompt = f"""
Generate research suggestions for topic: {topic}
Field: {field}

Return JSON:

{{
"research_gaps":[],
"methodology":[],
"datasets":[],
"future_directions":[]
}}
"""

        try:
            result = self._chat_request(
                "You are an expert research advisor.", prompt
            )

            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"suggestions": result}

        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    # ---------------------------------------------------------
    # Plagiarism Risk Check
    # ---------------------------------------------------------

    def check_plagiarism_risk(self, text: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {"error": "OpenAI API key not configured"}

        prompt = f"""
Analyze plagiarism risk of the following text.

Return JSON:

{{
"risk_score":1-10,
"risk_factors":[],
"recommendations":[]
}}

Text:
{text}
"""

        try:
            result = self._chat_request(
                "You are an academic integrity expert.", prompt, temperature=0.3
            )

            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"analysis": result}

        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    # ---------------------------------------------------------
    # Citation Suggestions
    # ---------------------------------------------------------

    def generate_citation_suggestions(
        self, text: str, citation_style: str = "APA"
    ) -> str:
        if not self.is_configured():
            return "OpenAI API key not configured"

        prompt = f"""
Suggest where citations should be added in the following text.

Citation Style: {citation_style}

Text:
{text}
"""

        try:
            return self._chat_request(
                f"You are an academic citation expert specialized in {citation_style} style.",
                prompt,
            )

        except Exception as e:
            logging.error(e)
            return f"Error generating citation suggestions: {e}"


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------


def test_openai():
    client = OpenAIClient()

    if not client.is_configured():
        print("OpenAI API key not configured.")
        return

    print("Testing paraphrasing...\n")

    text = "Machine learning algorithms have significantly improved data analysis capabilities."

    result = client.paraphrase_text(text)

    print("Original:", text)
    print("Paraphrased:", result)


if __name__ == "__main__":
    test_openai()
