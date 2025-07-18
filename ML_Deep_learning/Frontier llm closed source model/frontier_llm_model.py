from loaders import ItemLoader
from testing import Tester
from dotenv import load_dotenv
import os
import re
import openai

# === Load .env ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# === Create new client ===
client = openai.OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"

# === Price extraction helper ===
def extract_price_from_response(text):
    match = re.search(r"(\d+\.\d{2})", text)
    if match:
        return float(match.group(1))
    match = re.search(r"(\d+)", text)
    if match:
        return float(match.group(1))
    return 0.0

# === Prediction using GPT-4o ===
def gpt_predict(item):
    prompt = (
        f"Estimate the realistic price in USD of the following product. "
        f"Return only a number with two decimals.\n\n"
        f"Product description:\n{item.test_prompt()}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.3,
        )
        reply = response.choices[0].message.content.strip()
        return extract_price_from_response(reply)

    except Exception as e:
        snippet = item.test_prompt()[:50].replace("\n", " ")
        print(f"Error for item: \"{snippet}...\": {e}")
        return 0.0

def main():
    print("Loading items...")
    loader = ItemLoader("Appliances")
    items = loader.load()

    if len(items) < 10:
        print("Not enough items to test.")
        return

    print(f"{len(items)} items loaded.")

    print("Evaluating using GPT-4o-mini...")
    tester = Tester(gpt_predict, items, title="GPT-4o-mini", size=len(items))
    tester.run()

if __name__ == "__main__":
    main()
