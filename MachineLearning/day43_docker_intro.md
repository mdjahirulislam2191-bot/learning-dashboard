# Day 43: ডকার ইন্ট্রো
## Docker Introduction

### ডকার কি?
ডকার একটি কন্টেইনারাইজেশন প্ল্যাটফর্ম যা অ্যাপ্লিকেশন এবং তার ডিপেন্ডেন্সিগুলোকে একটি কন্টেইনারে প্যাকেজ করে। এটি "এটি আমার মেশিনে কাজ করে" সমস্যা সমাধান করে।

### ফাইন্যান্সে ডকারের ব্যবহার
- **কনসিস্টেন্ট এনভায়রনমেন্ট**: ডেভ, স্টেজিং, প্রোডাকশন একই
- **মাইক্রোসার্ভিসেস**: ফ্রড ডিটেকশন, ক্রেডিট স্কোরিং আলাদা সার্ভিস
- **স্কেলিং**: কুবারনেটিস দিয়ে অটো-স্কেলিং
- **সিআই/সিডি**: টেস্টিং এবং ডিপ্লয়মেন্ট অটোমেশন

### 1. ডকার বেসিক কনসেপ্ট
```python
print("=" * 60)
print("🐳 DOCKER BASICS")
print("=" * 60)

print("""
📌 Core Concepts:

1️⃣ Docker Image: একটি রিড-অনলি টেমপ্লেট (OS + Python + Libraries)
   - যেমন: python:3.11, ubuntu:22.04, nginx:latest

2️⃣ Docker Container: ইমেজের একটি রানিং ইনস্ট্যান্স
   - আইসোলেটেড এনভায়রনমেন্ট
   - হালকা (ভার্চুয়াল মেশিনের চেয়ে দ্রুত)
   - পোর্টেবল

3️⃣ Dockerfile: ইমেজ বিল্ড করার নির্দেশনা (রেসিপি)
   - FROM: বেস ইমেজ
   - COPY: ফাইল কপি
   - RUN: কমান্ড চালানো
   - CMD: কন্টেইনার স্টার্ট হলে কি চালাবে

4️⃣ Docker Hub: পাবলিক ইমেজ রেজিস্ট্রি
   - hub.docker.com
   - অফিশিয়াল ইমেজ: python, ubuntu, nginx

5️⃣ Container Registry: কাস্টম ইমেজ সংরক্ষণের জায়গা
   - Docker Hub, AWS ECR, GCP GCR, Azure ACR
""")
```

### 2. Flask ML App Dockerfile
```python
print("\n" + "=" * 60)
print("📄 DOCKERFILE FOR ML APP")
print("=" * 60)

dockerfile_content = '''
# === Dockerfile ===
# বেস ইমেজ (Python 3.11)
FROM python:3.11-slim

# ওয়ার্কিং ডিরেক্টরি
WORKDIR /app

# ডিপেন্ডেন্সি ফাইল কপি
COPY requirements.txt .

# ডিপেন্ডেন্সি ইনস্টল
RUN pip install --no-cache-dir -r requirements.txt

# অ্যাপ কোড কপি
COPY app.py .
COPY credit_risk_model.pkl .
COPY model_config.json .

# এক্সপোজ পোর্ট
EXPOSE 5000

# কন্টেইনার স্টার্ট কমান্ড
CMD ["python", "app.py"]
'''

print("📋 Dockerfile:")
print(dockerfile_content)

# requirements.txt
print("\n📋 requirements.txt:")
print("""
flask==3.0.0
scikit-learn==1.3.0
pandas==2.1.0
numpy==1.24.0
gunicorn==21.2.0
""")
```

### 3. Docker কমান্ড
```python
print("\n" + "=" * 60)
print("🚢 DOCKER COMMANDS")
print("=" * 60)

print("""
📌 Build Commands:
docker build -t credit-risk-api:1.0 .       # ইমেজ বিল্ড
docker build --no-cache -t myapp .          # ক্যাশ ছাড়া বিল্ড

📌 Image Management:
docker images                               # লোকাল ইমেজ লিস্ট
docker rmi credit-risk-api:1.0              # ইমেজ ডিলিট
docker tag myapp myrepo/myapp:latest        # ট্যাগিং
docker pull python:3.11-slim                # ইমেজ ডাউনলোড

📌 Container Commands:
docker run -p 5000:5000 credit-risk-api     # রান
docker run -d -p 5000:5000 --name api credit-risk-api   # ডিট্যাচড
docker ps                                   # রানিং কন্টেইনার
docker ps -a                                # সব কন্টেইনার
docker stop api                             # স্টপ
docker start api                            # পুনরায় স্টার্ট
docker logs -f api                          # লগ দেখা

📌 Interactive:
docker run -it python:3.11 bash             # ইন্টারঅ্যাকটিভ শেল
docker exec -it api bash                    # রানিং কন্টেইনারে শেল

📌 Networking:
docker network create ml-network            # নেটওয়ার্ক তৈরি
docker run --network ml-network myapp       # নেটওয়ার্কে রান

📌 Volumes (ডেটা পার্সিস্টেন্স):
docker run -v /host/data:/app/data myapp    # ভলিউম মাউন্ট
""")
```

### 4. মাল্টি-স্টেজ বিল্ড
```python
print("\n" + "=" * 60)
print("📦 MULTI-STAGE BUILD (অপ্টিমাইজড)")
print("=" * 60)

multi_stage_dockerfile = '''
# === Stage 1: বিল্ড স্টেজ ===
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

# ডিপেন্ডেন্সি ইনস্টল
RUN pip install --no-cache-dir --user -r requirements.txt

# === Stage 2: রান স্টেজ ===
FROM python:3.11-slim

WORKDIR /app

# ইউজার ডিপেন্ডেন্সি কপি
COPY --from=builder /root/.local /root/.local

# অ্যাপ ফাইল কপি
COPY . .

# PATH সেট
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

# gunicorn দিয়ে রান (প্রোডাকশন)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
'''

print(multi_stage_dockerfile)
print("""
✅ Multi-stage advantages:
- Smaller final image (40MB vs 500MB)
- No build tools in production
- Faster deployments
- Less attack surface
""")
```

### 5. Docker Compose
```python
print("\n" + "=" * 60)
print("📋 DOCKER-COMPOSE.YML")
print("=" * 60)

docker_compose_content = '''
# === docker-compose.yml ===
version: '3.8'

services:
  # ML API সার্ভিস
  ml-api:
    build: .
    container_name: credit-risk-api
    ports:
      - "5000:5000"
    environment:
      - MODEL_PATH=/app/models/credit_risk_model.pkl
      - LOG_LEVEL=INFO
      - ENVIRONMENT=production
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    networks:
      - ml-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ডাটাবেস
  redis:
    image: redis:7-alpine
    container_name: ml-redis
    ports:
      - "6379:6379"
    networks:
      - ml-network
    volumes:
      - redis-data:/data

  # মনিটরিং
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - ml-network

networks:
  ml-network:
    driver: bridge

volumes:
  redis-data:
'''

print(docker_compose_content)

print("""
📌 Docker Compose Commands:
docker-compose up              # সার্ভিস চালু
docker-compose up -d           # ডিট্যাচড মোড
docker-compose down            # সার্ভিস বন্ধ
docker-compose logs -f         # সব সার্ভিসের লগ
docker-compose ps              # সার্ভিস স্ট্যাটাস
docker-compose build           # ইমেজ রিবিল্ড
""")
```

### 6. প্রোডাকশন ডিপ্লয়মেন্ট
```python
print("\n" + "=" * 60)
print("🚀 PRODUCTION DEPLOYMENT")
print("=" * 60)

production_guide = '''
📋 Production ML Deployment with Docker:

1️⃣ Build Image:
   docker build -t ml-api:1.0.0 .

2️⃣ Tag for Registry:
   docker tag ml-api:1.0.0 my-registry/ml-api:1.0.0
   docker push my-registry/ml-api:1.0.0

3️⃣ Run Container:
   docker run -d \\
     --name ml-api-prod \\
     -p 5000:5000 \\
     -e ENVIRONMENT=production \\
     -e MODEL_PATH=/models/latest.pkl \\
     -v /data/models:/models \\
     --restart always \\
     --memory=4g \\
     --cpus=2 \\
     ml-api:1.0.0

4️⃣ Health Check:
   curl http://localhost:5000/health

5️⃣ Scaling (Docker Compose):
   docker-compose up -d --scale ml-api=3

6️⃣ Monitoring:
   docker stats                    # রিসোর্স ব্যবহার
   docker logs -f ml-api-prod      # অ্যাপ লগ
   docker container inspect ml-api-prod  # ডিটেইলস

7️⃣ Update:
   docker pull my-registry/ml-api:1.0.1
   docker stop ml-api-prod
   docker rm ml-api-prod
   docker run ... ml-api:1.0.1
'''

print(production_guide)
```

### Docker Best Practices
```python
print("\n" + "=" * 60)
print("✅ DOCKER BEST PRACTICES")
print("=" * 60)

print("""
1️⃣ 📦 Keep Images Small
   - Use slim/alpine base images
   - Multi-stage builds
   - Clean apt cache (apt-get clean)
   - .dockerignore file

2️⃣ 🔒 Security
   - Don't run as root (USER appuser)
   - Scan images (docker scan, Trivy)
   - Use specific tags (not 'latest')
   - Minimal attack surface

3️⃣ ⚡ Performance
   - Layer caching (frequently changing files last)
   - Use .dockerignore
   - Limit container resources (--memory, --cpus)
   - Health checks

4️⃣ 🔄 State Management
   - Containers are ephemeral (short-lived)
   - Use volumes for persistent data
   - Externalize configuration (env vars)
   - Log to stdout/stderr

5️⃣ 🚀 Deployment
   - Tag with semantic versions
   - Use container registry
   - Orchestrator: Kubernetes, Docker Swarm, ECS
   - CI/CD pipeline (GitHub Actions, GitLab CI)

📄 .dockerignore Example:
__pycache__
*.pyc
.git
.env
data/*.csv
*.md
""")
```

### সারসংক্ষেপ
আজ আমরা ডকারের বেসিক শিখলাম:
- **Dockerfile**: ইমেজ বিল্ড নির্দেশনা
- **Docker ইমেজ**: রিড-অনলি টেমপ্লেট
- **Docker কন্টেইনার**: রানিং এনভায়রনমেন্ট
- **Docker Compose**: মাল্টি-সার্ভিস অর্কেস্ট্রেশন
- **মাল্টি-স্টেজ বিল্ড**: অপ্টিমাইজড ইমেজ সাইজ

### অনুশীলনী
1. আপনার ML Flask অ্যাপের জন্য Dockerfile তৈরি করুন
2. docker-compose.yml এ ML API + Redis যোগ করুন
3. মাল্টি-স্টেজ বিল্ড ইমপ্লিমেন্ট করুন
4. ডকার ইমেজকে Container Registry (Docker Hub) এ পুশ করুন