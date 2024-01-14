import json
import matplotlib.pyplot as plt

def calculate_accuracy(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    total_correct = 0
    deprecated = 0
    q_type_accuracy = {}

    for entry in data:
        correctness = entry["correctness"]

        if (correctness == 3):
            deprecated += 1
            continue

        total_correct += entry["correctness"]
        question_type = entry["question_type"]
        if question_type not in q_type_accuracy:
            q_type_accuracy[question_type] = {"correct": 0, "total": 0, "accuracy": 0}
        q_type_accuracy[question_type]["correct"] += entry["correctness"]
        q_type_accuracy[question_type]["total"] += 1

    # Calculating accuracy for each question type
    for q_type in q_type_accuracy:
        q_type_accuracy[q_type]["accuracy"] = q_type_accuracy[q_type]["correct"] / q_type_accuracy[q_type]["total"]
    
    valid_questions = len(data) - deprecated
    q_type_accuracy['overall'] = {"correct": total_correct, "total": valid_questions, "accuracy": total_correct / valid_questions}
    return q_type_accuracy


# add image length analyzor
def imglen_accuracy(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    i_len_acc = {}
    for entry in data:
        if (entry["correctness"] == 3):
            continue
        image_num = str(entry["image_num"])
        if image_num not in i_len_acc:
            i_len_acc[image_num] = {"correct": 0, "total": 0, "accuracy": 0}
        i_len_acc[image_num]["correct"] += entry["correctness"]
        i_len_acc[image_num]["total"] += 1

    # Calculating accuracy for each question type
    for i_len in i_len_acc:
        i_len_acc[i_len]["accuracy"] = i_len_acc[i_len]["correct"] / i_len_acc[i_len]["total"]
    
    return i_len_acc

file_path = 'gpt4v_ans_wo_distractors.json'
# typed_accuracy = calculate_accuracy(file_path)
image_num_accuracy = imglen_accuracy(file_path)

# Print accuracies in fraction format
# for type, values in typed_accuracy.items():
#     fraction_accuracy = str(values['correct']) + '/' + str(values['total']) 
#     print(f"[{type}] Accuracy: {fraction_accuracy}")


# labels = list(typed_accuracy.keys())
# accuracies = [values["accuracy"] for values in typed_accuracy.values()]

# # Plotting
# fig, ax = plt.subplots()
# bars = ax.bar(labels, accuracies, color=['green' if label != 'overall' else 'orange' for label in labels])


# for bar in bars:
#     yval = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom')

# # Improve layout
# plt.xticks(rotation=90)
# plt.xlabel('Question Type')
# plt.ylabel('Accuracy')
# plt.title('Accuracy by Question Type')
# ax.set_ylim(0, 1)
# plt.tight_layout()

# # plt.show()
# plt.savefig('plot.png')



for len, values in image_num_accuracy.items():
    fraction_accuracy = str(values['correct']) + '/' + str(values['total']) 
    print(f"[{len}] Accuracy: {fraction_accuracy} = {values['accuracy']}")

len_labels = list(image_num_accuracy.keys())
len_accuracies = [values["accuracy"] for values in image_num_accuracy.values()]

# Plotting
fig, ax = plt.subplots()
bars = ax.bar(len_labels, len_accuracies, color='orange')


for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom')

# Improve layout
plt.xlabel('Images Required')
plt.ylabel('Accuracy')
plt.title('Accuracy by Images Required')
ax.set_ylim(0, 1)
plt.tight_layout()

plt.savefig('img_len_acc_plot.png')