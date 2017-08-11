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
                print("    [+] Adding heading to presentation")
                html += line + template["html"][1]

            # No heading supplied
            else:
                print("    [+] Adding default heading to presentation")
                html += "Presentation" + template["html"][1]
            firstLine = False

        # Slide title (automatically makes new slide)
        if counter == 0:
            print("    [+] Creating title and slide")
            if slideOpen:
                if contentOpen:

                    # Close content section
                    print("        [+] Closing content section")
                    html += template["contentSection"][1]
                    contentOpen = False

                # Close slide
                print("        [+] Closing slide")
                html += template["slide"][2]
                slideOpen = False

            # Create title and slide
            slideTitle = template["heading"][0] + line + template["heading"][1]
            html += template["slide"][0] + str(slideCounter) + template["slide"][1] + slideTitle
            slideOpen = True
            slideCounter += 1
            print("    [+] Created new slide")

        # Content type
        elif counter == 1:
            print("    [+] Creating new content section")
            if not contentOpen:

                # Create new content section
                print("        [+] Closing content section")
                html += template["contentSection"][0]
                contentOpen = True

            # Add line to content section
            html += template["content"][0] + line + template["content"][1]
            print("    [+] Created new content section")

    print("    [+] Running final checks on tags")
    # Checks to run before closing final tags
    if contentOpen:
        # Close content
        print("        [+] Closing content section")
        html += template["contentSection"][1]
        contentOpen = False
    if slideOpen:
        # Close slide
        print("        [+] Closing slide")
        html += template["slide"][2]
        slideOpen = False
    
    # Close final tags
    html += template["html"][2] + str(slideCounter - 1) + template["html"][3]
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
