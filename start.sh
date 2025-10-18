#!/bin/bash

# 1. Start the backend server on an internal port (e.g., 8000)
# NOTE: Your server.py must be configured to listen on 8000 (or whichever port you choose)
python server.py & 

# 2. Start the Chainlit application on the external port provided by Railway ($PORT)
# The Chainlit app will need to know the internal port of the backend server (8000).
chainlit run app.py --host 0.0.0.0 --port $PORT

# Wait for all background processes to finish (optional, but good practice)
wait