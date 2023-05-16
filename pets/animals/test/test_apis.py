import json
from django.test import TestCase
from animals.models import Animal
from rest_framework.test import APIClient

class AnimalApiTests(TestCase):

    def setUp(self) -> None:
        Animal.objects.all().delete()
        return super().setUp()

    def test_get(self):
        """
            Ensure get request returns all pets
        """

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

    def test_get_filtered(self):
        """
            Ensure get request can filter on species.
            Must not be case sensitive
        """

        Animal.objects.create(species='Dog', name='Ralf', age=2)
        Animal.objects.create(species='Cat', name='Mittens', age=2)
        Animal.objects.create(species='Dog', name='Boris', age=12)


        client = APIClient()

        #Filter on species
        response = client.get('http://localhost/pet/?species=cAt')

        self.assertEqual(
            response.status_code,
            200,
            msg="Expected response code to be 200 - OK"
        )

        self.assertCountEqual(
            #Note: this ensures the elements in the list are the same, but in any order
            response.data,
            [
                {'species': 'Cat', 'name': 'Mittens', 'age': 2},
            ],
            msg="Expected response data to contain only the cat from the Animal table"
        )

        #Filter on age
        response = client.get('http://localhost/pet/?age=2')
        self.assertEqual(
            response.status_code,
            200,
            msg="Expected response code to be 200 - OK"
        )

        self.assertCountEqual(
            #Note: this ensures the elements in the list are the same, but in any order
            response.data,
            [
                {'species': 'Cat', 'name': 'Mittens', 'age': 2},
                {'species': 'Dog', 'name': 'Ralf', 'age': 2},
            ],
            msg="Expected response data to contain only the pets of age 2 from the Animal table"
        )

        #Filter on name
        response = client.get('http://localhost/pet/?name=BORIS')
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
            ],
            msg="Expected response data to contain only the pet named Boris from the Animal table"
        )

    def test_post(self):
        """
            Ensure post request can create a pet.
            And additional post requests will create another pet.
        """

        self.assertEqual(
            list(Animal.objects.all()),
            [],
            msg="Test pre-condition. Ensure animal table is empty."
        )

        client = APIClient()

        #First post
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

        #Second post
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


    def test_post_non_allowed_species_fails(self):
        """
            Ensure post fails when created species that is disabled
        """

        self.assertEqual(
            list(Animal.objects.all()),
            [],
            msg="Test pre-condition. Ensure animal table is empty."
        )

        client = APIClient()

        #First post
        response1 = client.post(
            'http://localhost/pet/', 
            data={'species': 'Bunny', 'name': 'Wiggles', 'age': 1}
        )

        self.assertEqual(
            response1.status_code,
            400,
            msg="Expected first post response code to be 400 - bad request"
        )

        self.assertEqual(
            json.loads(response1.data),
            {"species": ["Adding pet of species 'Bunny' is not allowed"]}
        )

        self.assertCountEqual(
            list(Animal.objects.all()),
            [],
            msg="Expected no animal to be created"

        )

    def test_get_non_allowed_species_succeeds(self):
        """
            Ensure get succeeds when a non-allowed species already exists in database
        """

        Animal.objects.create(species='Bunny', name='Froggle', age=3)


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
                {'species': 'Bunny', 'name': 'Froggle', 'age': 3},
            ],
            msg="Expected response data to contain the bunny from the Animal table"
        )
