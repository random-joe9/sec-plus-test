import pathlib
import random
import time
import datetime
import os

# import find_q
from string import ascii_lowercase

try:
    import tomllib
except ModuleNotFoundError:
    import tomllib as tomllib

DEFAULT_QUESTIONS_PER_QUIZ = 5 #default number of questions to ask per test.
QUESTIONS_PATH = pathlib.Path(__file__).parent / "editted.toml"

total_questions = 286 #just shows total number of questions in test to help determine the number of questions to take per test
NUM_QUESTIONS_PER_QUIZ = int(
    input(
        f"\nHow many questions would you like on your test? There are a total of {total_questions} in this test bank\nYour selection:  "
    )
)

if NUM_QUESTIONS_PER_QUIZ >= DEFAULT_QUESTIONS_PER_QUIZ:
    print(f"you have selected {NUM_QUESTIONS_PER_QUIZ} for your test.")
    print("Let's begin.")
    NUM_QUESTIONS_PER_QUIZ = NUM_QUESTIONS_PER_QUIZ


else:
    print(
        f"Your have selection of {NUM_QUESTIONS_PER_QUIZ} does not meet the minimum of {DEFAULT_QUESTIONS_PER_QUIZ}. Test defaulted to {DEFAULT_QUESTIONS_PER_QUIZ} questions."
    )
    print("Let's begin.")
    NUM_QUESTIONS_PER_QUIZ = DEFAULT_QUESTIONS_PER_QUIZ


def run_quiz():
    questions = prepare_questions(QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ)
    questions_number_asked = []
    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(
            f"\nQuestion {num} ({num} of {NUM_QUESTIONS_PER_QUIZ}) ({question['question_number']}):\n"
        )
        questions_number_asked.append(question["question_number"])
        num_correct += ask_question(question)
        score_precent = 100 * (num_correct / num)
    print(
        f"\nYou got {num_correct} correct out of {num} questions\nScoring {score_precent}% "
    )
    print(questions_number_asked)
    insert_questions(questions_number_asked)
    tracker(num, num_correct, score_precent)


def prepare_questions(path, num_questions):
    questions = tomllib.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)


def ask_question(question):
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question=question["question"],
        question_number=question["question_number"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    if correct := (set(answers) == set(correct_answers)):
        print("⭐ Correct! ⭐")

        if "explanation" in question:
            print(f"\nEXPLANATION:\n{question['explanation']}")

    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n- ".join([f"❗️❗️ No, the answer{is_or_are} ❗️❗️:"] + correct_answers))
        if "explanation" in question:
            print(f"\nEXPLANATION:\n{question['explanation']}")

    print("----------------------------------------------------------------")
    time.sleep(2) #idea here is to just give a small break before the next question, sort f like a loading screen on a real test.

    return 1 if correct else 0


def get_answers(question, question_number, alternatives, num_choices=1, hint=None):
    print(f"{question}")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(",", " ").split())

        # Handle hints
        if hint and "?" in answers:
            print(f"\nHINT: {hint}")
            continue

        # Handle invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any((invalid := answer) not in labeled_alternatives for answer in answers):
            print(
                f"{invalid!r} is not a valid choice. "
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]


def insert_questions(questions_array):
    if os.path.isfile("Question_Tracker_File.txt"):
        print("file exists, adding entry")
        # f = open("demofile3.txt", "a")

        with open("Question_Tracker_File.txt", "a") as txt_file:
            for line in questions_array:
                txt_file.write(
                    str(line) + ", "
                )  # works with any number of elements in a line
            txt_file.close()

    else:
        print("Created file, adding entry")
        f = open("Question_Tracker_File.txt", "w")
        f.close()

        with open("Question_Tracker_File.txt", "a") as txt_file:
            for line in questions_array:
                txt_file.write(
                    str(line) + ", "
                )  # works with any number of elements in a line
            txt_file.write("\n")
            txt_file.close()


def tracker(num, questions_correct, score_precent):
    try:
        if os.path.isfile("COMPTIA_Sec_Plus_Tracker_File.txt"):
            print("file exists, adding entry")
            # f = open("demofile3.txt", "a")

            score_precent = 100 * (questions_correct / num)
            input_array = [
                questions_correct,
                num,
                score_precent,
                str(datetime.datetime.now()),
            ]

            with open("COMPTIA_Sec_Plus_Tracker_File.txt", "a") as txt_file:
                for line in input_array:
                    txt_file.write(
                        str(line) + ", "
                    )  # works with any number of elements in a line

                txt_file.write("\n")
                txt_file.close()

        else:
            print("Created file, adding entry")
            f = open("COMPTIA_Sec_Plus_Tracker_File.txt", "w")
            f.close()
            input_array = [
                questions_correct,
                num,
                score_precent,
                str(datetime.datetime.now()),
            ]
            with open("COMPTIA_Sec_Plus_Tracker_File.txt", "a") as txt_file:
                for line in input_array:
                    txt_file.write(
                        str(line) + ", "
                    )  # works with any number of elements in a line
                txt_file.write("\n")
                txt_file.close()

    except:
        print("error")


if __name__ == "__main__":
    run_quiz()
