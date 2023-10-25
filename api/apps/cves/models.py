from django.db import models
import requests


class Downloader:
    def __init__(self) -> None:
        self._prepare_session()

    def _prepare_session(self):
        self._session = requests.session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": "http://www.google.com/"
        })

    @property
    def _base_url(self):
        raise NotImplementedError

    def get_table(self):
        raise NotImplementedError
    
    def _post(self, url, data):
        response = self._session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    
    def _get(self, url):
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()
    
class RedHatDownloader(Downloader):
    @property
    def _base_url(self):
        return 'https://access.redhat.com/api/redhat_node/'

    def _prepare_session(self):
        super()._prepare_session()
        self._session.headers.update({
            'referrer': 'https://access.redhat.com/',
            'origin': 'https://access.redhat.com/',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
        })
    
    def get_table(self, error: str):
        url = f'{self._base_url}{error}.json?lang=en'
        return self._get(url)
    
class RedHatError(models.Model):
    error_code = models.CharField(max_length=1000, unique=True)
    error_json = models.JSONField(null=True, blank=True)
    downloader = RedHatDownloader()
    def __str__(self):
        return self.error_code
    
    def get_error_table(self):
        try:
            error_json =  self.downloader.get_table(self.error_code)
        except requests.exceptions.HTTPError:
            error_json = self.error_json or {}
        else:
            self.error_json = error_json
            self.save(update_fields=['error_json'])
        return_dict = {}
        try:
            for v in error_json['field_cve_releases_txt']['und'][0]['object']:
                return_dict[v['product']] = {
                    'product': v['product'],
                    'state': v['state'],
                }
            return_dict = dict(sorted(return_dict.items(), key=lambda item: item[0]))
        except (KeyError, IndexError):
            values = []
        else:
            values = list(return_dict.values())
        return {
            self.error_code: values
        }