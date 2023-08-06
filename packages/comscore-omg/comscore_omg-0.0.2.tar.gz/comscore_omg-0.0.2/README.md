# Omnicom media group | Comscore Library

Under construction!

Developed by Carlos Trujillo, Data Analytics Manager from Omnicom Media Group Chile (c) 2021

## Examples (How To Use)

Connection to Comscore data bases

```python
from omnicom_comscore_queries import comscore_omnicom_api

comscore = comscore_omnicom_api(user = 'user_name', password = 'password_value')
```

Executing the first query to obtain the total visits in time from different domains.
```python

from omnicom_comscore_queries import comscore_omnicom_api

comscore = comscore_omnicom_api(user = 'user_name', password = 'password_value')

dataframe_time = comscore.domain_by_time(country = 'cl')
```

Calculate the probability of visiting the next site, after visiting a specific domain.
```python

from omnicom_comscore_queries import comscore_omnicom_api

comscore = comscore_omnicom_api(user = 'user_name', password = 'password_value')

results_over_40_percent, full_dataframe = comscore.bayesian_site_predictor(country_in = 'cl', start_date_in = '2021-01-01', 
                                                                            domain_in = 'sodimac.cl', time_spent_in = 300)
```