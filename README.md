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

### Users api    
| URI  | METHOD | ΕΝΕΡΓΕΙΑ | RETURN STATUS |  
| ------------- | ------------- | ------------- | ------------- |
| `/users`  | GET | Επιστρέφει όλους τους χρήστες του παιχνιδιού, `returns users` | 200(OK), 500(SERVER ERROR) |
| `/users`  | POST | Δημιουργεί έναν νέο χρήστη, `returns user, token`| 200(ΟΚ), 400(MISSING FIELDS), 500(SERVER ERROR) |
| `/users/{username}` | GET | Επιστρέφει τον συγκεκριμένο χρήστη, `returns user`| 200(OK), 500(SERVER ERROR) |
| `/users/{username}` | PUT | Ανανεώνει τα δεδομένα του συγκεκριμένου χρήστη, `returns user` | 200(OK), 401(UNAUTHORIZED), 500(SERVER ERROR) |
| `/users/{username}` | DELETE | Διαγράφει τον συγκεκριμένο χρήστη, `returns user` | 200(OK), 401(UNAUTHORIZED), 500(SERVER ERROR) |
| `/users/jwtToUsername` | POST | Επιστρέφει το username που αντιστοιχεί το token, `returns user` | 200(OK) |
| `/users/login` | POST | Επιστρέφει το token του χρήστη, `returns user, token` | 200(ΟΚ), 401(UNAUTHORIZED), 500(SERVER ERROR)

#### User model in mysql
```
User : 
        username
        password
        email
        img
        games
        wins
```

#### User return from API
```json
    users {
        "username" : "some username",
        "email" : "some email",
        "img" : "some img",
        "game" : "some games",
        "wins" : "some wins"
    }
```

### Room API
| URI | METHOD | ΕΝΕΡΓΕΙΑ | RETURN STATUS |
| ------------- |  ------------- | ------------- | ------------- |
| `/game` | GET | Επιστρέφει όλα τα διαθέσιμα rooms, `returns rooms` | 200(OK), 500(SERVER ERROR) |
| `/game` | POST | Δημιουργεί νέο room, `returns room` | 200(OK), 500(SERVER ERROR) |
| `/game` | DELETE | Διαγράφει το room που δημιούργησε το room, `returns room` | 200(OK), 500(SERVER ERROR) |
| `/game/{roomID}/round/whitecards` | GET | Επιστρέφει τις λευκές κάρτες του συγκεκριμένου room για το συγκεκριμένο room, `returns white cards` | 200(OK) , 500(SERVER ERROR) |
| `/game/{roomID}/round/whitecards` | POST | Δηλώνει ποια κάρτα έπαιξε ο χρήστης και επιστρέφει ένα απλό μήνυμα, `returns message` | 200(OK), 500(SERVER ERROR) |
| `/game/{roomID}/round/czar` | GET | Επιστρέφει τον czar του room, `returns czar` | 200(OK), 500(SERVER ERROR) |
| `/game/{roomID}/round/blackcard` | GET | Επιστρέφει μία μαύρη κάρτα , `returns blackcard` | 200(OK), 500(SERVER ERROR) |
| `/game/{roomID}/players` | GET | Επιστρέφει τους παίχτες του room, `returns players` | 200(OK), 500(SERVER ERROR) |
| `/game/{roomID}/players/{username}/whitecards` | GET | Επιστρέφει τις λευκές κάρτες του δεδομένου παίχτη, `returns whitecards` | 200(OK), 500(SERVER ERROR)

#### White Card model
```
    whiteCard = "Some text"
```
#### Black Card model
```json
    blackCard {
        "pick" : "1 or 2",
        "text" : "Some text"
    }
```
#### Room model 
```json
    room {
        "owner" : "owner's_name",
        "gamesession" : {
            "round" : {
                "czar" : "czar's_name",
                "blackCard": {"pick":"1 or 2","text":"Some Text"},
                "whiteCards": ["Some text","Some more text"]
            },
            "players" : [
                {
                    "username": "username",
                    "points" : "Number of points",
                    "whiteCards" : ["Some text","Some more text"]
                }
            ],
           "cards": {
                "blackCards" : [{"pick":"1 or 2", "text":"Some text"},{"pick":"1 or 2", "text":"Some more text"}],
                "whiteCards" : ["Some text","Some more text"]
           }
        }
    }
```
## Thanks to
   1. Our professors for allowing us to make such a masterpiece
   2. Hell energy drinks
   3. Antidepressants
