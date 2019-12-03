# movapi
Retrieve information about any movie from IMDB.  

Following example queries on IMDB id: 
```python
from movapi import Movie
imdbID = 'tt1375666'
m = Movie.imdb_id(imdbID)
```
Result:

```json
{ "imdbID": "tt1375666", "title": "Inception", "year": "2010", "stars": [ "Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page" ], "actors": [ "Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page", "Tom Hardy", "Ken Watanabe", "Dileep Rao", "Cillian Murphy", "Tom Berenger", "Marion Cotillard", "Pete Postlethwaite", "Michael Caine", "Lukas Haas", "Tai-Li Lee", "Claire Geare", "Magnus Nolan" ], "characters": { "Leonardo DiCaprio": "Cobb", "Joseph Gordon-Levitt": "Arthur", "Ellen Page": "Ariadne", "Tom Hardy": "Eames", "Ken Watanabe": "Saito", "Dileep Rao": "Yusuf", "Cillian Murphy": "Robert Fischer", "Tom Berenger": "Browning", "Marion Cotillard": "Mal", "Pete Postlethwaite": "Maurice Fischer", "Michael Caine": "Miles", "Lukas Haas": "Nash", "Tai-Li Lee": "Tadashi", "Claire Geare": "Phillipa (3 years)", "Magnus Nolan": "James (20 months)" }, "directors": [ "Christopher Nolan" ], "production_company": [ "Warner Bros.", "Legendary Entertainment", "Syncopy" ], "writers": [ "Christopher Nolan" ], "genres": [ "Action", "Adventure", "Sci-Fi" ], "duration": [ "2h 28min", "148 min" ], "plot_short": "A thief, who steals corporate secrets through the use of dream-sharing technology, is given the inverse task of planting an idea into the mind of a CEO.", "plot_long": "Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state, when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted player in this treacherous new world of corporate espionage, but it has also made him an international fugitive and cost him everything he has ever loved. Now Cobb is being offered a chance at redemption. One last job could give him his life back but only if he can accomplish the impossible - inception. Instead of the perfect heist, Cobb and his team of specialists have to pull off the reverse: their task is not to steal an idea but to plant one. If they succeed, it could be the perfect crime. But no amount of careful planning or expertise can prepare the team for the dangerous enemy that seems to predict their every move. An enemy that only Cobb could have seen coming.", "rating": { "value": "8.8", "count": "1,687,105", "best": "10" }, "awards": [ "Won 4 Oscars", "Another 152 wins & 203 nominations" ], "poster_url": "https://ia.media-imdb.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_UX182_CR0,0,182,268_AL_.jpg", "content_rating": "PG-13", "metascore": "74" }
```


Following example search movie titles: 
```python
from movapi import Movie
title = 'Inception'
t = Movie.search_title(title, count=2)
```

Retrieves a list of movies related to title
