import xml.etree.ElementTree as ET
from urllib.parse import urlencode
import requests

# The goal of the API is to allow application developers
# access to all of the arXiv data, search and linking facilities
# with an easy-to-use programmatic interface.
# User's Manual and Terms of Use at https://arxiv.org/help/api
ROOT_URL = "http://export.arxiv.org/api/"

NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def _query_page(search_query, start=0, max_results=1):
    url_args = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": "relevance",
    }
    response = requests.get(ROOT_URL + "query?" + urlencode(url_args))
    response.raise_for_status()
    return _parse(response.text)


def _parse(response):
    root = ET.fromstring(response)
    for entry in root.findall("atom:entry", NAMESPACES):
        # If there are no results, arXiv sometimes returns just a blank entry
        if entry.find("atom:id", NAMESPACES) is None:
            continue
        return _convert_entry_to_paper(entry)


def _get_authors(entry):
    authors = []
    for author in entry.findall("atom:author", NAMESPACES):
        authors.append(
            {
                "name": author.find("atom:name", NAMESPACES).text,
                "affiliation": [
                    e.text for e in author.findall("arxiv:affiliation", NAMESPACES)
                ],
            }
        )
    return authors


def _convert_entry_to_paper(entry):
    paper = {}
    paper["arxiv_id"] = entry.find("atom:id", NAMESPACES).text.split("/")[-1]
    paper["title"] = entry.find("atom:title", NAMESPACES).text
    paper["title"] = paper["title"].replace("\n", "").replace("  ", " ")
    paper["summary"] = entry.find("atom:summary", NAMESPACES).text
    paper["authors"] = _get_authors(entry)
    paper["arxiv_url"] = entry.find("./atom:link[@type='text/html']", NAMESPACES).attrib["href"]
    paper["pdf_url"] = entry.find("./atom:link[@type='application/pdf']", NAMESPACES).attrib["href"]
    paper["primary_category"] = entry.find("arxiv:primary_category", NAMESPACES).attrib["term"]
    paper["categories"] = [e.attrib["term"] for e in entry.findall("atom:category", NAMESPACES)]
    paper["comment"] = getattr(entry.find("arxiv:comment", NAMESPACES), "text", None)
    paper["doi"] = getattr(entry.find("arxiv:doi", NAMESPACES), "text", None)
    paper["journal_ref"] = getattr(entry.find("arxiv:journal_ref", NAMESPACES), "text", None)
    return paper
