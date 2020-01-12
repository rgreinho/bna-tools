# Advancement

## Street by street

It is not straightforward to monitor the progress of the tagging, especially at the scale of the city.

The first idea was to use the streets of the city as a completion indicator:

1. Collect all the streets of the city
2. Group them by zipcode
3. Assign streets or zipcode to groups
4. Each street will be tagged by a mapper AND reviewed by **another** mapper
5. Mark the status as "Done" ( ✅).

### Method validation

To test wether or not this approach is valid, I propose to run a first test with the 20 most bikeable streets in the city:

| Street Name             | Mapper  | Reviewer | Status|
|-------------------------|:-------:|:--------:|:-----:|
| 3rd Street              | Luis A. | Rémy G.  | ✅    |
| Arroyo Seco             | Rémy G. |          |       |
| Berkman Drive           | Rémy G. |          |       |
| Cherrywood Road         | Rémy G. |          |       |
| Chesnut Avenue          |         |          |       |
| Chicon Street           |         |          |       |
| Clyde Littlefield Drive |         |          |       |
| Comal Street            |         |          |       |
| Denson Drive            |         |          |       |
| E. M Franklin Avenue    | Rémy G. |          |       |
| Guadalupe Street        |         |          |       |
| Maor Road               |         |          |       |
| Pedernales Street       |         |          |       |
| Red River Street        | Rémy G. |          |       |
| Rio Grande Street       |         |          |       |
| San Jacinto boulevard   |         |          |       |
| Speedway                |         |          |       |
| Tiley Street            |         |          |       |
| Trinity Street          |         |          |       |
| Zach Schott Street      | Rémy G. |          |       |
