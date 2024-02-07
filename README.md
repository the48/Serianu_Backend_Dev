Foreword.
The data source itself is built upon 5 public APIs, as required in the assessment requirements.
In as much as I was at liberty to choose these APIs at random, it made more sense to ensure that these were not simply picked without much thought. Therefore, the thought process was to assume that these could be used in a real-life scenario; perhaps for a mobile application. A good use case that comes to mind is a real-time feed of information about a given area, essentially one's own surroundings. One would be able to get information such as the weather, local time, likelihood of rainfall, relevant news in the area and so on.
That being said, the entire premise of the endpoints is built around the data that could be collected and or relevant to a particular location.
In order to build the data source itself, the user would need to enter a location and allow the underlying logic to carry out the rest of the processing. Note that this endpoint has been disabled, as it was mostly utilised to generate date into the store, and further simulate the scheduled task so as to have data to work with.


Setting Up.
All requirements are listed in the requirements.txt file, which allows for convenient installation of dependencies.
For this setup, PostgreSQL was used as the database.
Credentials have been stored in the ./core/Configs.py file, which can be edited for use in a different setup.
These include database and API authentication. Plaintext user credentials are dev:hireme4success.



Documentation.
Fortunately, API documentation is generated via Swagger, and can be accessed on http://localhost:8000/docs once the project has been set up. Descriptions for endpoints will be available for the same. Note that the project is REST based.
Some endpoints have been marked for authorisation, and will be required in the form of a JWT.