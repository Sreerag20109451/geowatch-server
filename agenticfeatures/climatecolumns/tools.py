from  langchain.tools import tool
from typing import TypedDict, List
import  json
import requests
import xmltodict
import arxiv

semantic_search_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=climate+change&fields=title,abstract,openAccessPdf,authors,publicationDate,citationCount&limit=10&sort=citationCount:desc&publicationDateOrYear=2026-01"


class ResearchDocument(TypedDict):
    title: str
    abstract: str
    doi: str
    authors: List[str]
    link : str


@tool(description="searches research papers for articles")
def searchforpapers() -> List[ResearchDocument]:
    arxiv_client = arxiv.Client()
    researchdocs = []
    search = arxiv.Search(
        query="climate change",
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    try:
        results = arxiv_client.results(search)

        for paper in results:
            author_names = [author.name for author in paper.authors]
            doc_id = paper.doi if paper.doi else paper.entry_id.split('/')[-1]

            researchdocs.append(ResearchDocument(
                title=paper.title,
                abstract=paper.summary,
                doi=doc_id,
                authors=author_names,
                link=paper.pdf_url,
            ))

    except Exception as e:
        print(e.message)

    return researchdocs


