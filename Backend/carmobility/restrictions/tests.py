from django.test import TestCase
from django.urls import reverse

class TestVehicleRestrictionChecker(TestCase):

    def test_successful_post(self):
        url = reverse('home')
        data = {
            'plate': 'ABC-1234',
            'date': '2025-05-21',
            'time': '07:00'
        }
        response = self.client.post(url, data)

        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<span class="font-bold">ABC-1234</span>', html=True)
        self.assertContains(response, 'Your vehicle CAN circulate')
        self.assertContains(response, '<span class="font-bold">Wednesday, May 21, 2025</span>', html=True)
        self.assertContains(response, '<span class="font-bold">07:00 AM</span>', html=True)

##Test where the vehicle cannot circulate
    # def test_unsuccessful_post(self):
    #     url = reverse('home')
    #     data = {
    #         'plate': 'ABC-1234',
    #         'date': '2025-05-21',
    #         'time': '08:00'
    #     }
    #     response = self.client.post(url, data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, '<span class="font-bold">ABC-1234</span>', html=True)
    #     self.assertContains(response, 'Your vehicle CANNOT circulate')
    #     self.assertContains(response, '<span class="font-bold">Wednesday, May 21, 2025</span>', html=True)
    #     self.assertContains(response, '<span class="font-bold">08:00 AM</span>', html=True)