# Juvo

django 2.0.5

# Set database
```python

python manage.py migrate

```

Set how many category you want to crawl in yahoo_crawler.py
default is 5

# Crawler
```python

python yahoo_crawler.py

```

# Run Server
```python

python manage.py runserver

```

本地端
<localhost:8000/yahoo>

# Query
```sqlite3

select category, count(*) from yahoo_product group by category

```
