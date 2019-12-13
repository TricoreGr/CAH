# ieeediots
Cards against humanity online game 

## In order to run:

1. Fork/Clone

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3 -m venv venv
    $ source venv/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ python run.py
    ```

    Navigate to [http://localhost:5000](http://localhost:5000)

1. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    Navigate to [http://localhost:8080](http://localhost:8080)
