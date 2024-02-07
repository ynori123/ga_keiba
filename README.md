### ER図
```mermaid
erDiagram
  
  races ||--|| states : "has one"
  races ||--|{ horses : "has many"
  horses ||--|| jockeys : "has one"
  horses {
    int id PK
    int race_id FK
    int jockey_id FK
    int frame_number
    int arrival
    string name
    float odds
    int popularity
    int handicap 斤量
    int weight
    int age
    int sex_id 1: 牡, 2: 牝, 3: セ
  }

  jockeys {
    int id PK
    string name
  }
  races {
    string id PK レースID(netkeibaと対応)
    int state_id FK
    string name
    str course
    bool is_dart ダートor芝
    bool is_right 右回りor左回り
    int distance
    string weather
  }
  states {
    int id PK
    string name
  }

```
