import sys
import fileinput
import os
from random import randint

template = {}
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

# Stops the script if something is missing
def checkFile(filePath):
    if not os.path.exists(filePath):
        print("[!] Missing file/directory or insufficent permissions: {}".format(filePath))
        sys.exit()


if len(sys.argv) < 2:
    print("Usage: {} /path/to/file [-c]".format(sys.argv[0]))
    print("   -c: Custom mode. Gives options to change things like background color")
else:
    # If custom flag set it will leave options for custom changes
    if len(sys.argv) == 3:
        if sys.argv[2] == "-c":
            customMode = True

    # Checks for all the files required
    print("[+] Checking if files exist")
    checkFile(sys.argv[1])
    checkFile("./template/html.txt")
    checkFile("./template/css.txt")
    checkFile("./template/js.txt")

    # Opens template files
    print("[+] Loading templates")
    with open("./template/html.txt") as f:
        f = f.read()
        template["html"] = f.split("[~html]")[1]
        template["slide"] = f.split("[~slide]")[1]
        template["heading"] = f.split("[~heading]")[1]
        template["contentSection"] = f.split("[~contentSection]")[1]
        template["content"] = f.split("[~content]")[1]
    print("[+] Loaded all templates")

    # Holds the html file
    html = template["html"]

    firstLine = True
    slideCounter = 0

    # Parses the input file
    print("[+] Parsing input file")
    for line in fileinput.input(sys.argv[1]):
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
            html = html.replace("[~title]", title)
            firstLine = False

        # Slide heading (automatically makes new slide)
        if counter == 0:
            # Clears tags from previous slide
            html = html.replace("[~contentSectionContent]", "")
            # Adds a new slide
            html = html.replace("[~slideSection]", template["slide"] + "[~slideSection]")
            # Puts in slide ID
            html = html.replace("[~slideId]", str(slideCounter))
            # Adds a heading to the slide and adds the ul element to house the points
            html = html.replace("[~slideContent]", template["heading"].replace("[~headingContent]", line) + template["contentSection"])
            slideCounter += 1

        # Content
        elif counter == 1:
            # Adds another point and puts the line in the content section
            html = html.replace("[~contentSectionContent]", template["content"] + "[~contentSectionContent]").replace("[~contentContent]", line)

    # Removes extra placeholders
    html = html.replace("[~contentSectionContent]", "").replace("[~slideSection]", "")
    print("[+] Successfully parsed input file")

    print("[+] Generating theme")
    # Makes a rgb color
    if customMode:
        backgroundColor = input("    [+] Pick a background color (basic color name or rgb value): ")
        if backgroundColor in colors:
            backgroundColor = colors[backgroundColor]
        elif backgroundColor[:3] == "rgb":
            try:
                backgroundColor = [int(i) for i in backgroundColor[4:].split(" ") if (int(i) <= 255) and (int(i) >= 0)]
            except:
                print("    [+] Not a valid rgb value. Try 'rgb 123 123 123'")
                backgroundColor = [randint(0,255), randint(0,255), randint(0,255)]
        else:
            print("    [+] Not a valid rgb value. Try 'rgb 123 123 123'")
            backgroundColor = [randint(0,255), randint(0,255), randint(0,255)]

    else:
        backgroundColor = [randint(0,255), randint(0,255), randint(0,255)]

    # 383 = (255 * 3) / 2
    if sum(backgroundColor[0:len(backgroundColor)]) < 383:
        textColor = "white"
    else:
        textColor = "black"

    backgroundColor = "rgb(" + str(backgroundColor)[1:-1] + ")"

    print("    [+] Using " + backgroundColor + " with " + textColor + " text")

    # Checks for output directory and creates one if needed
    if not os.path.exists("./output"):
        print("[-] Output directory not found. Creating")
        os.makedirs("./output")

    # Save js and css files into output folder
    print("[+] Opening css and js template files")
    with open("./template/css.txt") as f:
        css = f.read().split("[~]")
    with open("./template/js.txt") as f:
        js = f.read()

    # Applies theme to css
    css = css[0] + textColor + css[1] + backgroundColor + css[2] + textColor + css[3]

    # Write to output files
    print("[+] Writing output files in ./output")
    with open("./output/index.html", "w+") as f:
        f.write(html)
    with open("./output/main.css", "w+") as f:
        f.write(css)
    with open("./output/main.js", "w+") as f:
        f.write(js)
    print("[+] Completed")
