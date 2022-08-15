# Load python packages
from alive_progress import alive_it, config_handler
from bs4 import BeautifulSoup
from docx import Document
from pathlib import Path
from tabulate import tabulate
import json
import multiprocessing as mp
import pandas as pd
import re
import requests

# Define user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
 
config_handler.set_global(
    length=75,
    spinner='classic',
    bar='classic2',
    force_tty=True,
    dual_line=True
)

def create_json():
    image_path = Path.cwd() / 'image'
    if not image_path.is_dir():
        image_path.mkdir()

    file_path = Path.cwd() / 'workout.docx'
    document = Document(file_path)

    paragraphs = document.paragraphs
    titles = [x.text for x in paragraphs if x.text.strip()]

    tables = document.tables
    keys = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6']

    data = {}
    for index, table in enumerate(tables):
        title = titles[index]
        print(title)

        df = create_df(table)
        df['Image'] = get_images(df)

        key = keys[index]
        data[key] = df.to_dict('records')

    json_path = Path.cwd() / 'data.json'
    with open(json_path, 'w') as file:
        json.dump(data, file)

def create_df(table):
    num_row = len(table.rows)
    num_col = len(table.rows[0].cells)
    for i in range(num_row):
        row = table.rows[i]
        if i == 0:
            header = [x.text.strip() for x in row.cells]
            data = {x:[] for x in header}
        else:
            for j in range(num_col):
                key = header[j]
                item = row.cells[j].text.strip()
                data[key].append(item)
    df = pd.DataFrame(data)
    return df

def get_images(df):
    links = list(df['Link'])
    processes = mp.cpu_count() - 1
    with mp.Pool(processes) as pool:
        results = alive_it(
            pool.imap(get_image, links),
            len(links)
        )
        images = []
        for index, result in enumerate(results):
            results.text(f'Download: {links[index]}')
            images.append(result)
        return images

def get_image(url):
    filename = url.split('/')[-2] + '.svg'
    url = get_link(url)
    headers = {
        'User-Agent': USER_AGENT
    }
    response = requests.get(url, headers=headers)
    image = response.content
    image_path = Path('image') / filename
    with open(image_path, 'wb') as file:
        file.write(image)
    return image_path.as_posix()

def get_link(url):
    headers = {
        'User-Agent': USER_AGENT
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('img', {'class': 'exImg'})['data-url_male']
    return link

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
            create_img(item['Image']),
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
def create_img(url):
    soup = BeautifulSoup(features='html.parser')
    img = soup.new_tag('img')
    img['src'] = url
    img['alt'] = url.split('/')[-1]
    return str(img)

# Run main program
if __name__ == '__main__':
    create_json()
    create_html()