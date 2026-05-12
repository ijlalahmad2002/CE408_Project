import logging
import time
import random
import os

# ── Setup ────────────────────────────────────────────────────────────────────
LOG_FILE = "/var/log/myapp/app.log"
os.makedirs("/var/log/myapp", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

# ── Events ───────────────────────────────────────────────────────────────────
INFO_EVENTS = [
    "User logged in successfully",
    "File uploaded successfully",
    "API request completed",
    "User profile updated",
    "Payment processed successfully",
    "Session started",
    "Data fetched from database",
]

WARNING_EVENTS = [
    "Database response slow (2.3s)",
    "Memory usage above 70%",
    "API response time high",
    "Disk space below 20%",
    "Retry attempt on failed request",
]

ERROR_EVENTS = [
    "Failed to connect to database",
    "Payment gateway timeout",
    "Unhandled exception in API handler",
    "File not found: config.json",
    "Authentication service unreachable",
    "OutOfMemory: Java heap space",
    "CRITICAL: Segmentation fault in worker",
]

# ── Mode control ─────────────────────────────────────────────────────────────
# Change this to "error" during your demo to trigger alerts
MODE = "error"

def generate_log():
    if MODE == "normal":
        weights = [75, 20, 5]   # mostly INFO, rare errors
    else:
        weights = [10, 10, 80]  # flood of errors — triggers alerts

    level = random.choices(["INFO", "WARNING", "ERROR"], weights=weights)[0]

    if level == "INFO":
        logging.info(random.choice(INFO_EVENTS))
    elif level == "WARNING":
        logging.warning(random.choice(WARNING_EVENTS))
    else:
        logging.error(random.choice(ERROR_EVENTS))

# ── Main loop ─────────────────────────────────────────────────────────────────
print("Log generator started. Writing to", LOG_FILE)
print("Press Ctrl+C to stop.")

while True:
    generate_log()
    time.sleep(2)  # new log every 2 seconds