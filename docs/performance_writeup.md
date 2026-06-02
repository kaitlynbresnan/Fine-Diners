# Fake Data Modeling
The fake data for our service was generated using a Python script called [generate_fake_data.py](https://github.com/kaitlynbresnan/Fine-Diners/blob/main/scripts/generate_fake_data.py). The script uses the Faker library to generate realistic restaurant names, locations, review text, and user identifiers. Randomized values were used for ratings, cuisine types, report reasons, and restaurant attributes.

Data Distribtuion:
| Table | Number of Rows |
| --- | --- |
| Restaurants | 10,000 |
| Reviews | 900,000 |
| Review Reports | 50,000 |
| Owner Replies | 20,000 |
| Saved Restaurants | 20,000 |
| Total | 1,000,000 |

We chose this distribution because a restaurant review platform will naturally contain far more reviews than restaurants. A restaurant may receive hundreds or thousands of reviews, making the reviews table the largest and fastest growing table in the system. 

The Review Reports table contains fewer rows because only a small percentage of reviews are reported by users. Similarly, the Owner Replies table contains fewer rows because restaurant owners don't respond to every review. The Saved Restaurants table is also relatively small because users typically browse many restaurants but save only a subset of them for future reference. 

This distribution creates a realistic workload for a restaurant review service while also providing sufficient data to test search queries, joins, aggregations, and more. 


# Performance Results of Hitting Endpoints
After generating approximately 1,000,000 rows of data in our local PostgreSQL database, we tested the performance of several API endpoints. Endpoint execution times were measured using the Unix `time` command while making requests against the local API instance.

| Endpoint | Execution Time |
| --- | --- |
| GET /restaurants/top | 220 ms |
| GET /restaurants/1/analytics | 71 ms |
| GET /reviews/search | 174 ms |
| GET /reviews/1 | 67 ms |
| POST /reviews/1/reply | 56 ms |
| POST /reviews/1/report | 30 ms |
| GET /profile/?user_id=user_1 | 15 ms |
| DELETE /profile/restaurants/1 | 49 ms |

The slowest endpoint was: `GET /restaurants/top/?limit=10` with an execution time of approximately 220 ms.

This was expected because the endpoint performs a join between the `restaurants` and `reviews` tables, computes multiple aggregate values using `AVG()`, groups results by restaurant, sorts the aggregated data, and returns the highest rated restaurants. Since the `reviews` table contains 900,000 rows, this endpoint performs more work than the others. 


# Performance Tuning


