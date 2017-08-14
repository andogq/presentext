# presentext
A Python script which when given a text file and a template, will generate a colorful HTML slide-show. The text file involves very simple formatting and indentation (think a cousin of markdown) which will be interpreted as a heading or a title or a dot point, and included as it should be. The final file should be usable as a presentation in place of a PowerPoint or a Keynote.
## Getting started
The easiest way to run the script is to clone the repo or download the zip. Make sure Python 3.x is installed (untested on Python 2.x).
```
git clone https://github.com/tom-ando/presentext.git
cd ./presentext
python3 ./generate.py test.txt
```
The final file can be found in `./output/index.html`. This file can be sent off or moved and needs no dependencies other than itself.
### Templates
The scripts reads 3 templates from `./template`, `css.txt`, `js.txt` and `html.txt`. They can all be modified to any extent. Please not, placeholders (look like `[~placeholder]`) must still be included, although they can be moved around to other places to change the functionality and look of the slide-show. A fresh set of the templates can always be found on this GitHub page.
### Images as backgrounds
Exactly as it sounds. Images can be used as a background for the slide-show. Either have an image in the base directory called `background.jpg` or specify a particular one with the custom mode.
### Input file
The syntax of the input file is very simple. No indentation or hyphens for a title, one hyphen for a slide heading (and consequently a new slide) and a space and a hyphen for a dot point on the slide. 
```
Title of presentation (can only be used once)
- Heading of slide 1
 - Dot point on slide 1
 - Another dot point
- Another slide
 - More dot points
```
### Slide show
The slide show can be navigated with arrow keys, clicking on one of the sides of a slide or with the spacebar. The script will generate a random color to use as the background of the slides, which can be customised in custom mode.
### Custom mode
Custom mode can be used with a `-c` on the end of the command.
```python3 ./generate.py test.txt -c```
When run any part of the script can be changed, when prompted. Custom locations for images can be used, along with specific colors for backgrounds and options for controls. Take a look!
## Bugs/Ideas
If you want to get in touch with me I can be found at `portlester.tom@gmail.com`.
