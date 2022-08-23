# ML soccer predictions

This project aims for soccer predictions regarding Europe's big five leagues Premier League, La Liga, Bundesliga, Serie A and Ligue 1. The predictions are based on supervised ML and uses data starting from season 2017/2018.

As an evaluation metrik Brier-score is used, which is a good indicator for checking an advantage against anybody else, e. g. the bookie. The Brier-score is better the lower it gets and can be calculated for multiclass classification as

<PRE>
>>> import numpy as np
>>> predicted_probabilities = [
...     [0.5, 0.3, 0.1],
...     [0.8, 0.1, 0.1],
...     [0.3, 0.3, 0.4],
...     [0.1, 0.4, 0.5],
...     [0.2, 0.3, 0.5],
...     [0.7, 0.2, 0.1],
...     [0.2, 0.2, 0.6],
...     [0.1, 0.7, 0.2],
... ]
>>> 
>>> actual_result = [
...     [1, 0, 0],
...     [1, 0, 0],
...     [0, 0, 1],
...     [0, 1, 0],
...     [1, 0, 0],
...     [0, 0, 1],
...     [0, 0, 1],
...     [0, 1, 0],
... ]
>>> 
>>> brier_score = np.mean(
...     np.sum(np.square(np.array(predicted_probabilities) - np.array(actual_result)), axis=1)
... )
>>> 
>>> print(brier_score)
0.5337500000000001
>>>
</PRE>

Therefore for predictions probabilities for classes (scikit-learn's predict_proba(X)) are rather used than actual classes (scikit-learn's predict(X)).

The project offers a semi-automated controller implemented in **00_a_production.ipynb**, which follows (more or less strict) all the typical ML steps from collecting and preparing data over over choosing, training and evaluating the model over parameter tuning to making actual predictions. The controller can be run before each matchday to get proper result using the latest available data.

More testing and real world simulations with different strategies are implemented in **01\_\*** notebooks.

### Important

If you can find a configuration (classifier and hyperparameter) in **step_05** from **00_a_production.ipynb**, which result in a score < 0.57 (yes, smaller!!!), let me know. We could get rich together ;). Hint: There is no need to run the previous steps, as the data is already scraped and pre-processed.

### Data

##### Raw data

- base.csv/base_update.csv -> https://fbref.com/en/squads/{link}
- additional.csv -> http://www.football-data.co.uk/germanym.php
- coaches.csv -> https://www.weltfussball.de/teams/{link}/9/
- promotions.csv -> http://www.trainer-baade.de/alle-aufsteiger-in-die-1-bundesliga/

##### Synthetic data

- production.csv/production_update.csv -> merged raw data enriched with feature engineering
- model.csv -> data prepared for ML models
- games.csv -> upcoming games
- prediction.csv -> results

### Technical prerequisites

The scraper is implemented with Selenium and uses Chrome (https://chromedriver.chromium.org/downloads) and AdblockPlus-extension. Make sure you set it up properly in **steps/step_01.py**.

### Usage and maintenance

To the best of my knowledge, all data for all games and sources is available and therefore can be scraped around noon the following day. Just run **00_a_production.ipynb** and make sure you have no errors ;).

It's recommend to scrape all sources completely (base_update.csv) and compute all features for all seasons (production_update.csv) at the beginning of each season. This can be handled with

- **no_of_seasons**-parameter in **step_01** set to _current season starting year - 2017_.
- **starting_season**-parameter in **step_03** set to _2017_

base.csv and production.csv should be empty on a full run. After that they can be set to 1 respectively _current season starting year_.

Futhermore one should do:

- update sources/data/promotions.csv every season
- update modules/translator.ods every season in case of upcomming unknown teams

### Conclusion

I could not get satisfying results. But if you are interested and have any questions, please don't hesitate to contact me! It would be a pleasure for me to keep this project alive.

### More ideas:

- implement feature **Weather** for each city
- implement feature **Numeric_Feature_Home_Against_Same_Team_Last_OFFSET_Games**
- implement reinforcement learning
  - libraries: Stable Baselines, Tensorforce, RL_Coach
  - models: DQN or ACER for "Discrete Actions - Single Process" --> 'H', 'D', 'A'

### Similar projects:

- https://github.com/Caldass/pl-matches-predictor
- https://content.iospress.com/articles/journal-of-sports-analytics/jsa200463
