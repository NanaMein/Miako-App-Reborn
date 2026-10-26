from typing import Literal

from requests import post

from ..core.config import settings_dev

LANGUAGES = Literal["en","fil"]
    
def translator_tool(
    query: str, 
    input_lang: LANGUAGES = "fil", 
    output_lang: LANGUAGES = "en"
):
    targets = [
        {
            "language": output_lang,
            "deploymentName": settings_dev.azure_translator_deployment_name, 
            "gender": "female"
        }
    ]
    def _translate_text(text, targets, source_language):
        body = {
            "inputs": [
                {
                    "Text": text,
                    "language": source_language,
                    "targets": targets
                }
            ]
        }
    
        response = post(
            url=settings_dev.azure_translator_url, 
            headers=settings_dev.azure_translator_headers, 
            json=body
        )
        response.raise_for_status()
        return response.json()
    try:
        result = _translate_text(query, targets, input_lang)
        translations = result["value"][0]["translations"]
        if translations:
            return translations[0]["text"]
        return None
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

