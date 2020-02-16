#!/bin/sh
exec pipenv run gunicorn -b :5000 server:app
