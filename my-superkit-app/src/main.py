
from superkit import create_app
from config.settings import settings
from superkit.logging import log

dev = create_app(
    settings=settings,
    environment=settings.environment,
)

# ══════════════════════════════════════════════════════════════
# LOGGING SCENARIOS
# ══════════════════════════════════════════════════════════════

# 1. Simple text logging
@dev.get("/log-info")
def log_info():
    log.info(title="Server Status", message="Application is running normally")
    return {"status": "logged"}

@dev.get("/log-warning")
def log_warning():
    log.warning(title="High Memory Usage", message="Memory usage is at 85%")
    return {"status": "logged"}

@dev.get("/log-critical")
def log_critical():
    log.critical(title="Database Connection Lost", message="Unable to connect to primary database")
    return {"status": "logged"}


# 2. JSON logging
@dev.get("/log-json")
def log_json():
    log.info(title="User Created").add_json({
        "id": 12345,
        "username": "alice",
        "email": "alice@example.com",
        "created_at": "2025-01-20T10:51:24Z"
    })
    return {"status": "logged"}


# 3. Table logging
@dev.get("/log-table")
def log_table():
    log.info(title="Active Users").add_table([
        ["ID", "Name", "Email", "Status"],
        [1, "Alice", "alice@example.com", "Active"],
        [2, "Bob", "bob@example.com", "Inactive"],
        [3, "Charlie", "charlie@example.com", "Active"],
        [4, "Diana", "diana@example.com", "Pending"],
    ])
    return {"status": "logged"}


# 4. Mixed: Message + JSON
@dev.get("/log-mixed-json")
def log_mixed_json():
    log.warning(
        title="Authentication Failed",
        message="User attempted to login with invalid credentials"
    ).add_json({
        "username": "alice",
        "ip_address": "192.168.1.100",
        "attempt_count": 3,
        "timestamp": "2025-01-20T10:51:24Z"
    })
    return {"status": "logged"}


# 5. Mixed: Message + Table
@dev.get("/log-mixed-table")
def log_mixed_table():
    log.info(
        title="Database Query Performance",
        message="Slow queries detected in the last hour"
    ).add_table([
        ["Query", "Duration (ms)", "Table"],
        ["SELECT * FROM users", 1250, "users"],
        ["SELECT * FROM orders", 3400, "orders"],
        ["JOIN users and orders", 5600, "multiple"],
    ])
    return {"status": "logged"}


# 6. Mixed: Message + JSON + Table
@dev.get("/log-mixed-all")
def log_mixed_all():
    log.critical(
        title="System Resource Alert",
        message="Critical resource thresholds exceeded"
    ).add_json({
        "cpu_usage": "92%",
        "memory_usage": "88%",
        "disk_usage": "76%",
        "alert_level": "critical"
    }).add_table([
        ["Process", "CPU", "Memory", "Status"],
        ["app_server", "45%", "3.2GB", "Running"],
        ["database", "38%", "4.1GB", "Running"],
        ["cache", "9%", "850MB", "Running"],
    ])
    return {"status": "logged"}


# 7. Multiple JSON objects
@dev.get("/log-multiple-json")
def log_multiple_json():
    log.info(
        title="API Response Comparison",
        message="Comparing responses from multiple endpoints"
    ).add_json({
        "endpoint": "/api/v1/users",
        "response_time": "120ms",
        "status": 200
    }).add_json({
        "endpoint": "/api/v2/users",
        "response_time": "85ms",
        "status": 200
    })
    return {"status": "logged"}


# 8. Multiple Tables
@dev.get("/log-multiple-tables")
def log_multiple_tables():
    log.warning(
        title="Service Health Check",
        message="Multiple services reporting degraded performance"
    ).add_table([
        ["Service", "Status", "Latency"],
        ["Auth Service", "Healthy", "45ms"],
        ["Payment Service", "Degraded", "350ms"],
        ["Email Service", "Healthy", "120ms"],
    ]).add_table([
        ["Database", "Connections", "Query Time"],
        ["Primary DB", "45/100", "25ms"],
        ["Replica DB", "32/100", "18ms"],
        ["Cache", "850/1000", "2ms"],
    ])
    return {"status": "logged"}


# 9. Large JSON object
@dev.get("/log-large-json")
def log_large_json():
    log.info(title="Application Configuration").add_json({
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 4,
            "timeout": 30
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp",
            "pool_size": 20,
            "max_overflow": 10
        },
        "cache": {
            "backend": "redis",
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "ttl": 3600
        },
        "features": {
            "analytics": True,
            "notifications": True,
            "beta_features": False
        }
    })
    return {"status": "logged"}


# 10. Large table
@dev.get("/log-large-table")
def log_large_table():
    rows = [["ID", "Username", "Email", "Status", "Last Login", "Role"]]
    for i in range(1, 21):
        rows.append([
            i,
            f"user{i}",
            f"user{i}@example.com",
            "Active" if i % 2 == 0 else "Inactive",
            f"2025-01-{20-i:02d}",
            "Admin" if i % 5 == 0 else "User"
        ])
    
    log.info(title="User Database Report", message="Complete user listing").add_table(rows)
    return {"status": "logged"}


# 11. Nested JSON structure
@dev.get("/log-nested-json")
def log_nested_json():
    log.info(title="API Request/Response").add_json({
        "request": {
            "method": "POST",
            "url": "/api/users",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer token123"
            },
            "body": {
                "username": "newuser",
                "email": "newuser@example.com"
            }
        },
        "response": {
            "status": 201,
            "body": {
                "id": 999,
                "username": "newuser",
                "created_at": "2025-01-20T10:51:24Z"
            }
        }
    })
    return {"status": "logged"}


# 12. Empty data edge cases
@dev.get("/log-empty-json")
def log_empty_json():
    log.info(title="Empty Configuration").add_json({})
    return {"status": "logged"}

@dev.get("/log-empty-table")
def log_empty_table():
    log.info(title="No Data Available").add_table([])
    return {"status": "logged"}


# 13. Long messages
@dev.get("/log-long-message")
def log_long_message():
    log.warning(
        title="Detailed Error Report",
        message="The system encountered a complex error during the processing of a large batch job. "
                "This error was caused by multiple factors including network timeouts, database connection "
                "pool exhaustion, and memory constraints. The system attempted automatic recovery but was "
                "unable to complete the operation. Manual intervention may be required to resolve this issue."
    )
    return {"status": "logged"}


# 14. Special characters in data
@dev.get("/log-special-chars")
def log_special_chars():
    log.info(title="Special Characters Test").add_json({
        "unicode": "Hello 世界 🌍",
        "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?",
        "quotes": 'Single \' and Double " quotes',
        "newlines": "Line 1\nLine 2\nLine 3",
        "tabs": "Column1\tColumn2\tColumn3"
    })
    return {"status": "logged"}


# 15. Sequential logging
@dev.get("/log-sequence")
def log_sequence():
    log.info(title="Step 1", message="Starting process")
    log.info(title="Step 2", message="Loading configuration").add_json({"config": "loaded"})
    log.warning(title="Step 3", message="Detected potential issue").add_table([
        ["Check", "Status"],
        ["Memory", "Warning"],
        ["Disk", "OK"],
    ])
    log.info(title="Step 4", message="Process completed successfully")
    return {"status": "logged"}


# ══════════════════════════════════════════════════════════════
# ERROR SCENARIOS
# ══════════════════════════════════════════════════════════════

# 1. Simple Division Error
def calc(a: int, b: int):
    return a / b

@dev.get("/boom")
def boom():
    calc(1, 0)


# 2. Deep Nested Call Stack
def level_1():
    return level_2()

def level_2():
    return level_3()

def level_3():
    return level_4()

def level_4():
    return level_5()

def level_5():
    data = {"users": [{"name": "Alice"}]}
    return data["users"][5]["name"]  # IndexError

@dev.get("/deep-error")
def deep_error():
    return level_1()


# 3. Type Error with Multiple Calls
def process_user(user_id):
    user = fetch_user(user_id)
    return calculate_score(user)

def fetch_user(user_id):
    return {"id": user_id, "name": "Bob"}

def calculate_score(user):
    # This will fail because user is a dict, not a number
    return user + 100  # TypeError

@dev.get("/type-error")
def type_error_endpoint():
    return process_user(42)


# 4. Attribute Error Chain
class UserService:
    def get_profile(self, user_id):
        db = self.connect_db()
        return db.query_user(user_id)
    
    def connect_db(self):
        return None  # Oops, forgot to return actual DB

@dev.get("/attribute-error")
def attribute_error_endpoint():
    service = UserService()
    return service.get_profile(123)


# 5. Key Error with Nested Dicts
def parse_api_response(response):
    return extract_user_data(response)

def extract_user_data(response):
    return get_nested_value(response)

def get_nested_value(data):
    return data["result"]["data"]["user"]["email"]  # KeyError

@dev.get("/key-error")
def key_error_endpoint():
    response = {"result": {"data": {}}}  # Missing 'user' key
    return parse_api_response(response)


# 6. Value Error with Conversion
def convert_string_to_int(value):
    return validate_and_convert(value)

def validate_and_convert(value):
    return int(value)  # ValueError if not a number

@dev.get("/value-error")
def value_error_endpoint():
    return convert_string_to_int("not-a-number")


# 7. Import Error Simulation (File Not Found)
def load_config():
    return read_config_file()

def read_config_file():
    with open("nonexistent_file.json") as f:  # FileNotFoundError
        return f.read()

@dev.get("/file-error")
def file_error_endpoint():
    return load_config()


# 8. Recursion Error
def recursive_function(n):
    return recursive_function(n + 1)  # Never ends

@dev.get("/recursion-error")
def recursion_error_endpoint():
    return recursive_function(0)


# 9. Multiple Function Calls Leading to Error
def step_a(x):
    return step_b(x * 2)

def step_b(x):
    return step_c(x + 10)

def step_c(x):
    return step_d(x - 5)

def step_d(x):
    items = [1, 2, 3]
    return items[x]  # IndexError if x >= 3

@dev.get("/multi-step-error")
def multi_step_error():
    return step_a(5)  # 5*2=10, 10+10=20, 20-5=15, items[15] -> error


# 10. Exception in List Comprehension
def process_numbers(numbers):
    return [transform_number(n) for n in numbers]

def transform_number(n):
    if n == 0:
        raise ValueError("Cannot process zero!")
    return 100 / n

@dev.get("/list-comp-error")
def list_comp_error():
    return process_numbers([5, 3, 0, 2])


# 11. Class Method Error Chain
class Calculator:
    def __init__(self, base_value):
        self.base = base_value
    
    def multiply(self, x):
        return self.apply_operation(x, "multiply")
    
    def apply_operation(self, x, operation):
        return self.execute(x, operation)
    
    def execute(self, x, operation):
        if operation == "multiply":
            return self.base * x
        return self.base.unknown_method()  # AttributeError

@dev.get("/class-error")
def class_error_endpoint():
    calc = Calculator(10)
    return calc.apply_operation(5, "divide")


# 12. Async Error (if using async)
async def async_level_1():
    return await async_level_2()

async def async_level_2():
    return await async_level_3()

async def async_level_3():
    return 1 / 0

@dev.get("/async-error")
async def async_error_endpoint():
    return await async_level_1()


# 13. JSON Parsing Error
import json

def parse_json_data(json_string):
    return decode_json(json_string)

def decode_json(json_string):
    return json.loads(json_string)  # JSONDecodeError

@dev.get("/json-error")
def json_error_endpoint():
    bad_json = '{"name": "Alice", "age": }'  # Invalid JSON
    return parse_json_data(bad_json)


# 14. None Type Error Chain
def get_user_settings():
    user = get_current_user()
    return user.settings  # AttributeError: NoneType has no attribute 'settings'

def get_current_user():
    return fetch_from_database()

def fetch_from_database():
    return None  # Simulating no user found

@dev.get("/none-error")
def none_error_endpoint():
    return get_user_settings()
