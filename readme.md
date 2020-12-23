# Canvs Emotion Extraction
Setup guide for Canvs API

### What does this API do?
- ****Emotion/Topic Extraction:**** Passes the text input over a pipeline (*Normalize -> NonEmotion Extraction -> Emotion Extraction -> Remove Common Entries of Emotions/NonEmotions -> Topic Extraction*) and outputs a list of emotions and topics.
- ****Unit Tests:**** Django's Test Framework conducts unit tests over the 3 litmus test examples provided in the brief.


### Testing Environment
- Ubuntu 20.04


### Pre-requisites
- All packages mentioned in the *requirements.txt* file (pip3 install -r requirements.txt)


### Assumptions
- Punctuations have been removed to make sure they don't hinder the emotion extraction.
- Common entries between emotions and nonemotions are removed from final emotions list in the 4th step of pipeline to conform to the outputs of both Example#1 and Example#2 in the brief, i.e. "dont feel good" phrases.
- Exact-match substring extractions have been avoided. For example, the word "dud" is in the emotions dictionary, but this word should NOT be extracted from this sentence "that dude gets no respect" since here the word is "dude" and not "dud".
- Extra spaces have been replaced with single space to improve the extraction.


### How to run the API?
1. ****Emotion/Topic Extraction:**** By hitting the API (http://ip_address/api) with a GET request and a JSON input in the following format, a list of emotions and topics are extracted from the input text.
```sh
{'text': 'sample input'}
```
2. ****Unit Tests:**** Django's Test Framework has been included that can be run with this command for unit testing of the litmus test examples provided in the brief: 
```sh
python3 manage.py test
```


### Example Outputs
1. ****Emotion/Topic Extraction:****

![N|emotion_extraction](https://res.cloudinary.com/tkxel/image/upload/v1608671438/emotion_extraction_wm6kmf.jpg)

2. ****Unit Tests****
![N|pytest](https://res.cloudinary.com/tkxel/image/upload/v1608671150/pytest_om00ti.jpg)
