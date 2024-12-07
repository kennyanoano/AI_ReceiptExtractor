#opneAIとのやり取りの部分
import base64
import json
import os
from openai import OpenAI

SYSTEM_ROLE_CONTENT = "このシステムは提供された画像の内容の説明を生成します。画像を識別し視覚情報をテキスト形式で提供します。"

def ensure_settings_file():
    """設定ファイルが存在しない場合、デフォルト設定で作成する"""
    if not os.path.exists("settings.json"):
        default_settings = {
            "language": "ja",
            "theme": "light",
            # 他のデフォルト設定をここに追加
        }
        with open("settings.json", "w", encoding='utf-8') as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)
        return default_settings
    
    try:
        with open("settings.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("settings.jsonの形式が正しくありません。")

def save_settings(settings):
    """設定を保存する"""
    with open("settings.json", "w", encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def get_gpt_openai_apikey():
    try:
        if not os.path.exists("secret.json"):
            raise FileNotFoundError("secret.jsonファイルが見つかりません。APIキーを設定してください。")
            
        with open("secret.json") as f:
            secret = json.load(f)
            
        if "OPENAI_API_KEY" not in secret:
            raise KeyError("secret.jsonにOPENAI_API_KEYが設定されていません。")
            
        return secret["OPENAI_API_KEY"]
    except json.JSONDecodeError:
        raise ValueError("secret.jsonの形式が正しくありません。")

def create_secret_file(api_key):
    """APIキーを保存するための関数"""
    with open("secret.json", "w") as f:
        json.dump({"OPENAI_API_KEY": api_key}, f, indent=4)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"

def create_message(system_role, prompt, image_base64):
    message = [
        {
            'role': 'system',
            'content': system_role
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': image_base64
                    }
                },
            ]
        },
    ]
    return message

def gen_chat_response_with_gpt4(image_path, api_key, prompt_template):
    openai_client = OpenAI(api_key=api_key)
    image_base64 = encode_image(image_path)
    messages = create_message(SYSTEM_ROLE_CONTENT, prompt_template, image_base64)

    response = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        temperature=0,
    )

    if response and response.choices:
        extracted_data = response.choices[0].message.content
    else:
        extracted_data = "No data extracted"

    #return extracted_data, account_name
    return extracted_data