# 🧬 Zero Assumption DNA - Core Principle of CognoMega

**Core Principle:** **DO NOT ASSUME ANYTHING**

---

## 🎯 **WHAT IS ZERO ASSUMPTION DNA?**

Zero Assumption DNA is the fundamental principle that governs how CognoMega operates:

**NEVER assume:**
- ✅ Data exists
- ✅ Data is valid
- ✅ Operations succeed
- ✅ User intent
- ✅ Environment state
- ✅ Types are correct
- ✅ Keys exist in dictionaries
- ✅ Lists have elements
- ✅ Functions return successfully
- ✅ Errors are handled

**ALWAYS:**
- ✅ Verify explicitly
- ✅ Validate inputs
- ✅ Check return values
- ✅ Handle errors
- ✅ Get confirmation
- ✅ Log everything
- ✅ Fail loudly, not silently

---

## 🚫 **WHY THIS PRINCIPLE?**

### **Bad Code (Makes Assumptions):**

```python
# ❌ ASSUMES user exists
def get_user_email(user_id):
    user = db.get(user_id)
    return user.email  # What if user is None?

# ❌ ASSUMES key exists
def process_data(data):
    name = data['name']  # What if 'name' key doesn't exist?
    return name.upper()

# ❌ ASSUMES operation succeeds
def save_file(content, path):
    with open(path, 'w') as f:
        f.write(content)
    return True  # What if write failed?

# ❌ Silent failure
def delete_user(user_id):
    try:
        db.delete(user_id)
    except Exception:
        pass  # Silently swallows error!
```

**Result:** Silent failures, data corruption, security holes, "it should work" bugs

---

### **Good Code (Zero Assumptions):**

```python
from app.services.zero_assumption_dna import must_exist, must_have_key, no_silent_failures

# ✅ Verifies user exists
def get_user_email(user_id):
    user = db.get(user_id)
    must_exist(user, "user")  # Raises if None
    must_exist(user.email, "user.email")  # Verifies email exists
    return user.email

# ✅ Verifies key exists
def process_data(data):
    name = must_have_key(data, 'name')  # Raises if key missing
    must_not_be_empty(name, "name")  # Verifies not empty
    return name.upper()

# ✅ Verifies operation success
def save_file(content, path):
    try:
        with open(path, 'w') as f:
            bytes_written = f.write(content)
        
        # Verify write succeeded
        must_succeed(
            bytes_written,
            "file_write",
            lambda result: result > 0
        )
        return True
    except Exception as e:
        logger.error("File write failed", path=path, error=str(e))
        raise  # Re-raise, don't swallow

# ✅ No silent failures
@no_silent_failures("delete_user")
def delete_user(user_id):
    must_exist(user_id, "user_id")
    result = db.delete(user_id)
    must_succeed(result, "db_delete", lambda r: r.success)
    return result
```

**Result:** Explicit failures, early error detection, no silent bugs

---

## 📚 **API REFERENCE**

### **Core Verification Functions:**

#### **1. `must_exist(value, name, allow_none=False)`**
Verifies value exists (not None)

```python
from app.services.zero_assumption_dna import must_exist

user_id = request.get("user_id")
must_exist(user_id, "user_id")  # Raises if None

# Allow None explicitly
token = request.get("token")
must_exist(token, "token", allow_none=True)  # OK if None
```

#### **2. `must_be_type(value, expected_type, name)`**
Verifies value is correct type

```python
from app.services.zero_assumption_dna import must_be_type

age = request.get("age")
must_be_type(age, int, "age")  # Raises if not int

data = request.get("data")
must_be_type(data, dict, "data")  # Raises if not dict
```

#### **3. `must_not_be_empty(value, name)`**
Verifies collection is not empty

```python
from app.services.zero_assumption_dna import must_not_be_empty

users = db.query("SELECT * FROM users")
must_not_be_empty(users, "users")  # Raises if empty list

name = request.get("name")
must_not_be_empty(name, "name")  # Raises if empty string
```

#### **4. `must_have_key(data, key, dict_name="data")`**
Verifies dictionary key exists

```python
from app.services.zero_assumption_dna import must_have_key

config = load_config()
api_key = must_have_key(config, "api_key", "config")  # Raises if missing

user_data = get_user_data()
email = must_have_key(user_data, "email", "user_data")
```

#### **5. `must_succeed(result, operation, success_check)`**
Verifies operation succeeded

```python
from app.services.zero_assumption_dna import must_succeed

result = api_call()
must_succeed(
    result,
    "api_call",
    lambda r: r.status_code == 200
)

db_result = db.insert(data)
must_succeed(
    db_result,
    "database_insert",
    lambda r: r.success and r.id is not None
)
```

---

### **Decorators:**

#### **1. `@no_silent_failures(operation)`**
Ensures no silent failures

```python
from app.services.zero_assumption_dna import no_silent_failures

@no_silent_failures("create_user")
async def create_user(data):
    # If this fails, error is logged and re-raised
    # If this returns None, AssumptionViolation is raised
    user = await db.users.insert(data)
    return user
```

#### **2. `@verify_exists(allow_none=False)`**
Verifies all arguments exist

```python
from app.services.zero_assumption_dna import verify_exists

@verify_exists()
def calculate_total(price, quantity, tax_rate):
    # All args must not be None
    return price * quantity * (1 + tax_rate)

@verify_exists(allow_none=True)
def get_user_name(user_id, default_name=None):
    # user_id must exist, default_name can be None
    user = db.get(user_id)
    return user.name or default_name
```

---

### **ZeroAssumptionDNA Class:**

```python
from app.services.zero_assumption_dna import ZeroAssumptionDNA, VerificationLevel

# Create instance with strict verification
dna = ZeroAssumptionDNA(VerificationLevel.STRICT)

# Use verification methods
user_id = dna.verify_exists(request.get("user_id"), "user_id")
age = dna.verify_in_range(user.age, "age", min_val=0, max_val=150)
email = dna.verify_key_exists(user_data, "email", "user_data")

# Get violations report
report = dna.get_violations_report()
print(f"Total enforcements: {report['total_enforcements']}")
print(f"Total violations: {report['total_violations']}")
```

---

## 💡 **USAGE EXAMPLES**

### **Example 1: API Endpoint**

```python
from fastapi import APIRouter, HTTPException
from app.services.zero_assumption_dna import must_exist, must_have_key, must_not_be_empty

router = APIRouter()

@router.post("/users")
async def create_user(request: dict):
    """Create user - Zero Assumptions version"""
    
    # DO NOT ASSUME: request has required fields
    email = must_have_key(request, "email", "request")
    password = must_have_key(request, "password", "request")
    name = must_have_key(request, "name", "request")
    
    # DO NOT ASSUME: fields are not empty
    must_not_be_empty(email, "email")
    must_not_be_empty(password, "password")
    must_not_be_empty(name, "name")
    
    # DO NOT ASSUME: email is valid format
    if "@" not in email:
        raise HTTPException(400, "Invalid email format")
    
    # DO NOT ASSUME: password is strong enough
    if len(password) < 8:
        raise HTTPException(400, "Password too short")
    
    # DO NOT ASSUME: user creation succeeds
    try:
        user = await db.users.create({
            "email": email,
            "password": hash_password(password),
            "name": name
        })
        
        # DO NOT ASSUME: user object is valid
        must_exist(user, "created_user")
        must_exist(user.id, "user.id")
        
        return {"user_id": user.id, "email": user.email}
        
    except Exception as e:
        # DO NOT ASSUME: error handling is automatic
        logger.error("User creation failed", email=email, error=str(e))
        raise HTTPException(500, f"Failed to create user: {str(e)}")
```

---

### **Example 2: Database Operations**

```python
from app.services.zero_assumption_dna import must_exist, must_succeed, no_silent_failures

@no_silent_failures("database_query")
async def get_user_by_email(email: str):
    """Get user by email - Zero Assumptions"""
    
    # DO NOT ASSUME: email is provided
    must_exist(email, "email")
    must_not_be_empty(email, "email")
    
    # DO NOT ASSUME: database is connected
    if not db.is_connected():
        raise ConnectionError("Database not connected")
    
    # DO NOT ASSUME: query succeeds
    try:
        result = await db.users.find_one({"email": email})
    except Exception as e:
        logger.error("Database query failed", email=email, error=str(e))
        raise
    
    # DO NOT ASSUME: user exists
    if result is None:
        logger.warning("User not found", email=email)
        return None
    
    # DO NOT ASSUME: result has expected fields
    must_have_key(result, "id", "user")
    must_have_key(result, "email", "user")
    
    return result
```

---

### **Example 3: File Operations**

```python
from pathlib import Path
from app.services.zero_assumption_dna import must_exist, must_succeed

def read_config_file(config_path: str) -> dict:
    """Read config file - Zero Assumptions"""
    
    # DO NOT ASSUME: path is provided
    must_exist(config_path, "config_path")
    must_not_be_empty(config_path, "config_path")
    
    # DO NOT ASSUME: file exists
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    # DO NOT ASSUME: file is readable
    if not path.is_file():
        raise ValueError(f"Path is not a file: {config_path}")
    
    # DO NOT ASSUME: read succeeds
    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        logger.error("Failed to read config", path=config_path, error=str(e))
        raise
    
    # DO NOT ASSUME: content is not empty
    must_not_be_empty(content, "config_content")
    
    # DO NOT ASSUME: JSON parsing succeeds
    try:
        import json
        config = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in config", path=config_path, error=str(e))
        raise ValueError(f"Invalid JSON in config: {str(e)}")
    
    # DO NOT ASSUME: config has required keys
    must_have_key(config, "api_key", "config")
    must_have_key(config, "database_url", "config")
    
    return config
```

---

### **Example 4: User Confirmation**

```python
from app.services.zero_assumption_dna import zero_assumption_dna

async def delete_user_account(user_id: str, confirmed: bool = False):
    """Delete user account - requires explicit confirmation"""
    
    # DO NOT ASSUME: user wants to delete
    if not confirmed:
        # This logs the requirement for explicit confirmation
        zero_assumption_dna.require_explicit_confirmation(
            action="delete_user_account",
            danger_level="critical"
        )
        raise ValueError(
            "Account deletion requires explicit confirmation. "
            "Must pass confirmed=True after user confirms."
        )
    
    # DO NOT ASSUME: user_id is valid
    must_exist(user_id, "user_id")
    
    user = await db.users.get(user_id)
    must_exist(user, "user")
    
    # Proceed with deletion
    result = await db.users.delete(user_id)
    must_succeed(result, "user_deletion", lambda r: r.deleted_count > 0)
    
    logger.info("User account deleted", user_id=user_id)
    return True
```

---

## 🎯 **INTEGRATION EXAMPLES**

### **With FastAPI:**

```python
from fastapi import FastAPI, Depends, HTTPException
from app.services.zero_assumption_dna import must_exist, must_have_key

app = FastAPI()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user - Zero Assumptions"""
    # DO NOT ASSUME: token is valid
    must_exist(token, "authentication_token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")
    
    # DO NOT ASSUME: payload has user_id
    user_id = must_have_key(payload, "sub", "token_payload")
    
    # DO NOT ASSUME: user exists
    user = await get_user_by_id(user_id)
    must_exist(user, "user")
    
    return user

@app.get("/me")
async def read_users_me(current_user = Depends(get_current_user)):
    # current_user is guaranteed to exist and be valid
    return current_user
```

---

### **With Pydantic:**

```python
from pydantic import BaseModel, validator
from app.services.zero_assumption_dna import must_not_be_empty, must_be_type

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    
    @validator('email')
    def email_must_be_valid(cls, v):
        # DO NOT ASSUME: email format is correct
        must_not_be_empty(v, "email")
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v
    
    @validator('password')
    def password_must_be_strong(cls, v):
        # DO NOT ASSUME: password is strong
        must_not_be_empty(v, "password")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
    
    @validator('name')
    def name_must_exist(cls, v):
        # DO NOT ASSUME: name is provided
        must_not_be_empty(v, "name")
        return v
```

---

## 📊 **MONITORING & REPORTING**

### **Get Violations Report:**

```python
from app.services.zero_assumption_dna import zero_assumption_dna

# Get report
report = zero_assumption_dna.get_violations_report()

print(f"Total Enforcements: {report['total_enforcements']}")
print(f"Total Violations Caught: {report['total_violations']}")
print(f"Violation Types: {report['violation_types']}")
print(f"Recent Violations: {report['recent_violations']}")
```

**Example Output:**
```json
{
  "total_enforcements": 1543,
  "total_violations": 23,
  "violation_types": {
    "existence": 12,
    "type_mismatch": 5,
    "missing_key": 4,
    "empty_collection": 2
  },
  "recent_violations": [
    {
      "type": "missing_key",
      "dict_name": "request",
      "key": "email",
      "timestamp": "2025-10-09T10:00:00"
    }
  ],
  "principle": "DO NOT ASSUME ANYTHING"
}
```

---

## 🚀 **BEST PRACTICES**

### **1. Use at API Boundaries**
```python
# ✅ Good: Verify all external inputs
@app.post("/api/users")
async def create_user(request: dict):
    email = must_have_key(request, "email")
    password = must_have_key(request, "password")
    ...
```

### **2. Use for Critical Operations**
```python
# ✅ Good: Verify critical database operations
@no_silent_failures("payment_processing")
async def process_payment(amount, user_id):
    must_exist(amount, "amount")
    must_exist(user_id, "user_id")
    ...
```

### **3. Use for Data Transformations**
```python
# ✅ Good: Verify data before transformation
def transform_user_data(raw_data):
    must_be_type(raw_data, dict, "raw_data")
    email = must_have_key(raw_data, "email")
    must_not_be_empty(email, "email")
    ...
```

### **4. Don't Overuse in Internal Logic**
```python
# ❌ Too much: Internal calculations don't need verification
def calculate_tax(price):
    must_exist(price, "price")  # Overkill for internal function
    must_be_type(price, float, "price")  # Overkill
    return price * 0.1

# ✅ Better: Trust internal calculations, verify at boundaries
def calculate_tax(price):
    return price * 0.1
```

---

## 🎯 **WHEN TO USE**

### **Always Use:**
- ✅ API endpoints (external input)
- ✅ Database operations (data integrity)
- ✅ File operations (IO can fail)
- ✅ External API calls (network can fail)
- ✅ User authentication (security critical)
- ✅ Payment processing (money involved)
- ✅ Critical business logic

### **Consider Using:**
- 📝 Data transformations
- 📝 Complex algorithms
- 📝 State management
- 📝 Configuration loading

### **Don't Need:**
- ❌ Simple calculations
- ❌ Internal utility functions
- ❌ Pure functions with type hints
- ❌ Already validated data

---

## 🎉 **BENEFITS**

1. **No Silent Failures** - All errors are explicit and logged
2. **Early Error Detection** - Catch problems at the boundary
3. **Clear Error Messages** - Know exactly what went wrong
4. **Maintainable Code** - Explicit expectations
5. **Debugging Made Easy** - Clear violation logs
6. **Security** - No assumptions about user input
7. **Reliability** - No "it should work" bugs

---

## 📚 **SUMMARY**

**Zero Assumption DNA Principle:**

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   DO NOT ASSUME ANYTHING                                  ║
║                                                           ║
║   ✅ Verify everything explicitly                         ║
║   ✅ Validate all inputs                                  ║
║   ✅ Check all return values                              ║
║   ✅ Handle all errors                                    ║
║   ✅ Get explicit confirmation                            ║
║   ✅ Log everything                                       ║
║   ✅ Fail loudly, not silently                            ║
║                                                           ║
║   Result: Reliable, maintainable, secure code            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**Core of CognoMega!** 🧬

