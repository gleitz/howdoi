import xml.etree.ElementTree as ET
from urllib.parse import urlencode
import requests


ROOT_URL = 'http://export.arxiv.org/api/'

NAMESPACES = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom',
}


def query_page(search_query, start=0, max_results=1):
    url_args = {"search_query": search_query,
                "start": start,
                "max_results": max_results,
                "sortBy": "relevance"}
    response = requests.get(ROOT_URL + 'query?' + urlencode(url_args))
    response.raise_for_status()
    return parse(response.text)


def parse(response):
    root = ET.fromstring(response)
    for entry in root.findall("atom:entry", NS):
        # If there are no results, arXiv sometimes returns just a blank entry
        if entry.find("atom:id", NS) is None:
            continue
        return convert_entry_to_paper(entry)


def convert_entry_to_paper(entry):
    paper_details = {}
    paper_details['arxiv_id'] = entry.find("atom:id", NS).text.split('/')[-1]
    paper_details['title'] = entry.find("atom:title", NS).text
    paper_details['title'] = paper_details['title'].replace('\n', '').replace('  ', ' ')
    paper_details['summary'] = entry.find('atom:summary', NS).text
    paper_details['authors'] = []
    for author in entry.findall('atom:author', NS):
        paper_details['authors'].append({
            'name': author.find('atom:name', NS).text,
            'affiliation': [e.text for e in author.findall('arxiv:affiliation', NS)],
        })
    paper_details['arxiv_url'] = entry.find(
        "./atom:link[@type='text/html']", NS).attrib['href']
    paper_details['pdf_url'] = entry.find(
        "./atom:link[@type='application/pdf']", NS).attrib['href']
    paper_details['primary_category'] = entry.find(
        'arxiv:primary_category', NS).attrib['term']
    paper_details['categories'] = [e.attrib['term'] for e in entry.findall('atom:category', NS)]
    # Optional
    paper_details['comment'] = getattr(entry.find('arxiv:comment', NS), 'text', None)
    paper_details['doi'] = getattr(entry.find('arxiv:doi', NS), 'text', None)
    paper_details['journal_ref'] = getattr(entry.find('arxiv:journal_ref', NS), 'text', None)  
    return paper_details
