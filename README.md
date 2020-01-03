# arxiv-crawler
Crawl [arXiv](http://arxiv.org/) papers' Title & Abstract info and written into a CSV file

### Modifying crawling parameters
Please visit https://arxiv.org/search/advanced to figure out all possible params
```python
# crawler.py
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
```

### Launch the crawler

```sh
$ python crawler.py
Fetching 1/20...
https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=drone&terms-0-field=all&terms-1-operator=OR&terms-1-term=uav&terms-1-field=all&terms-2-operator=OR&terms-2-term=%22remote%20sensing%22&terms-2-field=all&terms-3-operator=OR&terms-3-term=remote-sensing&terms-3-field=all&classification-computer_science=y&classification-include_cross_list=include&date-year=&date-filter_by=date_range&&abstracts=show&date-from_date=2000&date-to_date=2020&date-date_type=submitted_date&order=submitted_date&size=50&start=0
Retrieved paper = 1
Retrieved paper = 2
Retrieved paper = 3
...
```

### Results
A csv file named `ArXiv.csv` will be created in the same location of the crawlers/caller

## Future work
Figure out to extract Keywords from Title & Abstract
