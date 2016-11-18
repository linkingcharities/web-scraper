#!/bin/bash

source venv/bin/activate
rm charities.json
scrapy crawl charities -o charities.json
deactivate