#!/usr/bin/env python
# import modules needed
import string

# List of symptoms (Our bot is selective, only pick one)
# We will filter out words that are not in list

list_symp = ['abdominal pain', 'blood in stool', 'chest pain', 'constipation',
             'cough', 'diarrhea', 'difficulty swallowing', 'dizziness',
             'eye discomfort', 'eye redness', 'eye problems', 'foot swelling', 'foot pain','headache', 'heart palpitations', 'hip pain', 'knee pain', 'low back pain',
             'nasal congestion', 'nausea or vomiting', 'neck pain', 'numbness', 'pelvic pain','shortness of breath', 'shoulder pain', 'sore throat', 'urinary problems', 'wheezing']

# Assigning each symptoms to possible diseases that cause the symptom.
# (For bot, use this )
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
     
if __name__ == '__main__':
    
    # Gathers information about the user
    user_name, user_age, user_gender = map(str, input('>').split()) # Should protect this more, what if input is > 3?
    main_symp = input('>').split()
    
    user_status = Patient(user_name,user_age,user_gender)
    user_symptoms = Symptom(main_symp)
    

    output = preprocess(filter_extra(filter_lower(user_symptoms.symptoms)),copy_list(list_symp))
    test = bot_access(output)

if test in Dict_symptoms:
    print(output)
    print(Dict_symptoms[test])
else:
    print("Contact doctor pls!!!")