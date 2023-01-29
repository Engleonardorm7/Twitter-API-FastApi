
## Twitter API

This project is a REST API made with FastAPI for learning purposes.

### Features
Features included:
- Data modeling with pydantic.
- Data validation.
- CRUD of users.
- CRUD of Tweets.
- Data persistance with JSON files (JSON files as database)


## Requirements:
- Python >= 3.10

## Installing
1. Clone or download de repository:
    ```
    $ git clone git@github.com:Engleonardorm7/Twitter-API-FastApi.git
    ```

2. Open the console inside the project directory and create a virtual environment.
    ```bash
    $ python -m venv venv
    $ source venv/Scripts/activate
    ```

3. Install the app
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

## Run it locally
```
(venv) $ uvicorn main:app --reload
```

## Basic Usage
Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.

## Authors
Leonardo Rodriguez - [Github Profile](https://github.com/Engleonardorm7)

## Additional notes
The code is a simple program and is not intended for production use. It serves only as an example of basic FastAPI concepts.