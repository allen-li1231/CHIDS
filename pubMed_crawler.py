"""
@Author: Allen Li       10/31/2019
"""
import time
from warnings import warn
import requests
from bs4 import BeautifulSoup as soup
import re
from pandas import DataFrame, concat

session = requests.Session()
URL = "https://www.ncbi.nlm.nih.gov/pubmed"


def post_form(keyword: str, page, page_count, per_page) -> dict:
    start_count = (page-2) * per_page + 1 if page >= 2 else 1
    form = {'term': keyword,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_PageController.PreviousPageName': 'results',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_PageController.SpecialPageName': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_Facets.FacetsUrlFrag': 'filters%3D',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_Facets.FacetSubmitted': 'false',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_Facets.BMFacets': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sSort': 'none',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPageSize': per_page,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FSort': '',
            'email_format': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.email_sort': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.email_count': per_page,
            'email_start': start_count,
            'email_address': '',
            'email_subj': 'NLP+-+PubMed',
            'email_add_text': '',
            'EmailCheck1': '',
            'EmailCheck2': '',
            'coll_start': start_count,
            'BibliographyUser': '',
            'BibliographyUserName': 'my',
            'citman_count': per_page,
            'citman_start': start_count,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileFormat': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPresentation': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize': per_page,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPageSize': per_page,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Sort': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastSort': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileSort': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Format': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastFormat': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PrevPageSize': per_page,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PrevPresentation': 'docsum',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PrevSort': '',
            'CollectionStartIndex': '1',
            'CitationManagerStartIndex': '1',
            'CitationManagerCustomRange': 'false',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_ResultsController.ResultCount': page_count,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_ResultsController.RunLastQuery': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.cPage': [page-1,
                                                                                    page],
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.CurrPage': page,
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailReport': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailFormat': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailCount': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailStart': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailSort': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.Email': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailSubject': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailText': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailQueryKey': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailHID':
                '1BGTOZiBdTRS-qr2f6bquDSBTpfZ8-qRibtG6muQWM2qLAQWOY1YNdx5rewklFTwIYWs8p9bwmno7fYtMEZEVMRKFIAmXqqEqn',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.QueryDescription': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.Key': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.Answer': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.Holding': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.HoldingFft': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.HoldingNdiSet': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.OToolValue': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.SubjectList': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.TimelineAdPlaceHolder.CurrTimelineYear': '',
            'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.TimelineAdPlaceHolder.BlobID': 'NCID_1_196696433_130.14.\
22.33_9001_1572555196_1146902011_0MetA0_S_MegaStore_F_1',
            'EntrezSystem2.PEntrez.DbConnector.Db': 'pubmed',
            'EntrezSystem2.PEntrez.DbConnector.LastDb': 'pubmed',
            'EntrezSystem2.PEntrez.DbConnector.Term': keyword,
            'EntrezSystem2.PEntrez.DbConnector.LastTabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': '1',
            'EntrezSystem2.PEntrez.DbConnector.IdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkReadableName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkSrcDb': '',
            'EntrezSystem2.PEntrez.DbConnector.Cmd': 'PageChanged',
            'EntrezSystem2.PEntrez.DbConnector.TabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.QueryKey': ''
            }
    return form


# parse form from str to dict
def form_parser(form_body: str) -> dict:
    d = dict()
    for x in form_body.split('&'):
        k, sep, v = x.partition('=')
        if sep != '=':
            raise ValueError('malformed query')

        k = k.split('%')[0]
        if k in d:
            if isinstance(d[k], list):
                d[k].append(v)
            else:
                d[k] = [d[k], v]
        else:
            d[k] = v
    return d


def get_html_context(URL: str, request_type: str, retry=3, **kwargs) -> soup:
    if request_type == "get":
        while retry:
            try:
                s = session.get(URL, **kwargs)
            except:
                retry -= 1
            else:
                html_context = soup(s.content, "lxml")
                return html_context

    elif request_type == "post":
        while retry:
            try:
                s = session.post(URL, **kwargs)
            except:
                retry -= 1
            else:
                html_context = soup(s.content, "lxml")
                return html_context
    else:
        warn("Unsupported http method")


def get_page_count(html_context: soup) -> int:
    page_count = html_context.find("input", attrs={"class": "num"})
    page_count = page_count.attrs['last']
    try:
        return int(page_count)
    except ValueError:
        warn("Page count is not a number")
    except TypeError:
        warn("Wrong type of page count")
    return -1


def get_date_of_publish(html_context: soup) -> DataFrame:
    date_container = html_context.find_all("p", attrs={"class": "details"})
    raw_date_text = [d.text for d in date_container]

    date_of_publish = []
    for raw in raw_date_text:
        date = re.findall(r"(\d{4}) ?(\w{0,3})", raw)
        if len(date) == 0:
            date_of_publish.append(('', ''))
        else:
            date_of_publish.append(date[0])

    return DataFrame(date_of_publish, columns=['Year', "Month"])


def get_title_abstract(html_context: soup) -> DataFrame:
    paragraph = html_context.find_all("p", attrs={'class': "title"})
    relative_link = [p.a.attrs["href"] for p in paragraph]
    absolute_link = [URL.rstrip("/pumbed") + link for link in relative_link]

    container = []
    title_rule = lambda x: x.name == "h1" and not x.has_attr("class")
    for link in absolute_link:
        html_context = get_html_context(link, "get")
        title = html_context.find(title_rule)
        abstract = html_context.find("div", attrs={"class": "abstr"})
        data = (title.text, '' if abstract is None else abstract.text.lstrip("Abstract"))
        container.append(data)
        time.sleep(0.1)

    return DataFrame(container, columns=['Title', 'Abstract'])


def page_search(functions, html_context):
    if isinstance(html_context, str):
        html_context = soup(html_context, 'lxml')
    container = [func(html_context) for func in functions]
    return concat(container, axis=1)


def full_search(keyword, functions, per_page=200) -> DataFrame:
    get_html_context(URL, "get", params={"term": keyword})

    html_container = []
    page_count = 1
    i = 1
    print("Preparing...")
    while i <= page_count:
        form = post_form(keyword, i, page_count, per_page)
        html_context = get_html_context(URL, "post", data=form)
        if i == 1:
            page_count = html_context.find("input", attrs={"class": "num"})
            page_count = int(page_count.attrs["last"])

        html_container.append(html_context)
        i += 1

    data_container = []
    for i, html_context in enumerate(html_container):
        print("Going for page %d/%d" % (i+1, page_count))
        data = page_search(functions, html_context)
        data_container.append(data)

    return concat(data_container, axis=0, ignore_index=True)


def test_html(html_context):
    with open(r"C:\Users\super\Desktop\test.html", 'w', encoding="utf-8") as f:
        f.write(str(html_context))
        f.close()
