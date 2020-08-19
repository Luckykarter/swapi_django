Endpoints description:

- `exhaust_port/xwings/`
    - GET - returns JSON with description of all XWings in database
    - POST - adds XWing in database from provided JSON
- `exhaust_port/defence_towers/`
    - GET - returns JSON with description of all Defense Towers in database
    - POST - adds Defense Tower in database from provided JSON
- `exhaust_port/defence_towers/<tower_id>`
    - GET - returns JSON with description of Defense Tower with given ID
    - DELETE - destroys the Defense Tower with given ID (sets health of tower to zero)
- `exhaust_port/defence_towers/xwings/<xwing_id>`
    - GET - returns JSON with description of all Defense Towers that targeting XWing with given XWing_id
- `exhaust_port/defence_towers/xwings/my`
    - GET - returns JSON with description of all Defense Towers that targeting the current user. 
    Login information of request is used to retrieve the user.
    - DELETE - destroys all Defense Towers that targeting the current user
- `exhaust_port/starships/`
    - GET - returns JSON with description of all Starships in database
    - POST - adds Starship in database from provided JSON
- `exhaust_port/species/starships/<starship_id>`
    - GET - returns JSON with description of all Species that seen the given Starship with starship_ID
    Species are resolved by film where the Starship appeared 
- `exhaust_port/species/starships/producers/<producer name>`
    - GET - returns JSON with description of all Species that seen Starships from
    the movies that were produced by given producer name.
- `exhaust_port/evacuate_planet/<planet_id>/starships/<starship_id>`
    - GET - returns JSON with short description of the given planet/starship and number 
    of the given starships required to evacuate the given planet in tag `ships_needed`. If evacuation is not possible
    the descriptive error message will be returned.

