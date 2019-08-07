UI = https://fuzzyauto.heroku.app.com/
Endpoint = https://fuzzyauto.herokuapp.com/search?word=<word>

GET call returns a dictionary with ranks as keys and words as values, rendered visually as a table. Returns first 25 ranks.

Criteria for ranking:
    The ranking of results satisfies the following conditions in decreasing order of precedence:
	a. Matches at the start of a word are ranked higher. 
	b. Common words (those with a higher usage count) are ranked higher than rare words.
	c. Short words rank higher than long words. 
	i. As a corollary to the above, an exact match is always ranked as the first result.
