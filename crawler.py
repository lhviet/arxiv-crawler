import csv
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

"""
Modify the below params to crawl the data we want
"""
# ex url = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=drone&terms-0-field=all&terms-1-operator=OR&terms-1-term=%22remote+sensing%22&terms-1-field=all&terms-2-operator=OR&terms-2-term=uav&terms-2-field=all&terms-3-operator=OR&terms-3-term=remote-sensing&terms-3-field=all&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2000&date-to_date=2020&date-date_type=submitted_date&abstracts=show&size=50&order=submitted_date'
base_url = 'https://arxiv.org/search/advanced?advanced='
fixed_params = 'classification-include_cross_list=include&date-year=&date-filter_by=date_range&&abstracts=show'

# Keywords used to search papers, using OR (not AND) operator
terms = ['drone', 'uav', '"remote sensing"', 'remote-sensing']
# Search in all fields: title, abstract, DOI...
term_field = 'all'

# Search in Computer Science class only
classification = 'classification-computer_science=y'

# Filter the query in range of years 2000.01.01 - 2020.12.31
date_type = 'submitted_date'
year_from = 2000
year_to = 2020

# With 100 articles in one page (URL), the current search will return 20 pages (under 2000 articles)
page_size = 100
crawling_pages = 20

"""
Start building the advanced search URLs for ArXiv
"""
query_param = ''
for idx, term in enumerate(terms):
  operator = 'AND' if idx == 0 else 'OR'
  term_idx = f'terms-{idx}'
  query_param = \
    f'{query_param}&' \
    f'{term_idx}-operator={operator}&' \
    f'{term_idx}-term={urllib.parse.quote(term)}&' \
    f'{term_idx}-field={term_field}'

# Structure the query URL
query_url = \
  f'{base_url}' \
  f'{query_param}&' \
  f'{classification}&' \
  f'{fixed_params}&' \
  f'date-from_date={year_from}&date-to_date={year_to}&' \
  f'date-date_type={date_type}&' \
  f'order={date_type}&' \
  f'size={page_size}'

# Structure the list of URLs that we will crawl for data
urls = [
  f'{query_url}&' \
  f'start={page * page_size}' for page in range(crawling_pages)
]
total_url = len(urls)

"""
Start crawling data in URLs
"""
author_separator = ','

# Lambda function to retrieve a plain Text from HTML element
cleanText = lambda text: text.replace('\\n', '').strip()

with open('ArXiv.csv', 'w') as file:
  writer = csv.writer(file)
  writer.writerow(['#', 'Title', 'Authors', 'Abstract', 'Announced', 'URL', 'DOI'])

  count_result = 0

  for idx, url in enumerate(urls):
    print(f'Fetching {(idx + 1)}/{total_url}...\n{url}')
    data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(str(data), 'html.parser')

    results = soup.findAll('li', {'class': 'arxiv-result'})

    for res in results:
      title = cleanText(res.find('p', {'class': 'title'}).text)

      abstract = res.find('span', {'class': 'abstract-full'})
      # Remove the element a-href from the abstract span
      abstract_tail = abstract.find('a')
      abstract_tail.extract()
      # Now get the plain text inside of the abstract span
      abstract = cleanText(abstract.text)

      arxiv_url = res.find('p', {'class': 'list-title'}).find('a').get('href')
      announced = cleanText(res.find('span', {}, True, 'originally announced').next_sibling)

      authors = [a.text for a in res.find('p', {'class': 'authors'}).findAll('a')]
      author_str = author_separator.join(authors)

      # Retrieve DOI; some articles have DOI, some do not
      doi_url = res.find('div', {'class': 'tags has-addons'})
      doi_url = '' if doi_url is None else doi_url.find('a').get('href')

      count_result += 1

      print(f'Retrieved paper = {count_result}')
      # print(title)
      # print(author_str)
      # print(abstract)
      # print(announced)
      # print(arxiv_url)
      # print(doi_url)
      # print('===========')

      # Finally, write the record into a CSV
      writer.writerow([count_result, title, author_str, abstract, announced, arxiv_url, doi_url])
