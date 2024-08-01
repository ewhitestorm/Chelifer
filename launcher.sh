#!/usr/bin/bash
source .venv/bin/activate
cd app/
uvicorn main:app --port 8080 --reload 2> ./logs/launcher.log
result=$(tac ./logs/launcher.log | head -n 1)
if [[ "$result" == "ERROR"* ]]
then
sudo lsof -t -i tcp:8080 | xargs kill -9
uvicorn main:app --port 8080 --reload 2> ./logs/launcher.log
else
uvicorn main:app --port 8000 --reload 2> ./logs/launcher.log
fi
deactivate
cd ..
chmod +x launcher.sh
trap './launcher.sh' EXIT