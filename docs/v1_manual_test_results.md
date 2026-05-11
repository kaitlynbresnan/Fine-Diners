# Example workflow
Sally visits a restaurant and wants to leave a review.

# Testing results
1. curl -X 'POST' \
  'https://fine-diners.onrender.com/reviews/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "rating": 0,
  "description": "string",
  "food_quality_score": 0,
  "service_score": 0,
  "romantic_score": 0,
  "pricing_score": 0,
  "photos": []
  }'
2. Response body
{
  "success": true,
  "review_id": 3
}

1. curl -X 'PUT' \
  'https://fine-diners.onrender.com/reviews/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "rating": 0,
  "description": "string",
  "food_quality_score": 0,
  "service_score": 0,
  "romantic_score": 0,
  "pricing_score": 0,
  "photos": []
  }'
2. Response body
{
  "success": true
}

1. curl -X 'GET' \
  'https://fine-diners.onrender.com/reviews/3' \
  -H 'accept: application/json'
2. Response body
{
  "review_id": 3,
  "rating": 0,
  "description": "string",
  "food_quality_score": 0,
  "service_score": 0,
  "romantic_score": 0,
  "pricing_score": 0,
  "photos": "",
  "created_at": "2026-05-04T21:17:09.021024",
  "updated_at": "2026-05-04T21:18:42.435290"
}

1. curl -X 'DELETE' \
  'https://fine-diners.onrender.com/reviews/3' \
  -H 'accept: application/json'
2. Response body
{
  "success": true
}
