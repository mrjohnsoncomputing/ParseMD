import time, random, threading


class ParseMD:
    DELIMITER = "\n"
    indent = 4

    def __init__(self):
        self.title = "test parse"  # input("What is the title of your document?")
        self.output_filename = "test_output.html"  # input("Enter html output filename")
        self.input_filename = "test_data.md"  # input("Enter markdown filename")

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as file:
            data = file.read()
        return data

    @staticmethod
    def write_file(filename, data, mode="a"):
        with open(filename, mode) as file:
            file.write(data)

    @staticmethod
    def parse_line(line):
        print(line)

    @staticmethod
    def check_file_exists(filename):
        try:
            with open(filename, 'r') as file:
                file.read()
            print("Overwriting existing file {}".format(filename))
        except FileNotFoundError:
            print("Creating new file: {}".format(filename))
        finally:
            with open(filename, 'w') as file:
                file.write("")

    @staticmethod
    def check_heading_level(arr, i):
        level = 0

        while arr[i] == '#':
            level += 1
            i += 1
        return level

    def parse(self):
        md = self.read_file(self.input_filename)
        while len(md) > 0:

            start = 0
            line = ""

            if md[start] == '#':
                level = self.check_heading_level(md, start)

                if level < 7:
                    line = self.build_line(md, start, "h"+str(level))
                else:
                    # Heading 7 doesn't exist, need to handle this as paragraph text.
                    print("Heading 7 doesn't exist")

            elif md[start:start+2] == '* ':
                line = self.build_list(md)

            else:
                line = self.build_line(md, start, "p")

            md = md.replace(line, "", 1)

    def add_html_wrapper(self):
        start = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{}</title>\n</head>\n<body>\n'.format(self.title)
        end = '\n</body>\n</html>'
        body = self.read_file(self.output_filename)
        body = start + body + end
        self.write_file(self.output_filename, body, 'w')
        print("{} successfully parsed from MD into HTML".format(self.title))

    def build_list(self, markdown):
        bullets = []
        time.sleep(1)

        while markdown[0:2] == '* ':
            line_break = markdown.index("\n")+1
            line = markdown[0: line_break]
            bullets.append(line)
            markdown = markdown.replace(line, "")

        content = Conversions.ul(bullets, self.indent)
        self.write_file(self.output_filename, content)
        return "".join(bullets)

    def build_line(self, markdown, end, element):
        raw_line = ""

        while end < len(markdown) and markdown[end] != "\n":
            raw_line += markdown[end]
            end += 1

        #print(raw_line)
        #time.sleep(1)

        if raw_line == "":
            return "\n"
        else:
            line = raw_line.strip()

            if element[0] == "h":
                content = self.indent * " " + Conversions.heading(line.replace("#", "", int(element[1])).strip(), element[1])

            elif element == "p":
                content = self.indent * " " + Conversions.p(line)

            else:
                print("Unrecognised Element")

            self.write_file(self.output_filename, content)

            try:
                if markdown[end] == "\n":
                    return raw_line + "\n"
            except IndexError:
                return raw_line

    def run(self):
        self.check_file_exists(self.output_filename)
        self.parse()
        self.add_html_wrapper()


class Conversions:

    @staticmethod
    def heading(text, level):
        html = "<h{} class='' id=''>{}</h{}>\n\n".format(level, text, level)
        return html

    @staticmethod
    def ul(bullets, indent):
        indent = indent * " "
        ul = indent + "<ul>\n"
        for li in bullets:
            li = li.replace("\n", "")
            li = li.replace("* ", "")
            ul += indent * 2 + "<li>{}</li>\n".format(li)
        ul += indent + "</ul>\n\n"
        return ul

    @staticmethod
    def p(text):
        html = "<p>"+text+"</p>\n\n"
        return html


parse_md = ParseMD()
parse_md.run()


