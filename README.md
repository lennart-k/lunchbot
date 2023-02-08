# Lunchbot (always hungry)

Disclaimer: This codebase is pure jank, contains lots of bodges.

asks for lunch so you don't have to

Also features previews of the menu by Craiyon and DALLE 2.
The latter must currently be updated in the source code. Sorry :/

## Requirements

My fork of mensa-utils from here: https://github.com/lennart-k/mensa-utils
Install using
```
pip install git+https://github.com/lennart-k/mensa-utils
```

## Docker setup


```
cp docker-compose.yml{.example,}
# Insert your environment variables
docker-compose up
```
