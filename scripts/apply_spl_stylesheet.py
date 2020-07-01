#!./_python-env/bin/python

import os
import sys
import lxml.etree as etree
from bs4 import BeautifulSoup

root_dir = './data/spl/dailymed/flatten'

# TODO: Automatically download this file
xsl_path = './data/spl/stylesheet/spl_stylesheet_6_2/spl.xsl'

def transform_xml(xml_path, xsl_path=xsl_path):
    if not os.path.isfile(xml_path):
        print(xml_path + ' not found')
        return

    prefix = os.path.splitext(xml_path)[0]
    output_file = prefix + '.html'

    if os.path.isfile(output_file):
        # print(output_file + ' already exists')
        return output_file

    print('transforming ' + output_file)
    try:
        dom = etree.parse(xml_path)
        xslt = etree.parse(xsl_path)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)

        with open(output_file, 'w') as f:
            f.write(str(newdom))

        return output_file
    except:
        print("Unexpected error:", sys.exc_info()[0])


def html2text(html_path):
    if not os.path.isfile(html_path):
        # print(html_path + ' not found')
        return

    prefix = os.path.splitext(html_path)[0]
    output_file = prefix + '.txt'

    if os.path.isfile(output_file):
        # print(output_file + ' already exists')
        return output_file

    with open(html_path, 'r') as f:
        html = BeautifulSoup(f, 'lxml')

        # kill all script and style elements
        # for script in html(["script", "style"]):
        # script.extract()

        with open(output_file, 'w') as f:
            # f.write(html.body.get_text(separator='\n', strip=True))
            f.write(html.get_text())

        return output_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        quit("incorrect number of arguments")

    target_dir = os.path.join(root_dir, sys.argv[1])
    print("Applying stylesheet to XML in directory: " + target_dir)

    for f in os.listdir(target_dir):
        if f.endswith('.xml'):
            html = transform_xml(os.path.join(target_dir, f))
            if not html:
                print('failure in ' + target_dir)
                continue

            # html2text(html)

quit("done")

label_dirs = os.listdir(root_dir)
l = len(label_dirs)

i = 0
for d in label_dirs:
    d = os.path.join(root_dir, d)

    for f in os.listdir(os.path.join(root_dir, d)):
        if f.endswith('.xml'):
            html = transform_xml(os.path.join(d, f))
            if not html:
                print('failure in ' + d)
                continue

            html2text(html)

    if i % 100 == 0:
        print(str(i / l * 100)[:4] + '% completed')

    i = i+1
