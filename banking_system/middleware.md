Acha, chalein **FastAPI middleware** ko bilkul detail mein samajhte hain, **Roman Urdu** mein. Main koshish karunga ke har concept ko example ke saath clear karun.

---

## 1. Middleware Kya Hai? (Asaan Lafzon Mein)

Middleware ek **function** hai jo **har request** ke aane par aur **response** ke jaane se pehle chalta hai.

Sochiye:
Request Aati Hai → **Middleware 1** → **Middleware 2** → **FastAPI App** → **Response** → **Middleware 2** → **Middleware 1** → Client Tak.

Middleware ka kaam:
- Request ko modify karna (headers, body)
- Logging karna
- Authentication check karna
- Response time nikalna
- CORS headers add karna

---

## 2. Middleware Ka Structure

FastAPI mein middleware ek **function** hota hai jo `@app.middleware("http")` decorator se decorate hota hai.

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # 1. Request se pehle ka code
    print("Middleware: Request aayi")

    # 2. Next middleware ya actual endpoint call karna
    response = await call_next(request)

    # 3. Response ke baad ka code
    print("Middleware: Response jaa rahi")

    return response
```

**Important Points:**
- `call_next` ek **coroutine** hai, isko `await` karna zaroori hai
- `call_next(request)` actual endpoint ya next middleware ko call karta hai
- Jo bhi code `call_next` se pehle likhenge, wo request pe perform hoga
- Jo bhi code `call_next` ke baad likhenge, wo response pe perform hoga

---

## 3. Real-World Examples

### Example 1: Request Logging Middleware

```python
from fastapi import FastAPI, Request
import time
import logging

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Request start time
    start_time = time.time()

    # Request details
    logger.info(f"Method: {request.method} | Path: {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate time taken
    process_time = time.time() - start_time

    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)

    # Log response
    logger.info(f"Status: {response.status_code} | Time: {process_time:.4f}s")

    return response

@app.get("/")
async def home():
    return {"message": "Hello World"}
```

### Example 2: Authentication Middleware (Simple)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Public paths jo authentication nahi mangte
    public_paths = ["/", "/docs", "/openapi.json", "/login"]

    if request.url.path in public_paths:
        return await call_next(request)

    # Authorization header check
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing or invalid token"}
        )

    token = auth_header.split(" ")[1]

    # Token validation logic (example)
    if token != "secret-token":
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"}
        )

    # Token valid, proceed
    response = await call_next(request)
    return response

@app.get("/protected")
async def protected():
    return {"message": "You have access!"}
```

### Example 3: Add Custom Header in Every Response

```python
@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)

    # Add custom headers
    response.headers["X-Custom-Header"] = "MyApp"
    response.headers["X-Powered-By"] = "FastAPI"

    return response
```

---

## 4. Multiple Middleware - Order Matters

Jis order mein middleware define karte ho, wohi order mein execute hote hain.

```python
@app.middleware("http")
async def middleware_one(request: Request, call_next):
    print("1: Before")
    response = await call_next(request)
    print("1: After")
    return response

@app.middleware("http")
async def middleware_two(request: Request, call_next):
    print("2: Before")
    response = await call_next(request)
    print("2: After")
    return response

# Execution order:
# 1: Before → 2: Before → Endpoint → 2: After → 1: After
```

---

## 5. Middleware vs Dependency vs Exception Handler

| Feature | Middleware | Dependency | Exception Handler |
|---------|------------|------------|-------------------|
| Scope | Har request | Per endpoint/route | Har exception |
| Use Case | Logging, CORS, Auth | DB session, validation | Error formatting |
| Execution | Har request pe | Jahan use karo | Jab exception aaye |

---

## 6. Advanced: Request Body Reading in Middleware

**Problem:** Middleware mein agar request body read karo to endpoint mein body empty ho jati hai (stream consume ho jati hai).

**Solution:** Body ko cache karna.

```python
from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.middleware("http")
async def read_body_middleware(request: Request, call_next):
    # Body read karna
    body = await request.body()

    # Body ko cache karna
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive

    # Optional: Body parse karna
    if body:
        try:
            json_body = json.loads(body)
            print(f"Request body: {json_body}")
        except:
            pass

    response = await call_next(request)
    return response
```

---

## 7. Built-in Middleware

FastAPI/FastAPI kuch built-in middleware provide karta hai:

### a. CORSMiddleware (Most Common)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### b. TrustedHostMiddleware

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

### c. GZipMiddleware

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### d. HTTPSRedirectMiddleware

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

---

## 8. Performance Considerations

1. **Async/Await**: Middleware ko `async` banayein, kyunki `call_next` async hai
2. **Lightweight**: Heavy operations (DB calls) avoid karein middleware mein
3. **Early Return**: Agar request invalid hai to jaldi return karein
4. **Body Reading**: Sirf zaroorat ho tabhi body read karein

```python
# Bad practice
@app.middleware("http")
async def slow_middleware(request: Request, call_next):
    # Heavy DB query - should be in dependency
    user = await db.query(User).all()

    response = await call_next(request)
    return response

# Good practice
@app.middleware("http")
async def fast_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Time"] = str(time.time() - start)
    return response
```

---

## 9. Testing Middleware

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_middleware():
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) > 0
```

---

## 10. Common Use Cases Summary

1. **Request/Response Logging** - Debugging, analytics
2. **Authentication** - Token validation
3. **CORS** - Cross-origin requests
4. **Rate Limiting** - Request throttling
5. **Compression** - GZip responses
6. **Security Headers** - Add security headers
7. **Request ID** - Unique ID for tracing
8. **Response Time** - Performance monitoring

---

## 11. Complete Production-Ready Example

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import uuid
import logging

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, specify hosts
)

# Custom middleware for request ID and timing
@app.middleware("http")
async def production_middleware(request: Request, call_next):
    # Generate request ID
    request_id = str(uuid.uuid4())

    # Add request ID to logger context
    logger.info(f"Request ID: {request_id} | Method: {request.method} | Path: {request.url.path}")

    # Start time
    start_time = time.time()

    # Process request
    try:
        response = await call_next(request)

        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{time.time() - start_time:.4f}s"

        return response

    except Exception as e:
        logger.error(f"Request ID: {request_id} | Error: {str(e)}")
        raise

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.get("/protected")
async def protected():
    return {"message": "Protected route"}
```

---

## Summary (Yaad Rakhne Wali Baatein)

1. Middleware **har request** pe chalta hai
2. **Order** matter karta hai
3. `call_next` ko **await** karna mandatory hai
4. Middleware **async** hona chahiye
5. Body read karne mein **careful** rahein
6. **Heavy operations** avoid karein
7. Production mein **built-in middleware** (CORS, TrustedHost) zaroor use karein

Koi specific middleware pattern ya use case chahiye to bata sakte hain, main aur detail mein samjha sakta hoon!


Bilkul, ab main aapko **production-level**, **big platform** ki tarah **saari information** collect karne ka tareeqa bataunga — jaise IP address, browser info, device info, location, security headers, request tracking, aur bhi bahut kuch.

---

## 🎯 Big Platforms Kya Collect Karte Hain?

Pehle samajhte hain ke bade platforms (Netflix, Amazon, Google, etc.) generally kya information collect karte hain:

| Category | Information | Purpose |
|----------|-------------|---------|
| **Network** | IP address, ISP, proxy detection | Security, geo-restriction |
| **Device** | Browser, OS, device type, screen resolution | Analytics, optimization |
| **Browser** | User-Agent, language, plugins, fonts | Fingerprinting, personalization |
| **Behavior** | Request ID, timestamp, session ID | Tracing, debugging |
| **Security** | TLS version, cipher suite, headers | Attack prevention |
| **Location** | Country, city (from IP) | Geo-blocking, compliance |

---

## 🚀 Production-Ready Solution: Step by Step

### Step 1: Install All Required Packages

```bash
pip install fastapi uvicorn
pip install uainsight           # User-Agent parsing
pip install fastapi-middlewares # Request ID, timing, logging, security headers
pip install secweb              # Advanced security headers
pip install geoip2              # Geo-location from IP (requires MaxMind DB)
```

---

### Step 2: Complete Middleware Setup (Like Big Platforms)

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from middlewares import (
    RequestIDMiddleware,
    RequestTimingMiddleware,
    LoggingMiddleware,
    ErrorHandlingMiddleware,
)
from uainsight import parse_user_agent
import geoip2.database
import uuid
import time
import logging
from typing import Dict, Any

# ============================================
# 1. APP INITIALIZATION
# ============================================
app = FastAPI(
    title="My Big Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# 2. LOGGING SETUP (Structured JSON logs like production)
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# ============================================
# 3. GEO-LOCATION SETUP (MaxMind GeoLite2 DB)
# ============================================
# Download GeoLite2-Country.mmdb from MaxMind
# Place it in your project directory
geoip_reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

def get_geo_info(ip: str) -> Dict[str, Any]:
    """Get country, city, coordinates from IP address"""
    try:
        response = geoip_reader.city(ip)
        return {
            "country": response.country.name,
            "country_code": response.country.iso_code,
            "city": response.city.name,
            "postal_code": response.postal.code,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
            "timezone": response.location.time_zone,
            "isp": response.traits.isp,
            "organization": response.traits.organization
        }
    except:
        return {"error": "GeoIP lookup failed"}

# ============================================
# 4. MIDDLEWARE ORDER (Critical - outermost first)
# ============================================

# 4.1 ERROR HANDLING - Catches all exceptions (outermost)
app.add_middleware(
    ErrorHandlingMiddleware,
    include_traceback=False  # False in production
)

# 4.2 CORS - Handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 4.3 TRUSTED HOST - Prevent host header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "api.yourdomain.com"]
)

# 4.4 REQUEST ID - Unique ID for tracing
app.add_middleware(RequestIDMiddleware, header_name="X-Request-ID")

# 4.5 REQUEST TIMING - Response time measurement
app.add_middleware(RequestTimingMiddleware, header_name="X-Response-Time")

# 4.6 LOGGING - Structured logging with request/response
app.add_middleware(
    LoggingMiddleware,
    logger_name="api_logger",
    skip_paths=["/health", "/metrics"],
    log_response_body=False,  # Turn on for debugging only
)

# ============================================
# 5. CUSTOM DEVICE INFO MIDDLEWARE
# ============================================
@app.middleware("http")
async def device_info_middleware(request: Request, call_next):
    """Extract and store all device/browser information"""

    # Get User-Agent
    user_agent_string = request.headers.get("user-agent", "Unknown")

    # Parse User-Agent using uainsight
    ua = parse_user_agent(user_agent_string)

    # Get client IP (handling proxies)
    client_ip = get_client_ip(request)

    # Get geo-location
    geo_info = get_geo_info(client_ip)

    # Store all info in request.state for later use
    request.state.device_info = {
        "browser": {
            "name": ua.browser.name,
            "version": ua.browser.version,
            "major_version": ua.browser.major_version
        },
        "os": {
            "name": ua.os.name,
            "version": ua.os.version,
            "platform": ua.os.platform
        },
        "device": {
            "type": ua.device.type,  # smartphone, tablet, desktop, bot
            "vendor": ua.device.vendor,
            "model": ua.device.model
        },
        "engine": {
            "name": ua.engine.name,
            "version": ua.engine.version
        },
        "cpu": {
            "architecture": ua.cpu.architecture
        },
        "is_bot": ua.is_bot
    }

    request.state.client_info = {
        "ip": client_ip,
        "geo": geo_info
    }

    # Log for monitoring
    logger.info(f"Device: {ua.device.type} | Browser: {ua.browser.name} | OS: {ua.os.name} | IP: {client_ip}")

    response = await call_next(request)

    # Add device info headers (optional)
    response.headers["X-Device-Type"] = ua.device.type or "unknown"
    response.headers["X-Browser"] = ua.browser.name or "unknown"

    return response

def get_client_ip(request: Request) -> str:
    """Get real client IP behind proxies (Nginx, Cloudflare, etc.)"""
    # Check Cloudflare header first
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    if cf_connecting_ip:
        return cf_connecting_ip

    # Check X-Forwarded-For (Nginx, AWS, etc.)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Check X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fallback to direct client IP
    return request.client.host if request.client else "unknown"

# ============================================
# 6. ENDPOINT EXAMPLES
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/device-info")
async def get_device_info(request: Request):
    """Get complete device and client information"""
    return {
        "device": request.state.get("device_info", {}),
        "client": request.state.get("client_info", {}),
        "headers": dict(request.headers),
        "request_id": request.scope.get("request_id")
    }

@app.get("/api/analytics/track")
async def track_request(request: Request):
    """Track request for analytics (like Google Analytics)"""
    return {
        "success": True,
        "tracked_data": {
            "session_id": request.cookies.get("session_id"),
            "device": request.state.device_info,
            "timestamp": time.time()
        }
    }

# ============================================
# 7. STARTUP EVENT
# ============================================
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    # Initialize connections, load caches, etc.

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    geoip_reader.close()

# ============================================
# 8. RUN
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📊 What Each Component Does

### 1. **Request ID Middleware** (from `fastapi-middlewares`)
- Adds unique ID to every request
- Header: `X-Request-ID`
- Use case: Trace request across logs, debug distributed systems

### 2. **Request Timing Middleware**
- Measures response time
- Header: `X-Response-Time`
- Use case: Performance monitoring, SLA tracking

### 3. **User-Agent Parsing** (using `uainsight`)
- Browser name, version
- OS name, version
- Device type (mobile/tablet/desktop/bot)
- CPU architecture
- Bot detection

### 4. **IP Detection** (handling proxies)
Priority order:
1. `CF-Connecting-IP` (Cloudflare)
2. `X-Forwarded-For` (Nginx, AWS ALB)
3. `X-Real-IP` (Nginx)
4. `request.client.host` (direct)

### 5. **GeoIP** (using MaxMind DB)
- Country, city, postal code
- Latitude, longitude
- Timezone
- ISP, organization

---

## 🔒 Advanced Security Headers (Like Big Platforms)

Agar aapko Netflix ya Google jaisi **security headers** chahiye, to `secweb` package use karein:

```python
from Secweb import SecWeb

# Apply all 16 security headers at once
SecWeb(
    app=app,
    Option={
        'csp': {'default-src': ["'self'"], 'script-src': ["'self'", "'unsafe-inline'"]},
        'hsts': {'max-age': 31536000, 'preload': True},
        'xframe': {'X-Frame-Options': 'DENY'},
        'referrer': {'Referrer-Policy': 'strict-origin-when-cross-origin'},
        'coep': {'Cross-Origin-Embedder-Policy': 'require-corp'},
        'coop': {'Cross-Origin-Opener-Policy': 'same-origin'},
        'corp': {'Cross-Origin-Resource-Policy': 'same-site'},
    },
    script_nonce=True,
    style_nonce=True
)
```

**Headers it adds:**
- Content-Security-Policy (CSP)
- HSTS (Strict-Transport-Security)
- X-Frame-Options
- Referrer-Policy
- Cross-Origin-Embedder-Policy
- Cross-Origin-Opener-Policy
- Cross-Origin-Resource-Policy
- X-Content-Type-Options
- X-XSS-Protection
- Cache-Control
- And more...

---

## 🌐 Client-Side Fingerprinting (Like Netflix)

Jab aapko browser fingerprinting karna ho (different devices detect karna ho), to **FingerprintJS** use karein frontend pe :

```javascript
// React/Frontend code
import FingerprintJS from '@fingerprintjs/fingerprintjs';

const fpPromise = FingerprintJS.load();

fpPromise
  .then(fp => fp.get())
  .then(result => {
    const visitorId = result.visitorId;  // Unique device ID
    const components = result.components; // Screen, fonts, canvas, etc.

    // Send to backend
    fetch('/api/fingerprint', {
      method: 'POST',
      body: JSON.stringify({ visitorId, components })
    });
  });
```

Backend mein store karein aur compare karein — agar naya fingerprint aaye to security alert bhejein.

---

## 📈 Production Deployment: Nginx + Cloudflare Configuration

Agar aap **Nginx** ya **Cloudflare** use kar rahe hain, to real IP lene ke liye ye configure karein :

### Nginx Configuration:
```nginx
location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://fastapi_app:8000;
}
```

### Cloudflare Headers (automatic):
- `CF-Connecting-IP`: Real visitor IP
- `CF-Ray`: Cloudflare request ID
- `CF-IPCountry`: Country code
- `CF-Device-Type`: Device type (mobile/desktop/tablet)

---

## 📋 Complete Information Collection Summary

| Information | Source | Method |
|-------------|--------|--------|
| IP Address | Headers (CF-Connecting-IP, X-Forwarded-For) | `get_client_ip()` |
| Country/City | MaxMind GeoIP DB | `geoip2` |
| Browser | User-Agent | `uainsight` |
| OS | User-Agent | `uainsight` |
| Device Type | User-Agent | `uainsight` |
| Request ID | Middleware | `RequestIDMiddleware` |
| Response Time | Middleware | `RequestTimingMiddleware` |
| Security Headers | Middleware | `SecWeb` or `SecurityHeadersMiddleware` |
| Client Fingerprint | Frontend JS | FingerprintJS |
| All Headers | Request object | `request.headers` |
| Cookies | Request object | `request.cookies` |
| Query Params | Request object | `request.query_params` |

---

## 🎯 Big Platform Examples

**Netflix/Amazon Prime:**
- Device fingerprinting for DRM
- Different device detection (send security email)
- Geo-restriction based on IP

**Google/YouTube:**
- Request ID for debugging
- Structured logging for analytics
- Security headers (CSP, HSTS)

**Uber/Zomato:**
- IP-based fraud detection
- Device information for app version tracking
- Session tracking with request ID

---

## ✅ Checklist: Production-Ready Setup

- [ ] Request ID middleware (tracing)
- [ ] Timing middleware (performance monitoring)
- [ ] Logging middleware (structured JSON logs)
- [ ] IP detection with proxy support
- [ ] GeoIP lookup
- [ ] User-Agent parsing
- [ ] Security headers (CSP, HSTS, etc.)
- [ ] CORS configuration
- [ ] Trusted hosts
- [ ] Health check endpoint
- [ ] Error handling (no tracebacks in production)

Koi specific scenario ya doubt ho to pooch sakte hain!


Bilkul, ab main aapko **ek complete, advanced-level middleware system** bataunga jo **production mein big platforms** (Netflix, Uber, Amazon jaise) use karte hain. Yeh ek **all-in-one solution** hai.

---

## 🎯 Complete Advanced Middleware Architecture

Yeh wo sab kuch hai jo ek **enterprise-grade** FastAPI app mein middleware ke through implement karna chahiye:

```python
# Complete Production Middleware System
# A middleware is a function that runs for every request before it reaches your endpoint
# and after the response is generated before it's sent back to the client
```

---

## 📦 Step 1: Install All Required Packages

```bash
# Core
pip install fastapi uvicorn

# Security & Rate Limiting
pip install fastapi-guard           # IP control, rate limiting, security headers
pip install fastapi-easylimiter     # Advanced rate limiting with Redis

# Observability
pip install fastapi-middlewares     # Request ID, timing, logging, error handling

# User-Agent & Device Detection
pip install uainsight               # Parse browser, OS, device from User-Agent

# GeoIP (MaxMind)
pip install geoip2                  # Country/city from IP address

# Background Tasks
pip install celery redis            # For async background jobs

# Caching
pip install redis                   # For rate limiting state
```

---

## 🏗️ Step 2: Complete Middleware System (Production Ready)

### File Structure

```
your_project/
├── middleware/
│   ├── __init__.py
│   ├── security.py          # Security headers, CORS
│   ├── auth.py              # JWT, API key authentication
│   ├── rate_limit.py        # Rate limiting logic
│   ├── logging.py           # Request/response logging
│   ├── device_info.py       # Browser/device detection
│   ├── geo_ip.py            # IP geolocation
│   ├── request_id.py        # Unique request tracking
│   ├── timing.py            # Response time measurement
│   ├── error_handler.py     # Global exception handling
│   ├── compression.py       # GZip response compression
│   ├── ip_filter.py         # IP whitelist/blacklist
│   ├── bot_detection.py     # Bot/crawler detection
│   └── audit.py             # Audit logging for compliance
└── main.py                  # FastAPI app with all middlewares
```

---

## 🔧 Step 3: Individual Middleware Implementations

### 1. Request ID Middleware (Tracing)

```python
# middleware/request_id.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID to every request for tracing across logs.
    Think of it like a tracking number for every API call.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate unique ID for this request
        request_id = str(uuid.uuid4())

        # Store in request scope for access in endpoints
        request.state.request_id = request_id

        # Process the request
        response = await call_next(request)

        # Add ID to response headers so client can send it back for debugging
        response.headers["X-Request-ID"] = request_id

        return response
```

**Use case:** Jab koi error aata hai, client aapko `X-Request-ID` bhej sakta hai aur aap logs mein dekh sakte ho exactly kya hua tha.

---

### 2. Request Timing Middleware (Performance Monitoring)

```python
# middleware/timing.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measures how long each request takes to process.
    Critical for identifying slow endpoints.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        # Calculate processing time in milliseconds
        process_time_ms = (time.perf_counter() - start_time) * 1000

        # Add header so clients know how long it took
        response.headers["X-Response-Time-Ms"] = str(round(process_time_ms, 2))

        # Store for logging middleware
        request.state.process_time_ms = process_time_ms

        return response
```

**Use case:** Agar koi endpoint slow ho raha hai, to aap `X-Response-Time-Ms` header dekh kar identify kar sakte ho.

---

### 3. Security Headers Middleware (OWASP Compliance)

```python
# middleware/security.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to every response to protect against common attacks.
    These are OWASP-recommended headers used by all big platforms.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Prevent browsers from MIME-sniffing a response away from declared content-type
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enable browser XSS filtering
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Prevent clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"

        # Control how much referrer information is sent with links
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Force HTTPS connections (HSTS)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Control which resources can be loaded (CSP)
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Remove server identification (security through obscurity)
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        return response
```

**Use case:** Yeh headers XSS, clickjacking, MIME-sniffing jaise attacks se protect karte hain. Har big platform yeh headers use karta hai.

---

### 4. Rate Limiting Middleware (DDoS Protection)

```python
# middleware/rate_limit.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Limits the number of requests per client IP within a time window.
    Prevents brute force attacks and API abuse.
    """

    def __init__(self, app, max_requests: int = 100, time_window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests      # Maximum requests allowed
        self.time_window = time_window        # Time window in seconds
        self.requests = defaultdict(list)     # Store timestamps per IP

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = self._get_client_ip(request)

        # Get current timestamp
        now = time.time()

        # Clean up old requests
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if now - timestamp < self.time_window
        ]

        # Check if rate limit exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.max_requests} requests per {self.time_window} seconds."
            )

        # Add current request timestamp
        self.requests[client_ip].append(now)

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(self.max_requests - len(self.requests[client_ip]))
        response.headers["X-RateLimit-Reset"] = str(int(now + self.time_window))

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP behind proxies"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"
```

**Use case:** Har IP se sirf 100 requests per minute allow karna. Isse DDoS attacks aur brute force se bachat hoti hai.

---

### 5. Device & Browser Info Middleware

```python
# middleware/device_info.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from uainsight import parse_user_agent

class DeviceInfoMiddleware(BaseHTTPMiddleware):
    """
    Extracts browser, OS, and device information from User-Agent header.
    Used for analytics, fraud detection, and personalization.
    """

    async def dispatch(self, request: Request, call_next):
        user_agent_string = request.headers.get("user-agent", "Unknown")

        # Parse User-Agent using uainsight
        ua = parse_user_agent(user_agent_string)

        # Store all device info in request.state for endpoints to use
        request.state.device_info = {
            "browser": {
                "name": ua.browser.name,
                "version": ua.browser.version,
                "major_version": ua.browser.major_version
            },
            "os": {
                "name": ua.os.name,
                "version": ua.os.version,
                "platform": ua.os.platform
            },
            "device": {
                "type": ua.device.type,      # smartphone, tablet, desktop, bot
                "vendor": ua.device.vendor,
                "model": ua.device.model
            },
            "engine": {
                "name": ua.engine.name,
                "version": ua.engine.version
            },
            "cpu": {
                "architecture": ua.cpu.architecture
            },
            "is_bot": ua.is_bot
        }

        response = await call_next(request)

        # Add device type to response headers
        if request.state.device_info["device"]["type"]:
            response.headers["X-Device-Type"] = request.state.device_info["device"]["type"]

        return response
```

**Use case:** Analytics mein track karna ke users mostly mobile use kar rahe hain ya desktop. Fraud detection mein agar bot detect ho to block karna.

---

### 6. IP Geolocation Middleware

```python
# middleware/geo_ip.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import geoip2.database
from functools import lru_cache

# Load GeoIP database (download from MaxMind)
geoip_reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

class GeoIPMiddleware(BaseHTTPMiddleware):
    """
    Determines geographical location (country, city, coordinates) from client IP.
    Used for geo-blocking, content personalization, and analytics.
    """

    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)

        # Skip for localhost/internal IPs
        if client_ip in ["127.0.0.1", "localhost"] or client_ip.startswith("192.168."):
            request.state.geo_info = {"error": "Internal IP"}
            return await call_next(request)

        # Get geolocation data
        request.state.geo_info = self._get_geo_info(client_ip)

        response = await call_next(request)

        # Add country code to response headers
        if request.state.geo_info.get("country_code"):
            response.headers["X-Country-Code"] = request.state.geo_info["country_code"]

        return response

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"

    @lru_cache(maxsize=1000)
    def _get_geo_info(self, ip: str) -> dict:
        """Cached geo lookup for performance"""
        try:
            response = geoip_reader.city(ip)
            return {
                "country": response.country.name,
                "country_code": response.country.iso_code,
                "city": response.city.name,
                "postal_code": response.postal.code,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "timezone": response.location.time_zone
            }
        except:
            return {"error": "Geo lookup failed"}
```

**Use case:** Agar aapka content sirf US ke liye licensed hai, to aap US ke bahar ke IPs ko block kar sakte ho. Ya phir analytics mein dekhna ke kaunse country se traffic aa raha hai.

---

### 7. Logging Middleware (Structured Logging)

```python
# middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request and response in structured JSON format.
    Essential for debugging, monitoring, and compliance.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        await self._log_request(request)

        # Process request
        try:
            response = await call_next(request)

            # Log response
            await self._log_response(request, response, start_time)

            return response
        except Exception as e:
            # Log error
            logger.error(json.dumps({
                "event": "request_error",
                "request_id": getattr(request.state, "request_id", None),
                "method": request.method,
                "path": request.url.path,
                "error": str(e)
            }))
            raise

    async def _log_request(self, request: Request):
        log_data = {
            "event": "request_received",
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent"),
            "timestamp": time.time()
        }
        logger.info(json.dumps(log_data))

    async def _log_response(self, request: Request, response, start_time: float):
        log_data = {
            "event": "response_sent",
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": (time.time() - start_time) * 1000,
            "timestamp": time.time()
        }
        logger.info(json.dumps(log_data))

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"
```

**Use case:** Har request ka log. Jab production mein kuch galat hota hai, to aap logs dekh kar exactly pata kar sakte ho ke kya hua.

---

### 8. Error Handling Middleware

```python
# middleware/error_handler.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Catches all exceptions and returns formatted JSON responses.
    Prevents stack traces from leaking to clients in production.
    """

    def __init__(self, app, debug: bool = False):
        super().__init__(app)
        self.debug = debug

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            # FastAPI's HTTP exceptions - return as is
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.detail,
                    "request_id": getattr(request.state, "request_id", None)
                }
            )
        except Exception as e:
            # Unknown exceptions - log and return 500
            request_id = getattr(request.state, "request_id", None)

            logger.error(json.dumps({
                "event": "unhandled_exception",
                "request_id": request_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc() if self.debug else None
            }))

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "request_id": request_id,
                    "detail": str(e) if self.debug else None
                }
            )
```

**Use case:** Production mein kabhi bhi client ko raw stack trace nahi dikhna chahiye. Yeh middleware ensure karta hai ke har error clean JSON response mein convert ho jaye.

---

### 9. IP Whitelist/Blacklist Middleware

```python
# middleware/ip_filter.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import ipaddress

class IPFilterMiddleware(BaseHTTPMiddleware):
    """
    Allows or blocks requests based on client IP address.
    Used for internal admin panels or blocking malicious IPs.
    """

    def __init__(self, app, whitelist: list = None, blacklist: list = None):
        super().__init__(app)
        self.whitelist = [ipaddress.ip_network(net) for net in (whitelist or [])]
        self.blacklist = [ipaddress.ip_network(net) for net in (blacklist or [])]

    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)

        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except ValueError:
            # Invalid IP address
            raise HTTPException(status_code=400, detail="Invalid IP address")

        # Check whitelist first (if any)
        if self.whitelist:
            if not any(ip_obj in network for network in self.whitelist):
                raise HTTPException(status_code=403, detail="Access denied")

        # Check blacklist
        if self.blacklist:
            if any(ip_obj in network for network in self.blacklist):
                raise HTTPException(status_code=403, detail="Access denied")

        return await call_next(request)

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"
```

**Use case:** Admin panel ko sirf company ke internal IPs se accessible rakhna. Ya phir kisi malicious IP ko block karna.

---

### 10. Bot Detection Middleware

```python
# middleware/bot_detection.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from uainsight import parse_user_agent

class BotDetectionMiddleware(BaseHTTPMiddleware):
    """
    Detects and optionally blocks bots/crawlers.
    Useful for protecting content from being scraped.
    """

    def __init__(self, app, block_bots: bool = False):
        super().__init__(app)
        self.block_bots = block_bots

    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")

        # Parse User-Agent
        ua = parse_user_agent(user_agent)

        # Store bot info
        request.state.is_bot = ua.is_bot

        # Block bots if configured
        if self.block_bots and ua.is_bot:
            raise HTTPException(status_code=403, detail="Bots not allowed")

        response = await call_next(request)
        response.headers["X-Is-Bot"] = str(ua.is_bot).lower()

        return response
```

**Use case:** Agar aapko scrape se bachna hai ya bots ko analytics se exclude karna hai.

---

### 11. Audit Logging Middleware (Compliance)

```python
# middleware/audit.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json
import logging
from datetime import datetime

audit_logger = logging.getLogger("audit")

class AuditMiddleware(BaseHTTPMiddleware):
    """
    Logs all data mutations (POST, PUT, DELETE) for compliance.
    Required for GDPR, HIPAA, and other regulations.
    """

    async def dispatch(self, request: Request, call_next):
        # Only log mutating requests
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Log before processing
            await self._log_audit(request, "started")

        response = await call_next(request)

        # Log after completion with status
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            await self._log_audit(request, "completed", response.status_code)

        return response

    async def _log_audit(self, request: Request, status: str, status_code: int = None):
        audit_logger.info(json.dumps({
            "event": "audit_log",
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "client_ip": self._get_client_ip(request),
            "user_id": getattr(request.state, "user_id", None),
            "status": status,
            "status_code": status_code
        }))

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"
```

**Use case:** Agar aap healthcare ya finance domain mein kaam kar rahe ho, to audit trail mandatory hota hai.

---

## 🚀 Step 4: Putting It All Together (main.py)

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Import all custom middlewares
from middleware.request_id import RequestIDMiddleware
from middleware.timing import TimingMiddleware
from middleware.security import SecurityHeadersMiddleware
from middleware.rate_limit import RateLimitingMiddleware
from middleware.device_info import DeviceInfoMiddleware
from middleware.geo_ip import GeoIPMiddleware
from middleware.logging import LoggingMiddleware
from middleware.error_handler import ErrorHandlingMiddleware
from middleware.ip_filter import IPFilterMiddleware
from middleware.bot_detection import BotDetectionMiddleware
from middleware.audit import AuditMiddleware

app = FastAPI(
    title="Complete Production API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# MIDDLEWARE ORDER (CRITICAL!)
# Last added = First executed (outermost)
# ============================================

# 1. Error Handling - Catches all exceptions (outermost)
app.add_middleware(ErrorHandlingMiddleware, debug=False)

# 2. HTTPS Redirect - Force HTTPS in production
# app.add_middleware(HTTPSRedirectMiddleware)  # Enable in production

# 3. Trusted Host - Prevent host header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.yourdomain.com"])

# 4. CORS - Handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. IP Filter - Block/allow IPs
app.add_middleware(
    IPFilterMiddleware,
    whitelist=["192.168.1.0/24"],  # Internal network only
    # blacklist=["203.0.113.0/24"]
)

# 6. Rate Limiting - DDoS protection
app.add_middleware(RateLimitingMiddleware, max_requests=100, time_window=60)

# 7. Bot Detection - Identify/block bots
app.add_middleware(BotDetectionMiddleware, block_bots=False)

# 8. Security Headers - OWASP compliance
app.add_middleware(SecurityHeadersMiddleware)

# 9. Geo IP - Country detection
app.add_middleware(GeoIPMiddleware)

# 10. Device Info - Browser/OS detection
app.add_middleware(DeviceInfoMiddleware)

# 11. Request ID - Unique tracking
app.add_middleware(RequestIDMiddleware)

# 12. Timing - Response time measurement
app.add_middleware(TimingMiddleware)

# 13. Audit Log - Compliance logging
app.add_middleware(AuditMiddleware)

# 14. Request/Response Logging
app.add_middleware(LoggingMiddleware)

# 15. GZip Compression - Response compression (innermost)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ============================================
# SAMPLE ENDPOINTS
# ============================================

@app.get("/")
async def root(request: Request):
    """Root endpoint showing all collected info"""
    return {
        "message": "Welcome to Complete Production API",
        "request_id": getattr(request.state, "request_id", None),
        "device_info": getattr(request.state, "device_info", {}),
        "geo_info": getattr(request.state, "geo_info", {}),
        "is_bot": getattr(request.state, "is_bot", False),
        "response_time_ms": getattr(request.state, "process_time_ms", 0)
    }

@app.get("/health")
async def health():
    """Health check for load balancers"""
    return {"status": "healthy"}

@app.post("/api/data")
async def create_data(request: Request):
    """Example POST endpoint - will be audited"""
    return {"message": "Data created", "request_id": getattr(request.state, "request_id")}

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📊 Summary: What Each Middleware Does

| # | Middleware | Purpose | Use Case |
|---|------------|---------|----------|
| 1 | Error Handling | Catch all exceptions | Prevent stack trace leaks |
| 2 | HTTPS Redirect | Force secure connections | Production security |
| 3 | Trusted Host | Prevent host header attacks | Security |
| 4 | CORS | Allow cross-origin requests | Frontend integration |
| 5 | IP Filter | Block/allow IPs | Admin access control |
| 6 | Rate Limiting | Limit requests per IP | DDoS protection |
| 7 | Bot Detection | Identify/block bots | Anti-scraping |
| 8 | Security Headers | OWASP headers | XSS, clickjacking protection |
| 9 | Geo IP | Country detection | Geo-blocking, analytics |
| 10 | Device Info | Browser/OS detection | Analytics, personalization |
| 11 | Request ID | Unique tracking | Debugging across services |
| 12 | Timing | Response time | Performance monitoring |
| 13 | Audit Log | Compliance logging | GDPR, HIPAA |
| 14 | Logging | Request/response logs | Debugging, monitoring |
| 15 | GZip | Response compression | Faster responses |

---

## 🔑 Key Points Yaad Rakhne Wale

1. **Order Matters:** Last added = First executed. Error handling sabse pehle, compression sabse baad mein.
2. **Performance:** Middleware lightweight rakho. Heavy operations (DB calls) background tasks mein karo.
3. **Async:** Sab middleware `async` hone chahiye.
4. **State Management:** `request.state` ka use karo data pass karne ke liye endpoints tak.
5. **Production vs Development:** Debug mode sirf development mein on rakho. Production mein tracebacks band karo.

Yeh complete middleware system **production mein big platforms ki tarah** kaam karega. Koi specific middleware aur detail mein chahiye to batao!
