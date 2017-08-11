import sys
import fileinput
import os

template = {}

if len(sys.argv) < 2:
    print("Usage: {} [/path/to/file]".format(sys.argv[0]))
else:
    print("[-] Loading templates")
    # Opens template files
    with open("./template/html/html") as f:
        template["html"] = f.read().split("[~]")
        print("    [+] Loaded html template")

    with open("./template/html/slide") as f:
        template["slide"] = f.read().split("[~]")
        print("    [+] Loaded slide template")

    with open("./template/html/heading") as f:
        template["heading"] = f.read().split("[~]")
        print("    [+] Loaded heading template")

    with open("./template/html/contentSection") as f:
        template["contentSection"] = f.read().split("[~]")
        print("    [+] Loaded content section template")

    with open("./template/html/content") as f:
        template["content"] = f.read().split("[~]")
        print("    [+] Loaded content template")

    print("[+] Loaded all templates")

    html = template["html"][0]
    # Check to see if content tag is open
    contentOpen = False
    # Check to see if a title has been added
    slideTitleAdded = False
    slideNum = 0
    # Check for presentation heading has been added
    headingAdded = False

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

        # Removes dashes and extra spaces from start of line
        line = "".join(line)[counter + 1:]

        # Determines what needs to be added to the file
        # Presentation heading. Only one in the presentation
        if counter < 0:
            if not headingAdded:
                print("    [+] Heading")
                html += line + template["html"][1]
                headingAdded = True
            else:
                print("    [!] Warning: Cannot have two headings in the presentation. Moving on")

        if headingAdded:
            # Title of slide. One per slide
            if counter == 0:
                print("    [+] Creating new slide")
                if not slideTitleAdded:
                    html += template["slide"][0] + str(slideNum) + template["slide"][1] + template["heading"][0] + line[1:] + template["heading"][1]
                    slideTitleAdded = True
                    slideNum += 1
                else:
                    if contentOpen:
                        html += template["contentSection"][0]
                        contentOpen = False
                    html += template["slide"][2] + template["slide"][0] + str(slideNum) + template["slide"][1] + template["heading"][0] + line[1:] + template["heading"][1]
                    slideTitleAdded = False
                    slideNum = 0


            # Dot point on slide. Multiple per slide
            elif counter == 1:
                print("    [+] Content")
                if not contentOpen:
                    html += template["contentSection"][0]
                    contentOpen = True
                html += template["content"][0] + line[1:] + template["content"][1]
        else:
            print("    [!] No heading supplied. Using 'Presentation'")
            html += "Presentation" + template["html"][1]
            headingAdded = True

    html += template["contentSection"][1] + template["slide"][2] + template["html"][2]
    print("[+] Successfully parsed input file")

    # Checks for output directory and creates one if needed
    if not os.path.exists("./output"):
        print("[+] Output directory not found. Creating")
        os.makedirs("./output")

    # Write to output file
    print("[-] Writing as 'output.html'")
    with open("./output/output.html", "w+") as f:
        f.write(html)
    print("[+] Completed")
