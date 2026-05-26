# Concurrency Control

## 1. Lost Update / Write Skew: Two Users Report the Same Review

Our service allows users to report reviews using `POST /reviews/{review_id}/report`. A possible future rule is that once a review receives a certain number of reports, it should be hidden or flagged for moderation. If two users report the same review at the same time, both transactions might read the same current report count before either report is committed. This could cause the system to make the wrong moderation decision.

For example, suppose a review already has 2 reports and the threshold for hiding a review is 3 reports. Two users report the review at the same time. Both transactions might read that the review has 2 reports. Then both insert a new report, but neither transaction correctly handles the fact that the review has crossed the threshold.

```mermaid
sequenceDiagram
    participant UserA
    participant UserB
    participant API
    participant DBMS
    participant Reviews
    participant Reports

    UserA->>API: POST /reviews/10/report
    API->>DBMS: Begin T1
    DBMS->>Reports: T1 counts 2 reports for review 10

    UserB->>API: POST /reviews/10/report
    API->>DBMS: Begin T2
    DBMS->>Reports: T2 counts 2 reports for review 10

    DBMS->>Reports: T1 inserts report
    DBMS-->>API: Commit T1
    API-->>UserA: Report submitted

    DBMS->>Reports: T2 inserts report
    DBMS-->>API: Commit T2
    API-->>UserB: Report submitted

    Note over Reviews,Reports: Review now has 4 reports, but moderation status may not be updated correctly
```
