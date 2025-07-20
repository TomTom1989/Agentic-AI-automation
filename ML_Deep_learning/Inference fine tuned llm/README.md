# Inference with Fine-Tuned QLoRA Falcon Model for Price Prediction

This directory contains an implementation for running inference using a Falcon-RW-1B large language model that has been fine-tuned with QLoRA (Quantized Low-Rank Adapter) techniques. The script predicts product prices from Amazon product metadata and descriptions using the fine-tuned, quantized model and LoRA adapters.

PS: _As I was limited in terms of CPU power, I ran the code on a Google Colab T4 instance (free tier) and reduced the testing set to a smaller sample for demonstration purposes.

## Overview of Implemented Technique

- **Inference with previous Fine-Tuned LLM (inference_fine_tuned_model.py):**
  - Loads the Falcon-RW-1B model in 4-bit quantized mode along with LoRA adapters for efficient inference.
  - Uses a prompt-based approach to predict prices for curated product items.
  - Evaluates model predictions using the same data handling and visualization modules as in training.

## Workflow Summary

1. **Environment Setup:**
   - Installs all required libraries (transformers, peft, bitsandbytes, etc.).
   - Authenticates with Hugging Face Hub for model access.

2. **Data Preparation:**
   - Loads product data from a JSONL file (e.g., `meta_Appliances.jsonl`), typically stored on Google Drive for Colab usage.
   - Filters and curates items using the `Item` class from the main project.

3. **Model and Adapter Loading:**
   - Loads the Falcon-RW-1B base model in 4-bit quantized mode using `bitsandbytes`.
   - Loads the fine-tuned LoRA adapters from the specified directory.
   - Loads the tokenizer from the adapter directory for consistent prompt formatting.

4. **Prediction and Evaluation:**
   - Defines a prediction function that generates price estimates from model outputs.
   - Evaluates predictions using the `Tester` class, which provides error metrics and 2D visualization of results.

## Dataset Information

- **File:** Typically `meta_Appliances.jsonl` (Amazon Reviews 2023 subset).
- **Note:** The dataset should be downloaded from the [Hugging Face platform](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) and placed in the appropriate location (e.g., Google Drive for Colab).
- **Subset Used:** For demonstration, a curated subset of items is used for inference and evaluation.

## Hugging Face and Dependency Requirements

- **Hugging Face Hub Token:** Required for model and adapter access. Authenticate using `huggingface_hub.login()`.
- **Dependencies:** All required dependencies are listed in the `requirements.txt` file at the project root. Please ensure you install them before running the script.

## Project Highlights

- **Efficient Inference:** Uses 4-bit quantized LLM and LoRA adapters for fast, memory-efficient predictions.
- **Prompt-based Evaluation:** Predicts prices from natural language prompts for each product.
- **Modular and Reproducible:** Integrates with the project's data handling and evaluation modules.
- **Hugging Face Integration:** Leverages open-source tools for model loading and inference.

---

**To run the script:**
1. Download the Amazon Reviews dataset and place a portion in your working directory or Google Drive.
2. Authenticate with Hugging Face Hub using your token.
3. Install all dependencies from `requirements.txt`.
4. Run the script (e.g., in a Colab environment): `python inference_fine_tuned_model.py`.
5. Review the printed evaluation metrics and the generated scatter plot.

For more details, see the code and comments in the script. 