# Load python packages
from bs4 import BeautifulSoup
from pathlib import Path
from tabulate import tabulate
import json

# Create html file
def create_html():
    # Read json data
    json_path = Path.cwd() / 'data.json'
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Read template html
    html_path = Path.cwd() / 'template.html'
    with open(html_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Create tables for all tabs
    div_list = soup.find_all('div', {'class': 'overflow-auto'})
    for div in div_list:
        div_id = div.parent['id']
        table = create_table(data[div_id])
        div.append(table)

    # Add attributes to table elements
    for table in soup.find_all('table'):
        table['class'] = 'table table-bordered table-hover'

    for thead in soup.find_all('thead'):
        thead['class'] = 'table-dark'

    for th in soup.find_all('th'):
        th['scope'] = 'col'
        th['class'] = 'align-middle'

    # Export to html file
    output_path = Path.cwd() / 'index.html'
    with open(output_path, 'w') as file:
        html = soup.prettify()
        file.write(html)

# Create <table> tag element
def create_table(array):
    table = []
    for item in array:
        row = [
            item['No'],
            create_link(item['Exercise'], item['Link']),
            create_img(item['Image'], item['Link']),
            item['Body Part']
        ]
        table.append(row)
    headers = ['No', 'Exercise', 'Diagram', 'Body Part']
    html = tabulate(table, headers, tablefmt='unsafehtml', disable_numparse=True)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Create <a> tag element
def create_link(name, url):
    soup = BeautifulSoup(features='html.parser')
    a = soup.new_tag('a')
    a.string = name
    a['href'] = url
    return str(a)

# Create <img> tag element
def create_img(src, url):
    soup = BeautifulSoup(features='html.parser')
    img = soup.new_tag('img')
    img['src'] = src
    img['alt'] = url.split('/')[-1]
    return str(img)

# Run main program
if __name__ == '__main__':
    create_html()