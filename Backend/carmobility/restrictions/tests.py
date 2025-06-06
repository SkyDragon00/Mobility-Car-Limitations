from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class TestVehicleRestrictionChecker(TestCase):
## test that the home page loads correctly and can circulate
    def test_successful_post(self):
        url = reverse('home')
        data = {
            'plate': 'ABC-1234',
            'date': '2025-05-21',
            'time': '07:00'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        bold_texts = [span.text.strip() for span in soup.find_all('span', class_='font-bold')]
        self.assertIn('ABC-1234', bold_texts)
        self.assertIn('Wednesday, May 21, 2025', bold_texts)
        self.assertIn('07:00 AM', bold_texts)

        page_text = soup.get_text(separator=' ').strip()
        self.assertIn('Your vehicle CAN circulate', page_text)

##test where the vehicle cannot circulate because the last digit of the plate is restricted and its 9:00AM
    def test_restricted_post(self):
        url = reverse('home')
        data = {
            'plate': 'XYZ-5678',
            'date': '2025-05-15',
            'time': '09:00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # grab all bolded spans
        bold_texts = [span.text.strip() for span in soup.find_all('span', class_='font-bold')]

        # check plate, formatted date, and formatted time
        self.assertIn('XYZ-5678', bold_texts)
        self.assertIn('Thursday, May 15, 2025', bold_texts)
        self.assertIn('09:00 AM', bold_texts)

        # check the main “cannot circulate” message
        page_text = soup.get_text(separator=' ').strip()
        self.assertIn('Your vehicle CANNOT circulate on Thursday, May 15, 2025 at 09:00 AM', page_text)

        # optionally assert the restriction period appears
        self.assertIn('morning (6:00 AM - 9:30 AM)', page_text)


##test where the vehicle cannot circulate because the last digit of the plate is restricted and its 6:00PM
    def test_restricted_post_afternoon(self):
        url = reverse('home')
        data = {
            'plate': 'XYZ-5678',
            'date': '2025-05-15',
            'time': '18:00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # grab all bolded spans
        bold_texts = [span.text.strip() for span in soup.find_all('span', class_='font-bold')]

        # check plate, formatted date, and formatted time
        self.assertIn('XYZ-5678', bold_texts)
        self.assertIn('Thursday, May 15, 2025', bold_texts)
        self.assertIn('06:00 PM', bold_texts)

        # check the main “cannot circulate” message
        page_text = soup.get_text(separator=' ').strip()
        self.assertIn('Your vehicle CANNOT circulate on Thursday, May 15, 2025 at 06:00 PM', page_text)

        # optionally assert the restriction period appears
        self.assertIn('afternoon (4:00 PM - 8:00 PM)', page_text)

##test where the vehicle cannot circulate because the last digit of the plate is restricted that day but its 2:00PM so it can circulate
    def test_successful_post_afternoon(self):
        url = reverse('home')
        data = {
            'plate': 'XYZ-5678',
            'date': '2025-05-15',
            'time': '14:00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # grab all bolded spans
        bold_texts = [span.text.strip() for span in soup.find_all('span', class_='font-bold')]

        # check plate, formatted date, and formatted time
        self.assertIn('XYZ-5678', bold_texts)
        self.assertIn('Thursday, May 15, 2025', bold_texts)
        self.assertIn('02:00 PM', bold_texts)

        # check the main “can circulate” message
        page_text = soup.get_text(separator=' ').strip()
        self.assertIn('Your vehicle CAN circulate on Thursday, May 15, 2025 at 02:00 PM', page_text)
        