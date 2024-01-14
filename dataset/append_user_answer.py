import json

def append_user_answers():
    with open('question_answer_pairs.json', 'r') as file:
        question_answer_pairs = json.load(file)

    with open('user_results.json', 'r') as file:
        user_results = json.load(file)

    user_results_dict = {result['question_id']: result['user_answer'] for result in user_results}

    for item in question_answer_pairs:
        question_id = item['question_id']
        if question_id in user_results_dict:
            item['user1_answer'] = user_results_dict[question_id]

    # Save the updated data back to question_answer_pairs.json
    with open('question_answer_pairs.json', 'w') as file:
        json.dump(question_answer_pairs, file, indent=4)

# Call the function
append_user_answers()
