import json

import openai

from utils.image_utils import encode_image_to_base64


def form_question_vision_analyzer_tool(description: str, expected_output: str, image_path: str) -> str:
    """Analyzes a base64-encoded screenshot of a Google Form question and returns structured JSON.

    Args:
        description: Task description in the current language
        expected_output: Expected output in current language
        image_path: Path to the image file to analyze

    Returns: Analysis results as a JSON string

    """
    try:
        base64_image = encode_image_to_base64(image_path)

        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": description},
                        {"type": "text", "text": expected_output},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=800,
            temperature=0.2,
        )
        result = response.choices[0].message.content.strip()

        # Validate JSON before returning
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Try to extract JSON from the response if it's wrapped in markdown
            if "```json" in result:
                json_start = result.find("```json") + 7
                json_end = result.find("```", json_start)
                if json_end != -1:
                    result = result[json_start:json_end].strip()

            # Validate again
            json.loads(result)
            return result

    except json.JSONDecodeError as e:
        return json.dumps({"error": "Invalid JSON in response", "details": str(e), "confidence": 0.0})
    except FileNotFoundError as e:
        return json.dumps({"error": "Image file not found", "details": str(e), "confidence": 0.0})
    except openai.OpenAIError as e:
        return json.dumps({"error": "OpenAI API error", "details": str(e), "confidence": 0.0})
    except Exception as e:
        return json.dumps({"error": "Unexpected error during analysis", "details": str(e), "confidence": 0.0})
