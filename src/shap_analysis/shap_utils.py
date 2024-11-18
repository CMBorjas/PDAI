import shap
import matplotlib.pyplot as plt

def explain_model_with_shap(model, tokenizer, text, max_length=150):
    """
    Explains the predictions of the model using SHAP.

    Parameters:
    - model: The GPT-2 model (or any other model).
    - tokenizer: The tokenizer used with the model.
    - text: The input text for explanation.
    - max_length: The maximum length of the generated text.

    Returns:
    None (displays SHAP visualizations).
    """
    # Tokenize input text
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=max_length)

    # Define a SHAP explainer
    explainer = shap.Explainer(model, tokenizer)

    # Compute SHAP values
    shap_values = explainer(input_ids)

    # Plot the SHAP summary
    shap.summary_plot(shap_values.values, feature_names=tokenizer.convert_ids_to_tokens(input_ids[0].tolist()))
