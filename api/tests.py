import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


# region Test Class
class APIUnitTesting(APITestCase):

    def setUp(self):
        self.client = APIClient()

    # region test for input: {'text': 'i dont feeeel good about this because they are not the sweetest people'}
    def test_1(self):
        expected_output = str.encode('{"emotions": ["not the sweetest people", "dont feel good"], "topic": ["about", "this", "because", "they", "are"]}')
        data = json.dumps({'text': 'i dont feeeel good about this because they are not the sweetest people'})
        response = self.client.generic('GET', reverse('api'), data, content_type="application/json")
        print("Test#1 Input:", data)
        print("Test#1 Output:", response.content)
        self.assertEqual(response.content, expected_output)
    # endregion

    # region test for input: {"emotions": [], "topic": ["going", "home", "dont", "feel", "good"]}
    def test_2(self):
        expected_output = str.encode('{"emotions": [], "topic": ["going", "home", "dont", "feel", "good"]}')
        data = json.dumps({'text': 'Im going home bc I dont feel good'})
        response = self.client.generic('GET', reverse('api'), data, content_type="application/json")
        print("Test#2 Input:", data)
        print("Test#2 Output:", response.content)
        self.assertEqual(response.content, expected_output)
    # endregion

    # region test for input: {"emotions": [], "topic": ["that", "dude", "gets", "respect"]}
    def test_3(self):
        expected_output = str.encode('{"emotions": [], "topic": ["that", "dude", "gets", "respect"]}')
        data = json.dumps({'text': 'that dude gets no respectt'})
        response = self.client.generic('GET', reverse('api'), data, content_type="application/json")
        print("Test#3 Input:", data)
        print("Test#3 Output:", response.content)
        self.assertEqual(response.content, expected_output)
    # endregion
# endregion