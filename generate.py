import sys
import fileinput
import os
from random import randint

template = {}
customMode = False

if len(sys.argv) < 2:
    print("Usage: {} [/path/to/file]".format(sys.argv[0]))
else:
    # If custom flag set it will leave options for custom changes
    if len(sys.argv) == 3:
        if sys.argv[2] == "-c":
            customMode = True

    print("[+] Loading templates")
    # Opens template files
    with open("./template/html.txt") as f:
        f = f.read()
        template["html"] = f.split("[~html]")[1]
        template["slide"] = f.split("[~slide]")[1]
        template["heading"] = f.split("[~heading]")[1]
        template["contentSection"] = f.split("[~contentSection]")[1]
        template["content"] = f.split("[~content]")[1]

    print("[+] Loaded all templates")

    html = template["html"]

    firstLine = True
    slideOpen = False
    contentOpen = False
    slideCounter = 0

    print("[-] Parsing input file")
    # Parses the input file
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
            # Line type is a heading
            if counter == -1:
                title = line

            # No heading supplied
            else:
                title = "Presentation"

            # Puts the heading in the page
            html = html.replace("[~title]", title)
            firstLine = False

        # Slide title (automatically makes new slide)
        if counter == 0:
            if slideOpen:
                if contentOpen:

                    # Close content section
                    slideContent += template["contentSection"].replace("[~contentSectionContent]", contentSectionContent + "[~contentSectionContent]")
                    contentOpen = False

                # Close slide
                slide = template["slide"].replace("[~slideContent]", slideContent).replace("[~slideId]", str(slideCounter - 1)) + "[~slideSection]"
                html = html.replace("[~slideSection]", slide)
                slideOpen = False

            # Create title and slide
            heading = template["heading"].replace("[~headingContent]", line)
            slideContent = heading + "[~slideContent]"
            slideOpen = True
            slideCounter += 1

        # Content type
        elif counter == 1:
            if not contentOpen:

                # Create new content section
                contentSectionContent = template["contentSection"]
                contentOpen = True

            # Add line to content section
            contentSectionContent = template["content"].replace("[~contentContent]", line + "[~contentContent]")

    # Get rid of placeholders
    html = html.replace("[~slideContent]", "").replace("[~contentSectionContent]", "").replace("[~contentSection]", "").replace("[~contentContent]", "").replace("[~slideSection]", "").replace("[~slideCounter]", str(slideCounter - 2))

    print("[+] Successfully parsed input file")

    # Checks for output directory and creates one if needed
    if not os.path.exists("./output"):
        print("[+] Output directory not found. Creating")
        os.makedirs("./output")

    # Write to output file
    print("[+] Writing as './output/output.html'")
    with open("./output/output.html", "w+") as f:
        f.write(html)

    # Save js and css files into output folder
    print("[+] Opening css and js template files")
    with open("./template/css.txt") as f:
        css = f.read().split("[~]")
    with open("./template/js.txt") as f:
        js = f.read()

    print("[+] Generating theme")
    # Makes a rgb color
    randomColor = [randint(0,255), randint(0,255), randint(0,255)]
    # 383 = (255 * 3) / 2
    if sum(randomColor[0:len(randomColor)]) < 383:
        textColor = "white"
    else:
        textColor = "black"
    randomColor = "rgb(" + str(randomColor)[1:-1] + ")"
    print("    [+] Using " + randomColor + " with " + textColor + " text")
    css = css[0] + textColor + css[1] + randomColor + css[2] + textColor + css[3]

    print("[+] Writing css and js files")
    with open("./output/main.css", "w+") as f:
        f.write(css)
    with open("./output/main.js", "w+") as f:
        f.write(js)
    print("[+] Completed")

    if customMode:
        print("Custom")
