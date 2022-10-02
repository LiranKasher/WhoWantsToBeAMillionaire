# This program has been written by Liran Kasher for recreational purposes only.
# All rights of "Who wants to be a millionaire" are reserved to it's rightful owner and are not mine.

# import time function to pause the screen
import time
# import the choice function
import random
# import data from json file
import json
# import the modules to play sounds while in-game.
from playsound import playsound
import pygame

# mixer has to be initiated in order to play music files
pygame.mixer.init()


# checks if the user has written a proper answer
def check_written_answer(answer):
    while answer != "Yes" and answer != "No":
        answer = str(input("\nPlease write again (use only 'Yes' or 'No'):"))
    return answer


# checks if the user has written a proper answer to the lifeline question
def check_user_lifeline_answer(answer):
    while answer != "1" and answer != "2" and answer != "3":
        answer = str(input("\nPlease write again (use only 1/2/3):"))
    return answer


# checks if and how many lifelines are left
def check_lifelines():
    counter = 0
    unused_lifelines = []
    for i in lifelines_bool:
        if i == False:
            unused_lifelines.append(lifelines[counter])
        counter = counter + 1
    return unused_lifelines


def print_lifelines(unused_lifelines):
    print("\nPlease select which lifeline to use, by writing the number 1/2/3:")
    for j in unused_lifelines:
        place = lifelines.index(j)
        print(str(place + 1) + ". " + str(j))
    return str(input())


########################################################################################################################
# Lifelines:
########################################################################################################################
# '50:50' lifeline
def fifty_fifty(current_answers, correct_answer, used_answers):
    lifelines_bool[0] = True
    playsound('Lifeline-50-50.mp3', False)
    random_answer = random.choice([i for i in current_answers if i != correct_answer])
    index_random_answer = used_answers.index(random_answer)
    index_correct_answer = used_answers.index(correct_answer)
    if index_random_answer < index_correct_answer:
        print(str(index_random_answer + 1) + ". " + random_answer)
        print(str(index_correct_answer + 1) + ". " + correct_answer)
    else:
        print(str(index_correct_answer + 1) + ". " + correct_answer)
        print(str(index_random_answer + 1) + ". " + random_answer)


########################################################################################################################
# 'Ask the audience' lifeline
def ask_the_audience(correct_answer, used_answers):
    global percentage
    lifelines_bool[1] = True
    pygame.mixer.music.load('Lifeline-Audience.mp3')
    pygame.mixer.music.play()
    print("\nCalculating results from the audience, please wait...")
    time.sleep(6)
    pygame.mixer.music.load('Lifeline-Audience-Done.mp3')
    pygame.mixer.music.play()
    line_length = (len(max(used_answers, key=len))) + 4
    random_percentage = random.randrange(60, 100)
    rest_of_percentage_1 = random.randrange(0, 100 - random_percentage)
    rest_of_percentage_2 = random.randrange(0, 100 - random_percentage - rest_of_percentage_1)
    rest_of_percentage_3 = 100 - random_percentage - rest_of_percentage_1 - rest_of_percentage_2
    count_wrong_answers = 0
    for i in used_answers:
        if i == correct_answer:
            print(
                str(used_answers.index(i) + 1) + ". " + i + (line_length - len(i)) * " " + str(random_percentage) + "%")
        else:
            if count_wrong_answers == 0:
                percentage = rest_of_percentage_1
            if count_wrong_answers == 1:
                percentage = rest_of_percentage_2
            if count_wrong_answers == 2:
                percentage = rest_of_percentage_3
            count_wrong_answers = count_wrong_answers + 1
            print(str(used_answers.index(i) + 1) + ". " + i + (line_length - len(i)) * " " + str(percentage) + "%")

    time.sleep(1)


########################################################################################################################
# 'Phone a Friend' lifeline
def phone_a_friend(current_answers, correct_answer, used_answers):
    lifelines_bool[2] = True
    pygame.mixer.music.load('Lifeline-phone-a-friend.mp3')
    pygame.mixer.music.play()
    time.sleep(10.2)
    random_answer = random.choice([i for i in current_answers if i != correct_answer])
    index_random_answer = used_answers.index(random_answer)
    index_correct_answer = used_answers.index(correct_answer)
    random_percentage = random.randrange(0, 100)
    if random_percentage > 74:
        print("\nI am sure the correct answer is:" + "\n" + str(index_correct_answer + 1) + ". " + correct_answer)
    if random_percentage >= 50 and random_percentage <= 74:
        print("\nI am not sure exactly,but I think the correct answer is:" + "\n" + str(
            index_correct_answer + 1) + ". " + correct_answer)
    if random_percentage >= 25 and random_percentage <= 49:
        print("\nI have absolutely no idea what is the right answer. "
              "If I had to guess, I would guess the correct answer is:" + "\n" + str(
            index_correct_answer + 1) + ". " + correct_answer)
    if random_percentage < 25:
        print("\nI am not sure exactly,but I think the correct answer is:" + "\n" + str(
            index_random_answer + 1) + ". " + random_answer)


########################################################################################################################

# import the questions and answers from a JSON file
with open('data.json', 'r') as questions:
    obj = json.load(questions)
question_number = 1
used_questions = []
amount_num = 0
amount = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
lifelines = ["50:50", "Ask the audience", "Phone a friend"]
lifelines_bool = [False, False, False]

print("Welcome to Liran's: Who Wants to be a Millionaire! :)")
#playsound('main-theme.mp3')

for i in obj["questions"]:
    print("\nThe following question is worth " + str(f"{amount[amount_num]:,}") + "$!")
    playsound('next-question.mp3')
    print("\nQuestion " + str(question_number))
    print("¯¯¯¯¯¯¯¯¯¯")
    playsound('lets-play.mp3', False)
    # pausing the screen for (x) seconds
    time.sleep(5)
    question_number = question_number + 1
    current_question = random.choice([i for i in obj["questions"] if i not in used_questions])
    used_questions.append(current_question)
    location = obj["questions"].index(current_question)
    print(current_question)
    time.sleep(3)
    answer_number = 1
    used_answers = []
    for j in obj["answers"][location]:
        current_answer = random.choice([i for i in obj["answers"][location] if i not in used_answers])
        print(str(answer_number) + ". " + current_answer)
        answer_number = answer_number + 1
        used_answers.append(current_answer)
        time.sleep(1.5)
    if check_lifelines() != []:
        user_feedback = str(input("\nWould you like to use a lifeline? (Yes/No)"))
        user_feedback = check_written_answer(user_feedback)
        if user_feedback == "Yes":
            lifeline = print_lifelines(check_lifelines())
            lifeline = check_user_lifeline_answer(lifeline)
            print("\n")
            if lifeline == "1":
                fifty_fifty(obj["answers"][location], obj["correct_answer"][location], used_answers)
            elif lifeline == "2":
                ask_the_audience(obj["correct_answer"][location], used_answers)
            elif lifeline == "3":
                phone_a_friend(obj["answers"][location], obj["correct_answer"][location], used_answers)
    else:
        print("\n(You have no more lifelines.)")
    sure = "No"
    while sure == "No":
        pygame.mixer.music.load('answer-question.mp3')
        pygame.mixer.music.play()
        player_answer = str(input("\nPlease write the correct answer as it appears, and press enter:"))
        doesAnswerExist = False
        while doesAnswerExist == False:
            for k in obj["answers"][location]:
                if player_answer == k:
                    doesAnswerExist = True
                    break
            if doesAnswerExist == False:
                player_answer = str(input("Answer does not exist. Please try again (Use capital letters):"))
        pygame.mixer.music.load('final-answer.mp3')
        pygame.mixer.music.play()
        sure = str(input("Are you sure? (Yes/No)"))
        sure = check_written_answer(sure)
    pygame.mixer.music.stop()
    correct_answer = obj["correct_answer"][location]
    if player_answer != correct_answer:
        playsound('wrong-answer.mp3', False)
        print("Wrong Answer! The correct answer is " + str(correct_answer) + ". :(")
        time.sleep(3)
        print("\nYou Won " + str(f"{amount[amount_num]:,}") + "$")
        time.sleep(10)
        break
    else:
        playsound('correct-answer.mp3', False)
        print("\nCorrect Answer! :)")
        time.sleep(1)
        print("\nYou now have " + str(f"{amount[amount_num]:,}") + "$.")
        amount_num = amount_num + 1
        time.sleep(5)
    if amount_num == len(amount):
        playsound('main-theme.mp3', False)
        for i in range(0, 49):
            print("\n")
        print("You won!")
        print("         You are a Millionaire!!!")
        print("                                  ( A virtual one, at any rate :) )")
        time.sleep(10)
        print("Press any key to exit the game.")
        time.sleep(0)
        break
    time.sleep(10)
