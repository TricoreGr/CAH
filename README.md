# IEEEdiots
![CAH](https://media.firebox.com/product/8322/extra3_column_grid_10/cards-against-humanity_29067.jpg)
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
    
## API Guide
    
| URI  | METHOD | ΕΝΕΡΓΕΙΑ | RETURN STATUS |  
| ------------- | ------------- | ------------- | ------------- |
| `/users/`  | GET | Επιστρέφει όλους τους χρήστες του παιχνιδιού | 200(OK), 500(SERVER ERROR) |
| `/users/`  | POST | Δημιουργεί έναν νέο χρήστη | 200(ΟΚ), 400(MISSING FIELDS), 500(SERVER ERROR) |
| `/users/{username}` | GET | Επιστρέφει τον συγκεκριμένο χρήστη | 200(OK), 500(SERVER ERROR) |
| `/users/{username}` | PUT | Ανανεώνει τα δεδομένα του συγκεκριμένου χρήστη | 200(OK), 401(UNAUTHORIZED), 500(SERVER ERROR) |
| `/users/{username}` | DELETE | Διαγράφει τον συγκεκριμένο χρήστη | 200(OK), 401(UNAUTHORIZED), 500(SERVER ERROR) |
| `/users/jwtToUsername` | POST | Επιστρέφει το username που αντιστοιχεί το token | 200(OK) |
| `/users/login` | POST | Επιστρέφει το token του χρήστη | 200(ΟΚ), 401(UNAUTHORIZED), 500(SERVER ERROR)
