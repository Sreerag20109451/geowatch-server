from  langchain.tools import tool
from typing import TypedDict, List
import  json
import requests

semantic_search_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=climate+change&fields=title,abstract,openAccessPdf,authors,publicationDate,citationCount&limit=10&sort=citationCount:desc&publicationDateOrYear=2026-01"

class ResearchDocument(TypedDict):
    title: str
    abstract: str
    doi: str
    authors: List[str]


@tool
def searchforpapers() -> List[ResearchDocument]:

    researchdocs = []
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # Define your parameters clearly
    params = {
        "query": "climate change",
        "fields": "title,abstract,openAccessPdf,externalIds,authors,publicationDate,citationCount,externalIds",
        "limit": 10,
        "sort": "citationCount:desc",
        "publicationDateOrYear": "2025-2026"
    }

    try:
        response = requests.get(url, params=params).json()

        if response.status_code == 200:
            for paper in response["results"]:
                researchdocs.append(ResearchDocument(authors=paper["authors"],
                                                     title=paper["title"],
                                                     abstract=paper["abstract"],
                                                     doi=paper["externalIds"][0]["externalId"]))
        else:
            raise Exception("Error getting research documents")
    except Exception as e:
        print(e.message)

    return researchdocs


