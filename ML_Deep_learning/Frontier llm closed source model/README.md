# Frontier LLM (Closed Source) Price Prediction

This directory contains an implementation of a price prediction pipeline using a closed-source, frontier large language model (LLM) from OpenAI (GPT-4o-mini). The model leverages advanced generative AI capabilities to estimate product prices based on Amazon product metadata and descriptions.

## Overview of Implemented Technique

- **Frontier LLM Regression (frontier_llm_model.py):**
  - Uses the GPT-4o-mini model via the OpenAI API to predict product prices from text descriptions.
  - Sends a prompt containing the product description to the LLM and extracts the predicted price from the model's response.
  - Designed for realistic price estimation using state-of-the-art language understanding.
  - Relies on supporting modules: `items.py` (for data structure), `loaders.py` (for data loading), and `testing.py` (for evaluation and visualization).

## Supporting Modules

- **`items.py`:** Defines the `Item` class, which represents a cleaned and curated product datapoint, including text processing and prompt generation for LLM input.
- **`loaders.py`:** Handles efficient loading, filtering, and parallel processing of the dataset. Only a portion of the dataset (first 200 rows) is loaded for performance reasons.
- **`testing.py`:** Provides the `Tester` class for model evaluation, error reporting, and 2D visualization of predicted vs. actual prices.

## Dataset Information

- **File:** `data/meta_Appliances.jsonl`
- **Note:** This file is empty in the repository due to its large size. You can retrieve the full dataset from the [Hugging Face platform](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023).
- **Subset Used:** For performance and demonstration purposes, only a small portion (first 200 rows) of the dataset is used for prediction and evaluation.

## Data Splitting

- **Evaluation:** The script evaluates the LLM's predictions on the loaded dataset. (No explicit training phase, as the LLM is used in a zero-shot/few-shot manner.)

## API and Environment Requirements

- **OpenAI API Key:** You must provide a valid OpenAI API key in a `.env` file as `OPENAI_API_KEY` to use the GPT-4o-mini model.
- **Dependencies:** All required dependencies are listed in the `requirements.txt` file at the project root. Please ensure you install them before running the script.

## Visualization

- After evaluation, the script produces a 2D scatter plot visualizing the relationship between the ground truth prices and the LLM's predictions, helping to assess model accuracy and error distribution.

## Project Highlights

- **State-of-the-Art LLM:** Utilizes a cutting-edge, closed-source language model for regression tasks.
- **Modular Design:** Integrates seamlessly with the project's data handling and evaluation modules.
- **No Training Required:** Leverages the LLM's pre-trained knowledge for immediate predictions.
- **Reproducibility:** Consistent evaluation pipeline and fixed dataset subset.
- **Visualization:** Built-in 2D plots for intuitive model performance analysis.

---

**To run the model:**
1. Download the Amazon Reviews dataset and place a portion in `data/meta_Appliances.jsonl`.
2. Add your OpenAI API key to a `.env` file as `OPENAI_API_KEY`.
3. Run the script: `python frontier_llm_model.py`.
4. Review the printed evaluation metrics and the generated scatter plot.

For more details, see the code and comments in the script. 