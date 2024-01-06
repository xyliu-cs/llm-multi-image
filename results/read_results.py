import json
import matplotlib.pyplot as plt

def calculate_accuracy(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    total_correct = 0
    q_type_accuracy = {}
    total_questions = len(data)

    for entry in data:
        total_correct += entry["correctness"]
        question_type = entry["question_type"]
        if question_type not in q_type_accuracy:
            q_type_accuracy[question_type] = {"correct": 0, "total": 0, "accuracy": 0}
        q_type_accuracy[question_type]["correct"] += entry["correctness"]
        q_type_accuracy[question_type]["total"] += 1

    # Calculating accuracy for each question type
    for q_type in q_type_accuracy:
        q_type_accuracy[q_type]["accuracy"] = q_type_accuracy[q_type]["correct"] / q_type_accuracy[q_type]["total"]
    
    q_type_accuracy['overall'] = {"correct": total_correct, "total": total_questions, "accuracy": total_correct / total_questions}
    return q_type_accuracy


file_path = './gpt_4v_answers.json'
typed_accuracy = calculate_accuracy(file_path)

# Print accuracies in fraction format
for type, values in typed_accuracy.items():
    fraction_accuracy = str(values['correct']) + '/' + str(values['total']) 
    print(f"[{type}] Accuracy: {fraction_accuracy}")


labels = list(typed_accuracy.keys())
accuracies = [values["accuracy"] for values in typed_accuracy.values()]

# Plotting
fig, ax = plt.subplots()
bars = ax.bar(labels, accuracies, color=['green' if label != 'overall' else 'orange' for label in labels])


for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom')

# Improve layout
plt.xticks(rotation=90)
plt.xlabel('Question Type')
plt.ylabel('Accuracy')
plt.title('Accuracy by Question Type')
ax.set_ylim(0, 1)
plt.tight_layout()

plt.show()
