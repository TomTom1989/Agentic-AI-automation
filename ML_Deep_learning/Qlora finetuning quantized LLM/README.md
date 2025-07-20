# QLoRA Finetuning of Quantized LLM for Price Prediction

This directory contains an implementation for finetuning a quantized large language model (LLM) using QLoRA (Quantized Low-Rank Adapter) techniques. The script adapts the Falcon-RW-1B model for product price prediction based on Amazon product metadata and descriptions.

PS: _As I was limited in terms of CPU power, I ran the code on a Google Colab T4 instance (free tier) and reduced the training set to a smaller sample for demonstration purposes.

## Overview of Implemented Technique

- **QLoRA Finetuning (Qlora finetune_falcon.py):**
  - Loads the Falcon-RW-1B model in 4-bit quantized mode for efficient training.
  - Prepares a prompt-based dataset from Amazon product metadata, using a subset of the data for demonstration.
  - Applies QLoRA adapters to the model for parameter-efficient finetuning.
  - Uses Hugging Face's `transformers`, `peft`, and `trl` libraries for model loading, training, and supervision.
  - Saves the finetuned model and tokenizer for downstream inference.

## Workflow Summary

1. **Data Preparation:**
   - Loads product data from a JSONL file (e.g., `meta_Appliances.jsonl`), typically stored on Google Drive for Colab usage.
   - Formats each example into a prompt/response pair for supervised finetuning.
   - Uses a subset (e.g., 1,000 examples) for quick experimentation.
   - Splits the data into training and test sets (90%/10%).

2. **Model Loading and Quantization:**
   - Loads the Falcon-RW-1B model from Hugging Face in 4-bit quantized mode using `bitsandbytes` for memory efficiency.
   - Prepares the model for k-bit (quantized) training.

3. **QLoRA Adapter Application:**
   - Configures and applies LoRA adapters to the model for parameter-efficient finetuning.

4. **Training:**
   - Sets up training arguments (batch size, epochs, learning rate, etc.).
   - Trains the model using Hugging Face's `SFTTrainer` for supervised fine-tuning.

5. **Saving Artifacts:**
   - Saves the finetuned model and tokenizer for later use.

## Dataset Information

- **File:** Typically `meta_Appliances.jsonl` (Amazon Reviews 2023 subset).
- **Note:** The dataset should be downloaded from the [Hugging Face platform](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) and placed in the appropriate location (e.g., Google Drive for Colab).
- **Subset Used:** For demonstration, a small portion (e.g., 1,000 rows) is used for finetuning and evaluation.

## Hugging Face and API Requirements

- **Hugging Face Hub Token:** Required for model and dataset access. Authenticate using `huggingface_hub.login()`.
- **Dependencies:** All required dependencies are listed in the `requirements.txt` file at the project root. Please ensure you install them before running the script.

## Project Highlights

- **Efficient Finetuning:** Uses QLoRA and 4-bit quantization for memory- and compute-efficient LLM adaptation.
- **Prompt-based Supervision:** Trains the model to predict prices from natural language prompts.
- **Modular and Reproducible:** Clear workflow for data preparation, model loading, training, and saving.
- **Hugging Face Integration:** Leverages the latest open-source tools for LLM finetuning.



**To run the script:**
1. Download the Amazon Reviews dataset and place a portion in your working directory or Google Drive.
2. Authenticate with Hugging Face Hub using your token.
3. Install all dependencies from `requirements.txt`.
4. Run the script (e.g., in a Colab environment): `python Qlora finetune_falcon.py`.
5. The finetuned model and tokenizer will be saved for later inference.

For more details, see the code and comments in the script. 