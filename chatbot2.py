# ChatBot Version 2
import string
import re
import long_responses as long
from uagame import Window
from time import sleep
from random import randint, choice

# List of symptoms (Our bot is selective, only pick one)
# We will filter out words that are not in list

list_symp = ['abdominal pain', 'blood in stool', 'chest pain', 'constipation',
             'cough', 'diarrhea', 'difficulty swallowing', 'dizziness',
             'eye discomfort', 'eye redness', 'eye problems', 'foot swelling', 
             'foot pain','headache', 'heart palpitations', 'hip pain', 'knee pain', 
             'low back pain', 'nasal congestion', 'nausea or vomiting', 'neck pain', 'numbness', 
             'pelvic pain', 'shortness of breath', 'shoulder pain', 'sore throat', 'urinary problems', 'wheezing']

# Assigning each symptoms to possible diseases that cause the symptom.
Dict_symptoms = {
    "abdominal_pain" : "possible causes; food poisoning, gallstones, kidney stones, lactose intolerance",
    "blood_in_stool" : "possible causes; peptic ulcer, gastritis, colon cancer",
    "chest_pain": "possible causes; angina, heart attack, panic attack, heartburn",
    "dry_cough": " possible causes; asthma, common cold, flu, pneumonia",
    "eye_discomfort": "possible causes; dry eyes,pink eye",
    "foot_swelling":"possible causes; achilles tendinitis ,osteoarthritis",
    "foot_pain":" possible causes;broken foot, bruise, sprains, stress fractures",
    "head_ache":" possible causes; migraine,concussion,tension headache",
    "heart_palpitations":"possible causes; panic attack,heart arrhythmia, hyperthyrodism",
    "hip_pain":"possible causes; tendinitis, bursitis",
    "knee_pain":"possible causes; torn meniscus, sprains",
    "shortness_of_breath":"possible causes; asthma, bronchitis, heart attack, pneumonia"
}

####### START OF CHATBOT FUNCTIONALITY #######

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_HEALTH, ['analyze', 'symptoms','sick', 'health', 'doctor'], required_words=['analyze', 'symptom', 'symptoms', 'sick'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

####### END OF CHATBOT FUNCTIONS #######

####### START OF PREPROCESSING ####### 

# Create our patient
# (For bot, ask for name, age and gender)
# (For web, ask the same, expect with delay)
class Patient:
    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

# Make the symptoms as an object        
class Symptom:
    def __init__(self,symptoms):
        self.symptoms = symptoms

    # Processing the symptoms to read each word 
    def process_symptoms(self,symptoms):
        symp = symptoms.split()
        return symp
    
def copy_list(list_symp):
    # Nested list of symptom words
    copyls = []
    resultcopy = []
    # Make our nested list of symptoms from given data
    for word in list_symp:
        word = word.split()
        copyls.append(word)
    # traversing in till the length of the copy list
    for m in range(len(copyls)):
        # Use nested for loop, traversing the inner lists
        for n in range(len(copyls[m])):
            # Add each element to the result list
            resultcopy.append(copyls[m][n])
    return resultcopy
        
def filter_lower(primary):
    processed_0 = []
    for word in primary:
        word = word.lower()
        processed_0.append(word)
    return processed_0

def filter_extra(filtered):
    processed_1 = []
    for word in filtered:
        for letter in word:
            if (letter in string.punctuation) or (letter.isnumeric()):
                wordList = list(word)
                wordList.remove(letter)
                word = "".join(wordList)
        processed_1.append(word)
    return processed_1

def preprocess(filtered,copy):
    processed_final = []
    cplist = copy_list(filtered)
    for element in cplist: 
        if element in copy:
            processed_final.append(element)
    return processed_final

def bot_access(preprocessed):
    guess = "_".join(preprocessed)
    return guess

####### END OF PREPROCESS #######


####### Section for opening the window #######

def main():
    location = [0,0]
    window = create_window()
    display_header(window, location)
    display_symptom_list(window, location)
    user_info = get_info(window,location)
    display_info(window,location,user_info)
    chatbot_display(user_info, window, location)
    answer = display_result(window,location)
    disp_res(window,location,answer)
    end_prog(window)

def create_window():
    # Create a window for the bot, open it and return it
    window = Window('DocBot', 1200, 900)
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('white')
    window.set_bg_color('black')
    return window

def display_header(window, location):
    # Display the header
    # - window is the Window to display in
    # - location is a list containing the int x and y coords of
    # where the header should be displayed and it should be
    # updated for the next output

    header = ['WELCOME TO Dr.Pippin Flask!', 'Please let DocBot know your basic information', '']
    for header_line in header:
        display_line(window, header_line, location)

def listed_keys(Dict_symptoms):
    # Sorts the keys of the symptom dictionary
    newlsymp = []
    for key in Dict_symptoms.keys():
        newlsymp.append(key)
    return newlsymp

def display_symptom_list(window, location):
    # Display the symptoms that can be chosen by the user
    # Take into account the positioning of the text in the window
    embedded_size = 20
    symptom_list = listed_keys(Dict_symptoms)
    for symptom in symptom_list:
        # display embedded password
        symp_line = symptom
        display_line(window, symptom, location)

    # display blank line
    display_line(window, '', location)

    return symptom_list

# Get user input from the window. We want to take this input and pass it back to the chatbot functions to get evaluated
def get_info(window, location):
    info = []
    cFlag = True

    prompt_name = 'Name:'
    prompt_age = 'Age:'
    prompt_gender = 'Gender:'

    feedback_location = [window.get_width() // 2, 0]

    while cFlag:
        # get next guess
        window.draw_string(str(""),0, window.get_font_height())
        info1 = prompt_user(window, prompt_name, location)
        info.append(info1)
        info2 = prompt_user(window, prompt_age, location)
        info.append(info2)
        info3 = prompt_user(window, prompt_gender, location)
        info.append(info3)
        cFlag = False
    display_line(window, '', location)
    return info

def display_info(window,location,infolist):
    for info in infolist:
        info_line = info
        display_line(window, info_line, location)
    # display blank line
    display_line(window, '', location)


def chatbot_display(user_info, window, location):
    counter = 0
    while counter != 3:
        casual_chat = 'Bot: ' + get_response(prompt_user(window,'You: ',location))
        display_line(window, casual_chat, location)
        counter += 1

def display_result(window,location):
    prompt_symp = "How are you feeling today? Select one of the conditions>  "
    result1 = prompt_user(window, prompt_symp, location)
    user_symptoms = Symptom(result1)
    output = preprocess(filter_extra(filter_lower(user_symptoms.symptoms)),copy_list(list_symp))
    new3 = bot_access(output)
    display_line(window, new3, location)
    return new3

def disp_res(window,location,resstr):
    display_line(window,resstr,location)
    
def end_prog(window):
    window.clear()
    location = display_outcome(window,'ITS A PRANK')
    # prompt for end
    location[0] = (window.get_width() - window.get_string_width("URE DONE ENTER")) // 2
    prompt_user(window,'DONE!',location)

def display_line(window, string, location):
    pause_time = 0.5
    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(pause_time)
    location[1] = location[1] + window.get_font_height()

def display_outcome(window, outcome):
    # compute y coordinate
    string_height = window.get_font_height()
    outcome_height = (len(outcome) + 1)*string_height
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2

    location = [0, line_y]
    for outcome_line in outcome:
     # compute x coordinate
        x_space = window.get_width() - window.get_string_width(outcome_line)

        location[0] = x_space // 2
        display_line(window, outcome_line, location)
pass

# Get argument from preprocess file code (See code above)
def prompt_user(window, prompt, location):
    input = window.input_string(prompt, location[0], location[1])
    location[1] = location[1] + window.get_font_height()
    return input

main()