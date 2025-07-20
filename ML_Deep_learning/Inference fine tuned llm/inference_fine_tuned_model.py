# === Install required libraries ===
#!pip install -q bitsandbytes accelerate transformers datasets peft trl scipy scikit-learn
!pip install -q bitsandbytes accelerate transformers datasets peft trl scipy scikit-learn

# === 2. Hugging Face Login (for gated Falcon model) ===
from huggingface_hub import login
import os

HF_TOKEN = "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"  # replace if needed
login(HF_TOKEN, add_to_git_credential=True)

# === 3. Imports ===
from items import Item
from testing import Tester
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from google.colab import drive

# === 4. Mount Google Drive ===
drive.mount('/content/drive')

# === 5. Load JSONL items ===
PATH = "/content/drive/MyDrive/meta_Appliances.jsonl"
items = []

with open(PATH, 'r') as f:
    for line in f:
        obj = json.loads(line)

        price = obj.get('price')
        if price is None:
            print(f"Skipping item with missing price: {obj.get('title', 'Unknown')}")
            continue

        try:
            price = float(price)
        except ValueError:
            print(f"Skipping item with invalid price: {price}")
            continue

        item = Item(obj, price)
        if item.include:
            items.append(item)

print(f"✅ Loaded {len(items)} curated items.")

# === 6. Load Base Falcon + LoRA Adapters ===
MODEL_ID = "tiiuae/falcon-rw-1b"
ADAPTER_PATH = "/content/drive/MyDrive/falcon-price-regression/falcon-price-regression"

import torch
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    token=HF_TOKEN
)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(
    ADAPTER_PATH,
    use_fast=True
)

# === 7. Define prediction function ===
def predict_price(item: Item):
    prompt = item.test_prompt()
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        predicted = float([tok for tok in decoded.split() if '$' in tok or tok.replace('.', '').isdigit()][-1].replace('$', ''))
        if predicted <= 0:
            predicted = 0.01
    except:
        predicted = 0.01

    return predicted

# === 8. Run Evaluation ===
Tester(predict_price, items, title="Falcon QLoRA (Fine-Tuned)", size=250).run()