# Example workflow
Mike searches for a restaurant, checks reviews, and saves it to his profile.

# Testing results
1. curl -X 'GET' \
  'https://fine-diners.onrender.com/restaurants/search/?price_max=2&sort_order=desc' \
  -H 'accept: application/json'
2. Response body
{
  "previous": null,
  "next": null,
  "results": [
    {
      "restaurant_id": 1,
      "name": "string",
      "location": "string",
      "cuisine": "string",
      "price_range": 0,
      "allergen_free_options": true,
      "allows_animals": true
    },
    {
      "restaurant_id": 3,
      "name": "string",
      "location": "string",
      "cuisine": "string",
      "price_range": 0,
      "allergen_free_options": true,
      "allows_animals": true
    },
    {
      "restaurant_id": 2,
      "name": "McDonalds",
      "location": "Madonna Rd",
      "cuisine": "High End Dining",
      "price_range": 10,
      "allergen_free_options": true,
      "allows_animals": true
    }
  ]
}

1. curl -X 'GET' \
  'https://fine-diners.onrender.com/reviews/search/?restaurant_name=McDonalds' \
  -H 'accept: application/json'
2. Response body
{
}

1. curl -X 'POST' \
  'https://fine-diners.onrender.com/profile/restaurants/2/' \
  -H 'accept: application/json' \
  -d ''
2. Response body
{
  "success": true
}


