import sys
import fileinput
import os
from random import randint
from shutil import copyfile

customMode = False

colors = {
    "red": [255, 0, 0],
    "pink": [255, 193, 203],
    "orange": [255, 165, 0],
    "yellow": [255, 195, 0],
    "purple": [128, 0, 128],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "brown": [165, 42, 42],
    "white": [255, 255, 255],
    "gray": [128, 128, 128]
}

# Keeps prompting for response until valid response
def getInput(prompt, allowed):
    while True:
        userInput = input(prompt)
        if userInput in allowed:
            return userInput

# Stops the script if something is missing
def checkPath(path):
    if not os.path.exists(path):
        print("[!] Missing file/directory or insufficent permissions: {}".format(path))
        sys.exit()

# Returns the substring between two placeholders
def extractString(string, placeholder):
    return string.split(placeholder)[1]

# Saves a files
def saveFile(filePath, content):
    with open(filePath, "w+") as f:
        f.write(content)

# Saves all the files in one file
def saveSingle(htmlContent, jsContent, cssContent):
    print("[+] Writing to ./output/index.html")
    htmlContent = htmlContent.replace("[~css]", "<style>" + cssContent + "</style>")
    htmlContent = htmlContent.replace("[~script]", "<script>" + jsContent + "</script>")
    saveFile("./output/index.html", htmlContent)

# Splits the files up into each language
def saveMultiple(htmlContent, jsContent, cssContent):
    print("[+] Writing to files in ./output")
    htmlContent = htmlContent.replace("[~css]", '<link rel="stylesheet" type="text/css" href="main.css"/>')
    htmlContent = htmlContent.replace("[~script]", '<script src="main.js"></script>')
    saveFile("./output/index.html", htmlContent)
    saveFile("./output/main.css", cssContent)
    saveFile("./output/main.js", jsContent)

# Returns a random RGB color
def generateRgb():
    return [randint(0,255), randint(0,255), randint(0,255)]

# Checks for all the files and folders required
def checkFiles():
    print("[+] Checking if includes exist")
    checkPath(sys.argv[1])
    checkPath("./template/html.txt")
    checkPath("./template/css.txt")
    checkPath("./template/js.txt")
    # Checks for output directory and creates one if needed
    if not os.path.exists("./output"):
        print("[-] Output directory not found. Creating")
        os.makedirs("./output")

# Opens template files
def loadTemplate(templateFile):
    print("[+] Loading templates")
    template = {}
    with open(templateFile) as f:
        f = f.read()
        template["html"] = extractString(f, "[~html]")
        template["slide"] = extractString(f, "[~slide]")
        template["heading"] = extractString(f, "[~heading]")
        template["contentSection"] = extractString(f, "[~contentSection]")
        template["content"] = extractString(f, "[~content]")
        template["controls"] = extractString(f, "[~controlSection]")
    print("[+] Loaded all templates")
    return template

# Parses the input file
def parseInputFile(inputFile, template):
    print("[+] Parsing input file")

    # Holds the html file
    parsedFile = template["html"]
    firstLine = True
    slideCounter = 0

    for line in fileinput.input(inputFile):
        line = list(line)

        # Finds where the "-" is, signifying what type of dot point it is
        for counter in range(len(line)):
            if line[counter] == "-":
                break
            elif line[counter] != " ":
                counter = -1
                break

        # Removes dashes and extra spaces from start of line and newline from end
        line = "".join(line)[counter + 1:len(line) - 1].strip()

        if firstLine:
            # Line type is a title
            if counter == -1:
                title = line

            # No heading supplied
            else:
                title = "Presentation"

            # Puts the heading in the page
            parsedFile = parsedFile.replace("[~title]", title)
            firstLine = False

        # Slide heading (automatically makes new slide)
        if counter == 0:
            # Clears tags from previous slide
            parsedFile = parsedFile.replace("[~contentSectionContent]", "")
            # Adds a new slide
            parsedFile = parsedFile.replace("[~slideSection]", template["slide"] + "[~slideSection]")
            # Puts in slide ID
            parsedFile = parsedFile.replace("[~slideId]", str(slideCounter))
            # Adds a heading to the slide and adds the ul element to house the points
            parsedFile = parsedFile.replace("[~slideContent]", template["heading"].replace("[~headingContent]", line) + template["contentSection"])
            slideCounter += 1

        # Content
        elif counter == 1:
            # Adds another point and puts the line in the content section
            parsedFile = parsedFile.replace("[~contentSectionContent]", template["content"] + "[~contentSectionContent]").replace("[~contentContent]", line)

    print("[+] Successfully parsed input file")
    return parsedFile

# Adds a background image
def setImageBackground(htmlContent):
    while True:
        imagePath = input("[+] Image path for background (blank for none): ")
        if imagePath != "":
            if os.path.exists(imagePath):
                htmlContent = htmlContent.replace("[~background]", '<img id="background" src="background.jpg"/>')
                print("    [+] Copying image from {} to ./output/background.jpg".format(imagePath))
                copyfile(imagePath, "./output/background.jpg")
                break
            else:
                print("    [!] Image doesn't exist or invalid permissions")
        # User inputted nothing
        else:
            break
    return htmlContent

# Removes all the placeholders
def removePlaceholder(htmlContent):
    return htmlContent.replace("[~contentSectionContent]", "").replace("[~slideSection]", "").replace("[~background]", "").replace("[~controls]", "")

def determineTextColor(backgroundColor):
    # 383 = (255 * 3) / 2
    if sum(backgroundColor[0:len(backgroundColor)]) < 383:
        textColor = "white"
    else:
        textColor = "black"
    return textColor

# Generates either a random or custom theme depending on customMode
def generateTheme(cssContent):
    global customMode
    global colors
    global html
    print("[+] Generating theme")
    # Makes a rgb color
    if customMode:
        # Not using getInput function because of custom rules
        while True:
            backgroundColor = input("    [+] Pick a background color (basic color name or rgb value or enter for random): ")
            # A valid pre-known color
            if backgroundColor in colors:
                backgroundColor = colors[backgroundColor]
                break
            # Custom rgb color
            elif backgroundColor[:3] == "rgb":
                # No input
                if backgroundColor == "":
                    break

                # Set to false if loop needs to be rerun
                valid = True
                try:
                    backgroundColor = [int(i) for i in backgroundColor[4:].split(" ") if (int(i) <= 255) and (int(i) >= 0)]
                except:
                    valid = False
                    print("    [-] Not a valid rgb value")
                    backgroundColor = generateRgb()

                if valid:
                    break

            # No input
            elif backgroundColor == "":
                backgroundColor = generateRgb()
                break

            else:
                print("    [-] Not a valid rgb value")

        # Setting opacity for background
        if ('<img id="background"' in html):
            defaultOpacity = 0.4
        else:
            defaultOpacity = 1
        # Not using getInput function because of custom rules
        while True:
            try:
                opacity = float(input("    [+] Opacity for background (between 0-1. Default {}): ".format(defaultOpacity)))
            except:
                opacity = defaultOpacity

            if opacity >= 0 and opacity <= 1:
                break
            else:
                print("        [-] Not a number between 0-1")
    else:
        backgroundColor = generateRgb()
        opacity = 1
    textColor = determineTextColor(backgroundColor)
    backgroundColor = "rgba(" + str(backgroundColor)[1:-1] + ", " + str(opacity) + ")"
    print("    [+] Using " + backgroundColor + " with " + textColor + " text")

    # Applies theme to css
    return cssContent[0] + textColor + cssContent[1] + backgroundColor + cssContent[2] + textColor + cssContent[3]

def loadFile(filePath):
    with open(filePath) as f:
        return f.read()

def addControls(htmlContent, template):
    htmlContent = htmlContent.replace("[~controls]", template["controls"])
    return htmlContent

if len(sys.argv) < 2:
    print("Usage: {} /path/to/file [-c]".format(sys.argv[0]))
    print("   -c: Custom mode. Gives options to change things like background color")
else:
    # If custom flag set it will leave options for custom changes
    if len(sys.argv) == 3:
        if sys.argv[2] == "-c":
            customMode = True

    checkFiles()
    template = loadTemplate("./template/html.txt")
    print("[+] Opening css and js template files")
    css = loadFile("./template/css.txt").split("[~]")
    js = loadFile("./template/js.txt")

    # Parses the input file
    html = parseInputFile(sys.argv[1], template)

    if customMode:
        # Add controls
        controls = getInput("[+] Add controls to bottom of page? Y/n (default n): ", ("Y", "y", "N", "n", ""))
        if controls in ("Y", "y"):
            print("    [+] Adding controls")
            html = addControls(html, template)

        html = setImageBackground(html)

    html = removePlaceholder(html)

    css = generateTheme(css)

    # Writing to files
    if customMode:
        saveMode = getInput("[+] Save files in a [s]ingle file or [m]ultiple (blank for single): ", ("s", "S", "m", "M", ""))
        if saveMode in ("single", "s", ""):
            saveSingle(html, js, css)
        elif saveMode in ("multiple", "m"):
            saveMultiple(html, js, css)
    else:
        saveSingle(html, js, css)
    print("[+] Completed")
