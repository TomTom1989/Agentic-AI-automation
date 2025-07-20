# ML_Deep_Learning: Product Price Prediction with Machine Learning and LLMs

This project explores a range of machine learning and large language model (LLM) techniques for predicting product prices based on Amazon product metadata and descriptions. It demonstrates the evolution from traditional ML algorithms to state-of-the-art LLMs, including both closed-source and open-source, quantized, and fine-tuned models.

## Project Structure

- **Traditional ML techniques/**
  - Implements classic regression models (Linear Regression, Random Forest, SVR, Word2Vec-based regression) using scikit-learn.
  - Uses Bag-of-Words and word embedding features for price prediction.
  - Includes scripts, modular data handling, and 2D result visualizations.

- **Frontier llm closed source model/**
  - Uses OpenAI's GPT-4o-mini (closed-source LLM) via API for zero-shot price prediction.
  - Requires an OpenAI API key and internet access.
  - Integrates with the same data and evaluation pipeline as other approaches.

- **Qlora finetuning quantized LLM/**
  - Demonstrates parameter-efficient finetuning of the Falcon-RW-1B model using QLoRA (Quantized Low-Rank Adapter) techniques.
  - Loads the model in 4-bit quantized mode for efficient training on limited hardware (e.g., Google Colab T4 free tier).
  - Uses a prompt-based, supervised approach and saves the fine-tuned model and tokenizer.

- **Inference fine tuned llm/**
  - Runs inference using the QLoRA-finetuned Falcon model and LoRA adapters.
  - Loads the quantized model and adapters, predicts prices, and evaluates results with visualization.

- **data/**
  - Contains `meta_Appliances.jsonl`, a (potentially large) subset of the Amazon Reviews 2023 dataset. The file is empty in this repo due to size; download from [Hugging Face](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023).

- **items.py, loaders.py, testing.py, text_vectorizers.py**
  - Shared modules for data cleaning, loading, evaluation, and feature extraction.

## Dataset

- **Source:** [Amazon Reviews 2023 (Hugging Face)](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
- **Usage:** For performance and demonstration, only a small subset (e.g., 200–1,000 rows) is used in most scripts.
- **Note:** Place your data file in `data/meta_Appliances.jsonl` or the appropriate Colab/Drive path.

## Key Features & Highlights

- **Modular Design:** Reusable code for data handling, feature extraction, modeling, and evaluation.
- **Multiple Approaches:** Compare traditional ML, closed-source LLMs, and open-source, quantized, fine-tuned LLMs.
- **Efficient Training & Inference:** QLoRA and 4-bit quantization enable experimentation on limited hardware (e.g., Colab T4 free tier).
- **Prompt-based Supervision:** LLMs are trained and evaluated using natural language prompts.
- **Visualization:** All approaches include 2D scatter plots for intuitive performance analysis.
- **Reproducibility:** Fixed random seeds and clear data splits.

## Requirements

- All dependencies are listed in `requirements.txt` at the project root. Install with:
  ```bash
  pip install -r requirements.txt
  ```
- For LLM approaches, you may need API keys (OpenAI) or Hugging Face tokens.
- Some scripts are designed for Google Colab and may require mounting Google Drive.

## Getting Started

1. **Download the Dataset:**
   - Retrieve the Amazon Reviews dataset from Hugging Face and place a subset in `data/meta_Appliances.jsonl`.
2. **Install Dependencies:**
   - `pip install -r requirements.txt`
3. **(Optional) Set Up API Keys:**
   - For GPT-4o-mini, add your OpenAI API key to a `.env` file.
   - For Falcon models, authenticate with Hugging Face Hub.
4. **Run Experiments:**
   - Choose a script from any subfolder and follow its README for instructions.
   - Most scripts can be run in Colab or locally (hardware permitting).

## Notes on Compute

- Some experiments (especially QLoRA finetuning and LLM inference) were run on Google Colab T4 (free tier) due to local CPU/GPU limitations. Training and testing set sizes were reduced for demonstration and resource efficiency.

## References

- [Amazon Reviews 2023 Dataset](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
- [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o)
- [Falcon-RW-1B](https://huggingface.co/tiiuae/falcon-rw-1b)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)

---

For details on each approach, see the README in the corresponding subfolder and the code comments in each script. 