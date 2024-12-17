"""private-gpt."""

import logging
import os
from datetime import datetime

# Set to 'DEBUG' to have extensive logging turned on, even for libraries
ROOT_LOG_LEVEL = "INFO"

PRETTY_LOG_FORMAT = (
    "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(name)+25s - %(message)s"
)
# Get the current date and time 
current_time = datetime.now().strftime("(date=%Y-%m-%d), (time=%H-%M-%S)")
# Configure logging 
log_directory = "/app/logs" 
# Directory inside the container 
log_filename = f"app_{current_time}.log" 
log_path = f"{log_directory}/{log_filename}" 
logging.basicConfig(
    level=ROOT_LOG_LEVEL, 
    format=PRETTY_LOG_FORMAT, datefmt="%H:%M:%S",
    handlers=[ 
        logging.FileHandler(log_path), 
        logging.StreamHandler() 
    ]
)
logging.captureWarnings(True)

# Disable gradio analytics
# This is done this way because gradio does not solely rely on what values are
# passed to gr.Blocks(enable_analytics=...) but also on the environment
# variable GRADIO_ANALYTICS_ENABLED. `gradio.strings` actually reads this env
# directly, so to fully disable gradio analytics we need to set this env var.
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

# Disable chromaDB telemetry
# It is already disabled, see PR#1144
# os.environ["ANONYMIZED_TELEMETRY"] = "False"

# adding tiktoken cache path within repo to be able to run in offline environment.
os.environ["TIKTOKEN_CACHE_DIR"] = "tiktoken_cache"
