from requests import request
from requests import HTTPError
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, host: str, document: dict):
        self.host = host
        self.document = document

    def parse_ed(self, soup: BeautifulSoup, field, value=None):
        result = {}
        if isinstance(value, list):
            for t in value:
                fr = soup.find_all(itemprop=t)
                if len(fr) == 0:
                    result[t] = None
                elif len(fr) == 1:
                    result[t] = fr[0].text.strip()
                else:
                    result[t] = [f.text.strip() for f in fr]
        elif isinstance(value, dict):
            fr = soup.find_all(attrs={'itemprop': field})
            result = []
            for f in fr:
                result.append({k: self.parse_ed(f, k, v) for k, v in value.items()})
        elif value is None:
            fr = soup.find_all(itemprop=field)
            if len(fr) == 0:
                result = None
            elif len(fr) == 1:
                result = fr[0].text.strip()
            else:
                result = [f.text.strip() for f in fr]
        else:
            return None
        return result

    def parse(self, url: str, extract_fields) -> dict or None:
        r = request('get', f'{self.host}{url}')
        if r.status_code != 200:
            raise HTTPError()
        soup = BeautifulSoup(r.content.decode(), 'html.parser')
        extracted_data = {ef: self.parse_ed(soup, ef, ev) for ef, ev in extract_fields.items()}
        urls = soup.find_all('a', itemprop='addRef')
        if len(urls) > 0 and extracted_data is not None:
            for url in urls:
                u = str(url['href']).replace(self.host, '').replace('http://sbmpei.ru', '')
                extracted_data[u] = self.parse(u, extract_fields)
        return extracted_data

    def get_data(self):
        return {
            k: self.parse(k, v) for k, v in self.document.items()
        }
