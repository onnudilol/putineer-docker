# What is this
A stupid idea from a [streamer](http://malf.me/) that I implemented to mess with [PostGIS](https://postgis.net/) and [Vue](https://vuejs.org/) .
Not in any way affiliated with [poutineer.com](http://poutineer.com/).

# Deploy instructions
```
docker-compose build

docker-compose up

docker-compose exec putineer_web_1 ./manage.py migrate

cd src/static/poutineer && npm run build && docker exec putineer-docker_web_1 ./manage.py collectstatic --noinput
```

# Manually scraping Yelp
`docker-compose exec putineer_web_1 ./manage.py scrape_yelp`