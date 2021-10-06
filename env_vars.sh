echo 'To start dev server: source ./displayboard/env_vars.sh'
export SESSION_TYPE=redis
export SESSION_REDIS=redis://127.0.0.1:6379
export FLASK_APP=$PWD/app
export FLASK_DEBUG=1
flask run --host=0.0.0.0
