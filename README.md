# orkestra_project

# 1. Setup
    1. pip install -r requirements.txt
    2. python pets/manage.py migrate

# 2. Running Server
    1. python pets/manage.py runserver

# 3. Running Tests
    1. python pets/manage.py test animals

# 4. Further information
    - Most of the code of interest is in pets/animals (pets/pets is mostly boilerplate django)
        - Particularly views.py, urls.py, models.py, serializers.py, constants.py and test/test_apis.py
    - The requirement/note in the instructions that "allowed species will be added and removed regularly", really needed more scoping out, so I just went with the simplest solution.
       - I asummed any changes to allowed species would be in code and would only affect adding pets, not viewing pets, nor affect existing pets in the database.
       - Also I assumed the list of all species would never be removed from
    - Post adding multiple pets at once would make a lot of sense, but it didn't seem to be required. It would not be a difficult change