from django.test import TestCase
from animals.models import Animal
from rest_framework.test import APIClient

class AnimalApiTests(TestCase):

    def setUp(self) -> None:
        Animal.objects.all().delete()
        return super().setUp()

    def test_get(self):
        Animal.objects.create(species='Dog', name='Ralf', age=2)
        Animal.objects.create(species='Cat', name='Mittens', age=5)
        Animal.objects.create(species='Dog', name='Boris', age=12)


        client = APIClient()
        response = client.get('http://localhost/pet/')

        self.assertEqual(
            response.status_code,
            200,
            msg="Expected response code to be 200 - OK"
        )

        self.assertCountEqual(
            #Note: this ensures the elements in the list are the same, but in any order
            response.data,
            [
                {'species': 'Dog', 'name': 'Boris', 'age': 12},
                {'species': 'Dog', 'name': 'Ralf', 'age': 2},
                {'species': 'Cat', 'name': 'Mittens', 'age': 5},
            ],
            msg="Expected response data to contain the 3 animals from the Animal table"
        )

    def test_post(self):
        self.assertEqual(
            list(Animal.objects.all()),
            [],
            msg="Test pre-condition. Ensure animal table is empty."
        )

        client = APIClient()
        response1 = client.post(
            'http://localhost/pet/', 
            data={'species': 'Cat', 'name': 'Spot', 'age': 2}
        )

        self.assertEqual(
            response1.status_code,
            201,
            msg="Expected first post response code to be 201 - created"
        )

        self.assertCountEqual(
            list(Animal.objects.all().values('species', 'name', 'age')),
            [{"species":"Cat", "name":"Spot", "age":2}],
            msg="Expected post request to add new entry to the Animal table"

        )

        response2 = client.post(
            'http://localhost/pet/', 
            data={'species': 'Dog', 'name': 'Bird', 'age': 3}
        )

        self.assertEqual(
            response2.status_code,
            201,
            msg="Expected second post response code to be 201 - created"

        )

        self.assertCountEqual(
            list(Animal.objects.all().values('species', 'name', 'age')),
            [
                {"species":"Cat", "name":"Spot", "age":2},
                {"species":"Dog", "name":"Bird", "age":3},
             ],
            msg="Expected post request to add a second entry to the Animal table"
        )
