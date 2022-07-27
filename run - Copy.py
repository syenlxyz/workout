from bs4 import BeautifulSoup
from pathlib import Path
from tabulate import tabulate
import json

def create_html():
    json_path = Path.cwd() / 'data.json'
    with open(json_path, 'r') as file:
        data = json.load(file)

    html_path = Path.cwd() / 'template.html'
    with open(html_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    div_list = soup.find_all('div', {'class': 'overflow-auto'})
    for div in div_list:
        div_id = div.parent['id']
        table = create_table(data[div_id])
        div.append(table)

    for table in soup.find_all('table'):
        table['class'] = 'table table-bordered table-hover'

    for thead in soup.find_all('thead'):
        thead['class'] = 'table-dark'

    for th in soup.find_all('th'):
        th['scope'] = 'col'

    output_path = Path.cwd() / 'index.html'
    with open(output_path, 'w') as file:
        html = soup.prettify()
        file.write(html)

def create_table(array):
    table = []
    for item in array:
        row = [
            item['no'],
            create_link(item['exercise'], item['youtube']),
            create_img(item['image']),
            item['part'],
            item['sets'],
            item['reps']
        ]
        table.append(row)
    headers = ['No', 'Exercise', 'Diagram', 'Body Part', 'Sets', 'Reps']
    html = tabulate(table, headers, tablefmt='unsafehtml', disable_numparse=True)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def create_link(name, url):
    soup = BeautifulSoup(features='lxml')
    a = soup.new_tag('a')
    a.string = name
    a['href'] = url
    return str(a)

def create_img(url):
    soup = BeautifulSoup(features='lxml')
    img = soup.new_tag('img')
    img['src'] = url
    img['alt'] = url.split('/')[-1]
    return str(img)

if __name__ == '__main__':
    create_html()