# Presentation
A Python script which when given a text file and a template, will generate a colorful HTML slide-show.
## Getting started
The easiest way to run the script is to clone the repo or download the zip. Make sure Python 3.x is installed (untested on Python 2.x).
```
git clone https://github.com/tom-ando/Presentation.git
cd ./Presentation
python3 ./generate.py test.txt
```
The final file can be found in `./output/index.html`. This file can be sent off or moved and needs no dependencies other than itself.
### Templates
The scripts reads 3 templates from `./template`, `css.txt`, `js.txt` and `html.txt`. They can all be modified to any extent. Please not, placeholders (look like `[~placeholder]`) must still be included, although they can be moved around to other places to change the functionality and look of the slide-show. A fresh set of the templates can always be found on this GitHub page.
## Bugs/Ideas
If you want to get in touch with me I can be found at `portlester.tom@gmail.com`.
