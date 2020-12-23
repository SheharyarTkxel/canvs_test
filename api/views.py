import json
import re
import string
import pandas as pd
import simplejson as simplejson
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

# region Global Declarations
source_sheet = pd.ExcelFile('resources/data_exercise.xlsx', engine='openpyxl')
emotion_list = pd.read_excel(source_sheet, 'emotion')['emotion'].tolist()
misspelling_list = pd.read_excel(source_sheet, 'misspelling')['misspelling'].tolist()
norm_list = pd.read_excel(source_sheet, 'misspelling')['norm'].tolist()
nonemotion_list = pd.read_excel(source_sheet, 'nonemotion')['nonemotion'].tolist()
# endregion

# region API Call
@api_view(['GET'])
def api(request):
    if request.method == 'GET':
        try:
            input = json.loads(json.dumps(request.data))['text'].lower()

            # region Pipeline
            # Normalize -> NonEmotion Extraction -> Emotion Extraction -> Remove Common Entries -> Remove Emotions from Original Input ->  Topic Extraction
            input_normalized = normalize(input)
            input_nonemotion_list = nonemotion_extraction(input_normalized)
            input_emotion_list = emotion_extraction(input_normalized)
            input_emotion_list = remove_common_entries(input_emotion_list, input_nonemotion_list)
            input = remove_emotion(input_emotion_list, input_normalized)
            topics = topic_extraction(input)
            output = {'emotions': input_emotion_list, 'topic': topics}
            # endregion
        except Exception as e:
            return HttpResponse("Some error occured. Make sure to follow this JSON standard with a GET call: {'text': 'sample text'}", status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(simplejson.dumps(output), content_type='application/json', status=status.HTTP_200_OK)
    else:
        return HttpResponse("Please follow this JSON standard with a GET call: {'text': 'sample text'}", status=status.HTTP_404_NOT_FOUND)
# endregion

# region Helper Functions
def normalize(input):
    # Removing extra spaces
    input = ' '.join(input.split())
    # Removing punctuations and splitting the input string into a list
    input_list = input.translate(str.maketrans('', '', string.punctuation)).split(' ')

    # Checking if any misspelled word is in the input
    for index, misspelled_value in enumerate(misspelling_list):
        if str(misspelled_value).lower() in input_list:
            # Replacing the misspelled with the normalized words
            input_list = [str(norm_list[index]).lower() if str(val).lower() == misspelled_value else val for val in input_list]
    return ' '.join(input_list)


def nonemotion_extraction(input):
    # Extracting nonemotions from the input
    return [value for value in nonemotion_list if input.find(str(value).lower()) != -1]


def emotion_extraction(input):
    # Extracting emotions from the input
    return [value for value in emotion_list if re.search(r"\b{}\b".format(value), input, re.IGNORECASE) is not None]


def remove_common_entries(emotions, nonemotions):
    # Removing entries from the emotions list that are present in the nonemotions list as well
    for emotion in emotions:
        for nonemotion in nonemotions:
            if emotion in nonemotion:
                emotions.remove(emotion)
    return emotions


def remove_emotion(emotions, input):
    # Removing extracted emotions from the original input to clean it
    for emotion in emotions:
        input = input.replace(emotion, '')
    return input


def topic_extraction(input):
    # Extracting topic entries that are above 2 in length
    return [value for value in input.split(" ") if len(str(value)) > 2]
# endregion