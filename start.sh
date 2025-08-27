#!/bin/bash
source ~/.bashrc
conda activate agent_env
cd agent && python app.py &
cd front-end-react-v2 && bash start.sh start
