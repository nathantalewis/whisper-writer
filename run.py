import os
import sys
import subprocess


def load_env(env_file='.env'):
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if (value.startswith("'") and value.endswith("'")) or \
                       (value.startswith('"') and value.endswith('"')):
                        value = value[1:-1]

                    # Expand environment variables in the value
                    value = os.path.expandvars(value)

                    os.environ[key] = value


# Load environment variables
load_env()

# Run the main script
subprocess.run([sys.executable, os.path.join('src', 'main.py')])
