# Concurrency Control

## Case 1: Two users report the same review at the same time

### Problem
Two users could report the same review at the same time. Without concurrency control, both transactions may read the same original report count and fail to correctly update the review if it reaches the report threshold.

