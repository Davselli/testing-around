import random  # To randomize questions when in Learning mode
import jsonpickle  # To save class objects into a JSON file
import pandas as pd  # To convert JSON file into CSV file
import csv  # To convert CSV file into Class objects
import glob  # To list files in a directory
import os  # To list files excluding the path


# my_list = []
my_loaded_list = []


class Question:  # It defines questions for the test
    def __init__(self, question, answer, hint):
        self.question = question
        self.answer = answer
        self.hint = hint


def ask_question():  # It asks the question
    question: str = input("Please enter the question: ")
    return question


def ask_answer():  # It asks the answer related to the question
    answer: str = input("Please enter the answer: ")
    return answer


def ask_hint():  # It asks the hint related to the question
    hint: str = input("Please enter the hint: ")
    return hint


def get_info():  # It asks the user to enter all the info about the question
    question = ask_question()
    answer = ask_answer()
    hint = ask_hint()
    return question, answer, hint


def new_questions():  # It asks and adds questions to the list
    my_list = my_loaded_list
    more_questions = True
    while more_questions:
        item = get_info()
        question = Question(item[0], item[1], item[2])
        my_list.append(question)
        ask_if_more_questions: str = input("Press enter to add another question or anything else to exit: ")
        if ask_if_more_questions:
            more_questions = False
            break
    return my_list


def convert_json_to_csv():  # It converts a JSON file into CSV file
    load_json_file = pd.read_json("./Topics/" + topic_name_json)
    load_json_file.to_csv(("./Topics/" + topic_name_csv), index=None)


def topics():  # It generates a list of CSV files into the ~/Topics folder
    topics = [os.path.basename(asd).strip(".csv") for asd in
              glob.glob("./Topics/*.csv")]
    print("Here is a list of topics: OS", *topics, sep="\n")
    return topics


def learning_mode():  # It opens the Learning mode and tests the entered topic name
    print("Welcome to the Learning mode!")
    topics()
    test_topic = True
    while test_topic:
        topic_name = input("Please choose the topic or press Enter to go back: ")
        topic_name_csv = topic_name + ".csv"
        if not topic_name:
            return
        try:
            open_topic = open(("./Topics/" + topic_name_csv), "r")
            print("The file is open.")
            open_topic.close()
            test_topic = False
        except FileNotFoundError:
            print("The file doesn't exist.")
            test_topic = True
    return topic_name


def learning_mode2():  # It shows the question and asks what to do next (show answer/hint or quit)
    for a in import_list:
        print(a.question)
        while True:
            answer_or_help = input("Press a for Answer, h for Help, q to quit: ")
            if answer_or_help == "h":
                print(a.hint)
                print(a.question)
            elif answer_or_help == "a":
                print(a.answer)
                break
            elif answer_or_help == "q":
                print("Goodbye!")
                return
            else:
                print("This is not a valid answer")
    return learning_mode2()


def import_csv():  # It imports all data from an existing CSV file
    with open(("./Topics/" + topic_name_csv)) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            my_loaded_list.append(Question(row[1], row[2], row[3]))
    del my_loaded_list[0]
    return my_loaded_list


def database_mode():  # It edits  or creates a list of objects
    try:
        open_topic = open(("./Topics/" + topic_name_csv), "r")
        print("The file is open.")
        open_topic.close()
        importing_csv = import_csv()
    except FileNotFoundError:
        print("The file doesn't exist. Creating a new one...")
    ask_new_questions = new_questions()
    return ask_new_questions


def export_json_file():  # It exports all the objects into a JSON file
    json_encode = jsonpickle.encode(topic_questions, indent=4)
    with open("./Topics/" + topic_name_json, "w") as json_encoded_file:
        json_encoded_file.write(json_encode)
        json_encoded_file.close()
    return json_encoded_file


welcome1 = True
while welcome1:
    welcome = input("Please press enter for Learning mode or anything else to edit database: ")
    if not welcome:  # Learning mode
        topic_name = learning_mode()  # It opens the Learning mode and tests the entered topic name
        if not topic_name:
            pass
        else:
            topic_name_csv = topic_name + ".csv"
            import_list = import_csv()  # It imports data from a CSV file
            random.shuffle(import_list)  # It randomizes data from the CSV file
            learning_mode2()  # It shows the question and asks what to do next (show answer/hint or quit)


    else:  # Edit database mode
        topics()
        topic_name = input("Please enter the name of the topic or press Enter to go back: ")
        if topic_name:
            topic_name_csv = topic_name + ".csv"
            topic_name_json = topic_name + ".json"
            topic_questions = database_mode()
            exporting_json_file = export_json_file()
            convert_json_to_csv()
    close_app = input("Press Enter to exit, anything else to start from the beginning: ")
    if not close_app:
        welcome1 = False
        break


