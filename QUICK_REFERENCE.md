# Quick Reference Card - ELK Stack for Banking Logs

## URLs

- Kibana: http://localhost:5601
- Elasticsearch: http://localhost:9200
- Logstash: http://localhost:9600

## Common Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f elasticsearch
docker-compose logs -f logstash
docker-compose logs -f kibana

# Restart a service
docker-compose restart kibana

# Check status
docker-compose ps
```

## Generate Logs

```bash
# 10,000 logs (default)
python generate_logs.py

# 50,000 logs
python generate_logs.py -n 50000

# Custom output file
python generate_logs.py -o logs/custom.log -n 20000
```

## Elasticsearch Commands

```bash
# Cluster health
curl http://localhost:9200/_cluster/health?pretty

# List all indices
curl http://localhost:9200/_cat/indices?v

# Count documents
curl http://localhost:9200/banking-logs-*/_count?pretty

# Delete all banking logs
curl -X DELETE http://localhost:9200/banking-logs-*

# Get mapping
curl http://localhost:9200/banking-logs-*/_mapping?pretty
```

## Common KQL Queries (Use in Kibana Discover)

```kql
# Failed transactions
status: "failed"

# Suspicious or fraud
suspicious: true OR is_fraud: true

# Large amounts
amount > 10000

# Failed authentication
transaction_type: "authentication" AND status: "failed"

# Brute force attacks
is_brute_force: true

# Specific currency
currency: "USD"

# ATM operations
transaction_type: "atm"

# Slow operations
response_time_ms > 1000

# Specific country
country: "UA"

# Date range
@timestamp >= "2024-10-01" AND @timestamp <= "2024-10-31"

# Multiple conditions
transaction_type: "transaction" AND amount > 5000 AND status: "success"

# International transfers
transaction_type: "transfer" AND transfer_type: "international"

# Failed high-value transactions
amount > 5000 AND status: "failed"

# Specific user activity
user_id: "user_0042"

# Merchant category
merchant_category: "retail"
```

## Aggregation Examples (Dev Tools)

```json
# Statistics on transaction amounts
GET banking-logs-*/_search
{
  "size": 0,
  "aggs": {
    "amount_stats": {
      "stats": {
        "field": "amount"
      }
    }
  }
}

# Top 10 countries by transaction count
GET banking-logs-*/_search
{
  "size": 0,
  "aggs": {
    "top_countries": {
      "terms": {
        "field": "country.keyword",
        "size": 10
      }
    }
  }
}

# Average response time by service
GET banking-logs-*/_search
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": {
        "field": "service.keyword"
      },
      "aggs": {
        "avg_response": {
          "avg": {
            "field": "response_time_ms"
          }
        }
      }
    }
  }
}

# Transaction volume over time (hourly)
GET banking-logs-*/_search
{
  "size": 0,
  "aggs": {
    "over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "1h"
      }
    }
  }
}

# Failed transactions by type
GET banking-logs-*/_search
{
  "size": 0,
  "query": {
    "term": {
      "status.keyword": "failed"
    }
  },
  "aggs": {
    "by_type": {
      "terms": {
        "field": "transaction_type.keyword"
      }
    }
  }
}
```

## Visualization Types Quick Guide

| Visualization | Best For | Example Use |
|---------------|----------|-------------|
| **Line** | Trends over time | Transaction volume timeline |
| **Bar** | Comparisons | Top merchants, countries |
| **Pie** | Proportions | Status distribution |
| **Metric** | KPIs | Total count, averages |
| **Data Table** | Detailed lists | Top users, transactions |
| **Heat Map** | Patterns | Failed logins by IP/time |
| **Maps** | Geographic data | Transaction locations |
| **TSVB** | Complex time series | Multiple metrics over time |

## Common Filters

| Filter | Description |
|--------|-------------|
| `exists: amount` | Records with amount field |
| `NOT status: "success"` | Exclude successful transactions |
| `amount: [1000 TO 5000]` | Range filter |
| `transaction_type: ("transaction" OR "transfer")` | Multiple values |

## Field Types in Index

| Field | Type | Description |
|-------|------|-------------|
| @timestamp | date | Event timestamp |
| transaction_type | keyword | Type of transaction |
| amount | float | Transaction amount |
| status | keyword | Transaction status |
| client_ip | ip | Client IP address |
| response_time_ms | integer | Response time |
| suspicious | boolean | Fraud indicator |
| user_id | keyword | User identifier |

## Dashboard Best Practices

1. **Top Row**: KPIs (metrics) - total count, success rate, etc.
2. **Second Row**: Time series - trends over time
3. **Third Row**: Distributions - pie charts, bar charts
4. **Fourth Row**: Details - tables, maps
5. **Use filters**: Add global filters to dashboard
6. **Time picker**: Enable time range selector

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| No data in Kibana | Check time range (try "Last 7 days") |
| Can't create data view | Wait for Elasticsearch to index data |
| Slow queries | Reduce time range, add filters |
| Container won't start | Check Docker logs: `docker-compose logs [service]` |
| Out of memory | Reduce Java heap size in docker-compose.yml |

## Data View Setup (First Time)

1. Kibana → Stack Management → Data Views
2. Create data view
3. Name: `banking-logs`
4. Index pattern: `banking-logs-*`
5. Timestamp: `@timestamp`
6. Save

## Useful Keyboard Shortcuts (Kibana)

- `Ctrl/Cmd + /` - Toggle sidebar
- `Ctrl/Cmd + K` - Search
- `Ctrl/Cmd + Enter` - Run query (Dev Tools)

## Sample Analysis Questions

1. What is the total transaction volume?
2. What percentage of transactions fail?
3. Which country has the most suspicious activity?
4. What is the average response time per service?
5. Which users have the most failed login attempts?
6. What time of day sees the most transactions?
7. Which merchant category is most popular?
8. Are there any patterns in fraudulent transactions?

## Log Data Structure

```json
{
  "timestamp": "2024-10-21 10:30:45",
  "transaction_type": "transaction",
  "transaction_id": "TXN1234567",
  "user_id": "user_0042",
  "amount": 250.50,
  "currency": "USD",
  "status": "success",
  "client_ip": "192.168.1.100",
  "country": "US",
  "response_time_ms": 245,
  "suspicious": false
}
```

## Performance Tips

- Use specific time ranges (not "All time")
- Apply filters before creating visualizations
- Use keyword fields for aggregations
- Limit result size for tables
- Close unused browser tabs
- Refresh dashboards manually when needed

---

Keep this reference handy while working with the ELK stack!
