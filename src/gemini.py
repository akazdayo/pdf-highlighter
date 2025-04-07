from google import genai
from google.genai import types
import pathlib
import httpx
from pypdf import PdfReader
import json


def analyze_text(path):
    # PDFファイルの読み込み
    reader = PdfReader(path)

    # ページの取得。この場合は、1ページ目を取得する。
    page = reader.pages[25]

    # テキストの抽出
    text = page.extract_text()
    print(text)
    return text


client = genai.Client()
# Retrieve and encode the PDF byte


def get_pdf_text(filepath):
    prompt = analyze_text(filepath)
    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25",
        config=types.GenerateContentConfig(
            system_instruction="""
            あなたはこの文章を読む人のために、危ないところや読み飛ばしいそうなところ・重要そうなところを強調します。
            あなたは、この文章をハイライトしてあげる教師です。
            あなたはjsonの形式で絶対に次のように出力すること
            ```json
            {
                texts: [
                    {
                        "text": "重要な部分をハイライトした文章", // これは、生の文章にしてください。完全一致検索をします。省略はしないでください。15文字程度の部分をハイライトしてください。
                        "reason": "なぜその部分が重要なのか" // 種類("caution/tricky", "important", "easy-to-miss")
                        "comment": "あなたの意見や感想"
                    },
                    ...
                ]
            }
            ```
            """,
            temperature=0,
        ),
        contents=[prompt],
    )
    text = response.text.replace("```json", "")
    text = text.replace("```", "")
    print(text)
    result = json.loads(text)
    return result


if __name__ == "__main__":
    filepath = pathlib.Path("discovery.pdf")
    result = get_pdf_text(filepath)
    a = []
    for text in result["texts"]:
        a.append(text["text"])
    print(a)
