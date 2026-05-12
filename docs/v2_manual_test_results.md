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



# Example workflow
Alice is a restaurant owner who wants to monitor feedback and interact with customers.

# Testing results
1. curl -X 'GET' \
  'https://fine-diners.onrender.com/reviews/search/?restaurant_name=McDonalds' \
  -H 'accept: application/json'
2. Response body
{
  "previous": null,
  "next": null,
  "results": [
    {
      "review_id": 3,
      "review_name": "Great food and service",
      "user_name": "test_user",
      "timestamp": "2026-05-10T18:25:43"
    },
    {
      "review_id": 4,
      "review_name": "Decent but overpriced",
      "user_name": "test_user",
      "timestamp": "2026-05-09T14:12:10"
    }
  ]
}

1. curl -X 'POST' \
  'https://fine-diners.onrender.com/reviews/3/reply' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "owner_1",
  "reply": "Thank you for your feedback!"
  }'
2. Response body
{
  "reply_id": 1,
  "success": true
}

1. curl -X 'POST' \
  'https://fine-diners.onrender.com/reviews/3/report' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "owner_1",
  "reason": "Inappropriate content"
  }'
2. Response body
{
  "report_id": 1,
  "success": true
}
