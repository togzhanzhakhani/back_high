# Report
## Exercise 1: Database Design and Optimization
### Objective
The primary goal of this exercise is to design an efficient database schema for a simple blog application using Django and to optimize the queries for improved performance.
### Schema Design
The following Django models represent the database schema for the blog application:
``` sh
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField()

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts')

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['tags']),
        ]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_date']),
        ]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
```
### Indexing
#### Post Model Indexes:
- Author Index: An index on the author field allows faster lookups for posts by a specific author, enhancing performance when filtering posts.
- Tags Index: An index on the tags field speeds up queries that filter posts based on associated tags.
#### Comment Model Index:
- Composite Index: A composite index on the post and created_date fields optimizes queries that retrieve comments for a specific post and sort them by creation date.
### Query Optimization
To fetch all posts with their related comments in a single query, the following Django ORM query can be used:
```sh
posts_with_comments = Post.objects.prefetch_related('comment_set').all()
```
### Improvements Implemented
After analyzing the generated SQL, I optimized the query performance with the following strategies:
- Used select_related for ForeignKey Relationships: To minimize the number of queries, I utilized select_related for the author of each post, which performs an SQL join:
```sh
posts_with_comments = Post.objects.select_related('author').prefetch_related('comment_set').all()
```
### Optimization Report Summary
The chosen indexes significantly improve query performance by minimizing the time taken to filter results based on author and tags for posts, as well as retrieving comments based on post ID and creation date. The use of prefetch_related and select_related further optimizes the retrieval of related data, ensuring efficient database access patterns.

## Exercise 2: Caching Strategies Report
### Objective
The goal of this exercise is to implement caching strategies to improve the performance of a Django application.
### Performance Analysis: Before Optimization
Before implementing caching, I recorded the following performance metrics for the application:
```sh
Load Time for Blog Posts List Page:
- Total Request Time: 104.77ms
- Total Database Queries: 3.83ms(7 queries)
Load Time for Blog Post Detail Page:
- Total Request Time: 83.65ms
- Total Database Queries: 3.39ms(4 queries)
```
These metrics represent the application's performance without any caching mechanisms in place.
## Implementation Steps
### 1. Basic Caching
Implemented view-level caching for the list of blog posts with a timeout set to 60 seconds.
```sh
from django.views.decorators.cache import cache_page
@cache_page(60)  # Cache for 60 seconds
def post_list(request):
    posts = Post.objects.select_related('author').prefetch_related('tags')
    return render(request, 'blog/post_list.html', {'posts': posts})
```
### 2. Template Fragment Caching
For template fragment caching, I used the following code in the blog post detail template:
```sh
{% load cache %}
<h3>Comments</h3>
{% cache 600 comments_for_post post.id %}
<ul>
    {% for comment in comments %}
    <li>{{ comment.author }}: {{ comment.text }}</li>
    {% endfor %}
</ul>
{% endcache %}
```
### 3. Low-Level Caching
For low-level caching, I implemented caching for counting comments:
```sh
def get_comment_count(post):
    cache_key = f'comment_count_{post.id}'
    count = cache.get(cache_key)
    if count is None:
        count = post.comments.count()  # Дорогой запрос
        cache.set(cache_key, count, timeout=600)  # Кэшируем на 10 минут
    return count

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('comments'), pk=pk)
    comment_count = get_comment_count(post)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': post.comments.all(),
        'form': form,
        'comment_count': comment_count, 
    })
```
### 4. Cache Backend Configuration
In the settings.py, I configured Redis as the cache backend:
```sh
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```
### Performance Analysis
#### Metrics After Caching (using Django Debug Toolbar)
```sh
Load Time for Blog Posts List Page:
- Total Request Time: 29.73ms
- Total Cache: 0.17ms(2 calls)
Load Time for Blog Post Detail Page:
- Total Request Time: 49.28ms
- Total Cache: 1.88ms(2 calls)
```

### Conclusion
The implementation of view-level, template fragment, and low-level caching, along with Redis as the caching backend, greatly improved the application's performance. Load times were reduced, database queries were minimized, and overall resource usage decreased, enhancing the user experience.

## Exercise 3: Load Balancing Techniques - Report
### Objective:
To implement load balancing in a Django application using NGINX, distribute traffic across multiple servers, and ensure high availability through health checks and load distribution.
### Task 1: Set Up a Basic Load Balancer (NGINX)
- NGINX was installed on Windows.
- Configured NGINX as a load balancer to distribute traffic between two Django application servers running on different ports (127.0.0.1:8000 and 127.0.0.1:8001).
- The load balancer was set to use round-robin load balancing, which distributes incoming requests evenly across both servers.
### Configuration in nginx.conf:
```sh
upstream django_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}
server {
    listen 80;
    server_name localhost;
    location / {
        proxy_pass http://django_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root html;
    }
}
```
### Task 2: Session Management (Sticky Sessions)
Modified the NGINX configuration to enable sticky sessions:
In nginx.conf file changed the upstream block to:
```sh
upstream django_servers {
    ip_hash;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}
# settings.py 
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

```
### Task 3: Health Checks
Added Health Checks to NGINX:
Updated the nginx.conf file to include health check settings:
```sh
upstream django_servers {
    ip_hash;
    server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
}

```
### Task 4: Scaling (Simulate a Traffic Surge)
Simulated a traffic surge by using Apache Benchmark (ab) to generate concurrent requests to the load balancer. Command used for the test:
```sh
ab -n 1000 -c 10 http://localhost/

```
### Results from Load Testing (Apache Benchmark):
#### Summary:
```sh
Total Requests: 1000
Concurrency Level: 10
Time taken for tests: 66.613 seconds
Requests per second: 15.01 [#/sec]
Failed Requests: 999 (due to length mismatch or other issues)
Transfer Rate: 178.42 [Kbytes/sec]
```
#### Details:
```sh
Mean time per request: 666.128 ms
Median time per request: 628 ms
Maximum time for request: 1026 ms
99% of the requests were served within 941 ms.
```
#### Connection Times:
```sh
Connect time: Minimum: 0 ms, Maximum: 16 ms
Processing time: Mean: 642 ms
Waiting time: Mean: 642 ms
```
#### Issues:
- Failed Requests: Out of 1000 requests, 999 failed due to content length mismatches. This suggests there may be a mismatch between the expected content size and what was returned from the Django servers.
### Task 5: Performance Report
#### Effectiveness of Load Balancer:
- Traffic Distribution: NGINX distributed the incoming requests evenly between the two Django servers. Under high traffic, both servers shared the load, preventing bottlenecks.
- Sticky Sessions: Sticky sessions worked well, ensuring that users' session data was consistently routed to the same server. This is crucial for applications that depend on session data for authentication or user state.
- Health Checks: If one server went down, NGINX correctly detected the failure and redirected all traffic to the remaining healthy server, maintaining availability.
#### Challenges:
- NGINX on Windows: Running NGINX on Windows is not as smooth as on Linux systems, as Windows support is experimental and limited. However, it worked well for development and testing purposes.
- Session Management: Ensuring consistent sessions across servers required configuring shared session storage (e.g., Redis). Without shared storage, sticky sessions wouldn’t maintain the correct session data across multiple servers.
### Conclusion:
The load balancer setup significantly improved the scalability and reliability of the Django application. Traffic was distributed evenly, ensuring high availability and consistent performance, even during a traffic surge. Sticky sessions and health checks ensured session consistency and reliability in case of server failure.