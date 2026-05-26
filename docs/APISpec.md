# API Specification

## 1. Account Management

### 1.1 New Account - /accounts/ (POST)
Request:
```json
{
  "user_id": "string",
  "user_name": "string",
  "user_email": "string"
}
```
Response:
```json
{
  "user_id": "string"
}
```

### 1.2 Edit Account - /accounts/{user_id} (PUT)
Request:
```json
{
  "user_id": "string",
  "user_name": "string",
  "user_email": "string"
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 1.3 Get Account - /accounts/{user_id} (GET)
Response:
```json
{
  "success": "boolean"
}
```

### 1.4 Delete Account - /accounts/{account_id} (DELETE)
Request:
```json
{
  "user_id": "string",
  "user_name": "string",
  "user_email": "string"
}
```
Response:
```json
{
  "success": "boolean"
}
```

---

## 2. Review Management

### 2.1 Write Review - /reviews/{review_id} (POST)
Request:
```json
{
  "rating": "number",
  "description": "string",
  "food_quality_score": "number",
  "service_score": "number",
  "romantic_score": "number",
  "pricing_score": "number",
  "photos": ["string"]
}
```
Response:
```json
{
  "success": "boolean",
  "review_id": "integer"
}
```

### 2.2 Edit Review - /reviews/{review_id} (PUT)
Request:
```json
{
  "rating": "number",
  "description": "string",
  "food_quality_score": "number",
  "service_score": "number",
  "romantic_score": "number",
  "pricing_score": "number",
  "photos": ["string"]
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 2.3 Get Review - /reviews/{review_id} (GET)
Response:
```json
{
  "review_id": "integer",
  "rating": "number",
  "description": "string",
  "food_quality_score": "number",
  "service_score": "number",
  "romantic_score": "number",
  "pricing_score": "number",
  "photos": ["string"]
}
```

### 2.4 Delete Review - /reviews/{review_id} (DELETE)
Request:
```json
{
  "rating": "number",
  "description": "string",
  "food_quality_score": "number",
  "service_score": "number",
  "romantic_score": "number",
  "pricing_score": "number",
  "photos": ["string"]
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 2.5 Search Reviews - /reviews/search/ (GET)
Query Parameters:
- user_name (optional)
- restaurant_name (optional)
- search_page (optional)
- sort_col (optional): user_name, restaurant_name, timestamp
- sort_order (optional): asc, desc

Response:
```json
{
  "previous": "string",
  "next": "string",
  "results": [
    {
      "review_id": "integer",
      "review_name": "string",
      "user_name": "string",
      "timestamp": "string"
    }
  ]
}
```

---

## 3. Restaurant Management

### 3.1 Add Restaurant - /restaurants/ (POST)
Request:
```json
{
  "name": "string",
  "location": "string",
  "cuisine": "string",
  "price_range": "integer",
  "allergen_free_options": "boolean",
  "allows_animals": "boolean"
}
```
Response:
```json
{
  "success": "boolean",
  "restaurant_id": "integer"
}
```

### 3.2 Get Restaurant Details - /restaurants/search/ (GET)
Query Parameters:
- restaurant_name (optional)
- cuisine (optional)
- price_max (optional)
- allergen_free (optional)
- allows_animals (optional)
- min_pricing (optional)
- sort_col (optional): restaurant_name, timestamp
- sort_order (optional): asc, desc
- search_page (optional)

Response:
```json
{
  "previous": "string",
  "next": "string",
  "results": [
    {
      "restaurant_id": "integer",
      "name": "string",
      "location": "string",
      "cuisine": "string",
      "price_range": "integer",
      "allergen_free_options": "boolean",
      "allows_animals": "boolean",
      "average_rating": "number",
      "food_quality_score": "number",
      "service_score": "number",
      "romantic_score": "number",
      "pricing_score": "number"
    }
  ]
}
```

### 3.3 Complex Endpoint: Get Top Restaurants - /restaurants/top/ (GET)

Returns the top restaurants ranked by average review rating and food quality score. This endpoint is complex because it joins restaurants with reviews, calculates average scores, groups results by restaurant, and sorts restaurants by ranking.

Query Parameters:
- `limit` (optional): number of restaurants to return. Maximum value is 10.

Response:
```json
{
  "previous": null,
  "next": null,
  "results": [
    {
      "restaurant_id": "integer",
      "name": "string",
      "location": "string",
      "cuisine": "string",
      "price_range": "integer",
      "allergen_free_options": "boolean",
      "allows_animals": "boolean",
      "average_rating": "number",
      "food_quality_score": "number",
      "service_score": "number",
      "romantic_score": "number",
      "pricing_score": "number"
    }
  ]
}
```
### 3.4 Complex Endpoint: Restaurant Analytics - /restaurants/{restaurant_id}/analytics/ (GET)

Returns analytics for a specific restaurant. This endpoint is complex because it joins restaurants, reviews, reports, and owner replies to calculate summary statistics for the restaurant owner.

Response:
```json
{
  "restaurant_id": "integer",
  "restaurant_name": "string",
  "review_count": "integer",
  "average_rating": "number",
  "average_food_quality_score": "number",
  "average_service_score": "number",
  "average_romantic_score": "number",
  "average_pricing_score": "number",
  "report_count": "integer",
  "owner_reply_count": "integer"
}
```


---

## 4. Owner Interaction

### 4.1 Owner Reply - /reviews/{review_id}/reply (POST)
Request:
```json
{
  "user_id": "string",
  "reply": "string"
}
```
Response:
```json
{
  "reply_id": "string",
  "success": "boolean"
}
```



---

## 5. Review Censoring

### 5.1 Report Review - /reviews/{review_id}/report (POST)
Request:
```json
{
  "user_id": "string",
  "reason": "string"
}
```
Response:
```json
{
  "report_id": "string",
  "success": "boolean"
}
```

---

## 6. Profile Management

### 6.1 Get Profile - /profile/ (GET)
Request:
```json
{
  "user_id": "string",
  "user_name": "string",
  "saved_restaurants": ["restaurant_id"],
  "saved_reviews": ["review_id"]
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 6.2 Add Review to Profile - /profile/reviews/{review_id}/ (POST)
Request:
```json
{
  "review_id": "integer"
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 6.3 Add Restaurant to Profile - /profile/restaurants/{restaurant_id}/ (POST)
Request:
```json
{
  "restaurant_id": "integer"
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 6.4 Delete Review from Profile - /profile/reviews/{review_id}/ (DELETE)
Request:
```json
{
  "review_id": "integer"
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 6.5 Delete Restaurant from Profile - /profile/restaurants/{restaurant_id}/ (DELETE)
Request:
```json
{
  "restaurant_id": "integer"
}
```
Response:
```json
{
  "success": "boolean"
}
```

### 6.6 Delete Profile - /profile/ (DELETE)
Response:
```json
{
  "success": "boolean"
}
```

---

## 7. Audit Functions

### 7.1 Get Inventory Summary - /inventory/audit (GET)
Response:
```json
{
  "number_of_users": "number",
  "number_of_restaurants": "number",
  "number_of_reviews": "number"
}
```

---

## 8. Admin Functions

### 8.1 Reset Database - /admin/reset/ (POST)
Response:
```json
{
  "success": "boolean"
}
```
