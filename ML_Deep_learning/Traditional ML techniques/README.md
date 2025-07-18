# Traditional Machine Learning Techniques for Price Prediction

This directory contains implementations of several traditional machine learning models for predicting product prices based on Amazon product reviews and metadata. The models leverage structured data and text features to estimate prices, using a subset of the Amazon Reviews 2023 dataset from HuggingFace platform.

## Overview of Implemented Techniques

- **Linear Regression (linear_model.py):**
  - Uses Bag-of-Words (BoW) features extracted from product descriptions.
  - Implements a simple linear regression model to predict prices.
  - Relies on supporting modules: `items.py` (for data structure), `loaders.py` (for data loading), and `testing.py` (for evaluation and visualization).

- **Random Forest Regression (random_forest_model.py):**
  - Uses BoW features for input.
  - Employs a Random Forest Regressor for robust, non-linear price prediction.
  - Utilizes the same supporting modules as above.

- **Support Vector Regression (svm_model.py):**
  - Uses BoW features.
  - Applies Support Vector Regression (SVR) for price estimation.
  - Integrates with the same data and evaluation pipeline.

- **Linear Regression with Word2Vec Embeddings (word2vec_model.py):**
  - Extracts average word embeddings from product descriptions using pre-trained GloVe vectors (via `gensim`).
  - Trains a linear regression model on these semantic features.

## Supporting Modules

- **`items.py`:** Defines the `Item` class, which represents a cleaned and curated product datapoint, including text processing and prompt generation for ML models.
- **`loaders.py`:** Handles efficient loading, filtering, and parallel processing of the dataset. Only a portion of the dataset (first 200 rows) is loaded for performance reasons.
- **`testing.py`:** Provides the `Tester` class for model evaluation, error reporting, and 2D visualization of predicted vs. actual prices.
- **`text_vectorizers.py`:** (Optional) Contains reusable functions for extracting BoW features from product text.

## Dataset Information

- **File:** `data/meta_Appliances.jsonl`
- **Note:** This file is empty in the repository due to its large size. You can retrieve the full dataset from the [Hugging Face platform](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023).
- **Subset Used:** For performance and demonstration purposes, only a small portion (first 200 rows) of the dataset is used for training and evaluation.

## Data Splitting

- **Training:** 90% of the loaded dataset is used for training the models.
- **Testing:** 10% is reserved for evaluating model performance.
- The split is performed randomly but reproducibly (using a fixed random seed).

## Visualization

- After training and evaluation, each model produces a 2D scatter plot visualizing the relationship between the ground truth prices and the model's predictions. This helps assess model accuracy and error distribution.

## Project Highlights

- **Modular Design:** The codebase is organized into reusable modules for data handling, feature extraction, modeling, and evaluation.
- **Traditional ML Focus:** Demonstrates the effectiveness of classic ML algorithms (Linear Regression, Random Forest, SVR) on real-world, text-rich data.
- **Text Feature Engineering:** Explores both simple (BoW) and advanced (Word2Vec) text representations for regression tasks.
- **Efficient Processing:** Uses parallel data loading and restricts dataset size for quick experimentation.
- **Reproducibility:** Fixed random seeds ensure consistent results across runs.
- **Visualization:** Built-in 2D plots for intuitive model performance analysis.

---

**All required dependencies for running these models are listed in the `requirements.txt` file at the project root. Please ensure you install them before running any scripts.**

---

**To run the models:**
1. Download the Amazon Reviews dataset and place a portion in `data/meta_Appliances.jsonl`.
2. Run any of the scripts in this directory (e.g., `python linear_model.py`).
3. Review the printed evaluation metrics and the generated scatter plot.

For more details, see the code and comments in each script. 
