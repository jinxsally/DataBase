#!/bin/sh
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v fe/test/test_search.py --ignore=fe/data
coverage combine
coverage report
coverage html
