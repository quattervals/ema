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

Update from requirements.txt
`conda install  --file requirements.txt`

## Resources

https://betterprogramming.pub/building-your-first-website-with-flask-part-2-6324721be2ae
https://betterprogramming.pub/building-your-first-website-with-flask-part-5-e389fff0c8ec

https://flask-mobility.readthedocs.io/en/latest/

https://www.w3schools.com/howto/howto_css_four_columns.asp
https://www.freecodecamp.org/news/how-to-create-an-image-gallery-with-css-grid-e0f0fd666a5c/

https://www.w3schools.com/howto/howto_js_image_grid.asp

https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout

# Todo
- mobile friendly
  https://travishorn.com/responsive-grid-in-2-minutes-with-css-grid-layout-4842a41420fe
  - worked well
  https://www.w3schools.com/howto/howto_js_topnav.asp
  - nice menu
- expand image when clicked on
  - https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal_img
  - http://jsfiddle.net/vngx/qxyx4u73/


## Plot
- restrict temp, heigth to 0...5000m, always same format
- nicer colors
- check gradient ranges