from typing import Literal
import json
import uuid

from requests import Response, post

from ..core.config import settings_dev

PARAMS:  dict[str, str | list[str]] = {
    'api-version': '3.0',
    'from':'fil',
    'to':['en']
}

HEADERS: dict[str, str] = {
    'Ocp-Apim-Subscription-Key': settings_dev.azure_translate_key,
    'Ocp-Apim-Subscription-Region': settings_dev.azure_translate_location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def translator_tool(query: str) -> str:
    json_body: list[dict[str, str]] = [{'text':query}]
    # request_post = requests.post(
    request_post: Response = post(
        url=settings_dev.azure_translate_url,
        params=PARAMS, 
        headers=HEADERS, 
        json=json_body
    )
    
    json_request_post = request_post.json()
    
    return json.dumps(
        json_request_post,
        sort_keys=True,
        ensure_ascii=False,
        indent=4,
        separators=(',', ': ')
    )



LANGUAGES = Literal["en","fil"]
    
def translator_tool_v1(
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

