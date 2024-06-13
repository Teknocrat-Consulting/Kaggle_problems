import csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

def read_csv(file_path):
    messages = []
    local_predictions = []
    hf_predictions = []
    original_vals = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            messages.append(row[0])
            local_predictions.append(1 if row[1] == 'spam' else 0)  # Map 'spam' to 1, 'ham' to 0
            hf_predictions.append(1 if row[2] == 'spam' else 0)  # Map 'spam' to 1, 'ham' to 0
            original_vals.append(1 if row[3] == 'spam' else 0)   # Map 'spam' to 1, 'ham' to 0

    return messages, local_predictions, hf_predictions, original_vals

def evaluate_performance(original_vals, local_predictions, hf_predictions):
    metrics = {}
    
    for model_name, predictions in zip(["Local Model", "Hugging Face Model"], [local_predictions, hf_predictions]):
        accuracy = accuracy_score(original_vals, predictions)
        precision = precision_score(original_vals, predictions)
        recall = recall_score(original_vals, predictions)
        f1 = f1_score(original_vals, predictions)
        fpr, tpr, _ = roc_curve(original_vals, predictions)
        roc_auc = auc(fpr, tpr)

        metrics[model_name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1,
            "ROC AUC": roc_auc
        }

        # Confusion Matrix
        cm = confusion_matrix(original_vals, predictions)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title(f'{model_name} Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.show()

    # ROC Curve
    plt.figure(figsize=(8, 6))
    for model_name, predictions in zip(["Local Model", "Hugging Face Model"], [local_predictions, hf_predictions]):
        fpr, tpr, _ = roc_curve(original_vals, predictions)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=2, label=f'{model_name} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

    # Display metrics as a table
    metrics_df = pd.DataFrame(metrics)
    print(metrics_df)

    return metrics

file_path = 'spam_detection_results.csv'
messages, local_predictions, hf_predictions, original_vals = read_csv(file_path)
evaluation_results = evaluate_performance(original_vals, local_predictions, hf_predictions)
