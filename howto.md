# make venv

Using conda

Create venv in project
`conda env create --prefix ./venv`

Create venv in project and specify what to install in requirements.txt
`conda create --prefix ./venv python --file requirements.txt`


Create venv under Anaconda wings and specify what to install in requirements.txt
`conda create --name emavenv python=3.8 --file requirements.txt`

This doesn't seem to work
`conda env update -f venvConfig.yml`

Activate using the full path
`conda activate /home/owit/Nextcloud/pyShare/ema/venv`


Resources

https://betterprogramming.pub/building-your-first-website-with-flask-part-2-6324721be2ae
https://betterprogramming.pub/building-your-first-website-with-flask-part-5-e389fff0c8ec

https://flask-mobility.readthedocs.io/en/latest/


# Todo
- mobile friendly
- nicer CSS

