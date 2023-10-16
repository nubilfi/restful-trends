import multiprocessing
import os

debug = os.getenv('DEBUG', False)

# Host and port
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

# Number of worker processes (adjust as needed)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class for UVicorn
worker_class = "uvicorn.workers.UvicornWorker"
