#!/bin/bash
if ! [ -d altynai ]; then
  git clone https://GITHUB_ACCESS_TOKEN@github.com/wthlolbbq/altynai.git
fi

cd altynai
git pull
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:/home/container/altynai/"
python bot/main.py