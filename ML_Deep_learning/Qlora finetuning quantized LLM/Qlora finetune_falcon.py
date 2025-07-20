# !pip install -q bitsandbytes accelerate transformers datasets peft trl scipy scikit-learn

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset, Dataset
import json
import os


from google.colab import drive
drive.mount('/content/drive')

DATA_PATH = "/content/drive/MyDrive/meta_Appliances.jsonl"

with open(DATA_PATH, 'r') as f:
    data = [json.loads(line) for line in f]

# Prompt-template based dataset preparation
def format_example(example):
    return {
        "text": f"What is the price of this item: {example['description']}\nAnswer: {example['price']}"
    }

formatted_data = [format_example(item) for item in data]


formatted_data = formatted_data[:1000]

dataset = Dataset.from_list(formatted_data)
train_test = dataset.train_test_split(test_size=0.1, seed=42)

from huggingface_hub import login
login("Hugginface Token")


MODEL_ID = "tiiuae/falcon-rw-1b"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)

# Load model in 4-bit (QLoRA setup)
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto"
)

model = prepare_model_for_kbit_training(model)

from peft import LoraConfig, get_peft_model # Import get_peft_model

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["query_key_value", "dense"] # Target the correct layer names for Falcon
)

model = get_peft_model(model, lora_config)

from transformers import TrainingArguments  
from trl import SFTTrainer

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=1,
    learning_rate=2e-4,
    save_strategy="epoch",
    logging_steps=20,
    fp16=True,
    save_total_limit=2,
    push_to_hub=False
)

from peft import get_peft_model # Import get_peft_model

# Re-apply get_peft_model to ensure the model has the PEFT adapters
model = get_peft_model(model, lora_config)

trainer = SFTTrainer(
    model=model,
    train_dataset=train_test['train'],
    args=training_args,
)

trainer.train()

model.save_pretrained("./falcon-price-regression")
tokenizer.save_pretrained("./falcon-price-regression")