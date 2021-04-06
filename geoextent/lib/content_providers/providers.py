from requests import Session, HTTPError
from geoextent.lib import helpfunctions as hf
import logging


class ContentProvider:
    def __init__(self):
        self.log = logging.getLogger("geoextent")


class DoiProvider(ContentProvider):

    def __init__(self):
        self.session = Session()

    def _request(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def _type_of_reference(self):
        if hf.doi_regexp.match(self.reference):
            return "DOI"
        elif hf.https_regexp.match(self.reference):
            return 'Link'

    @property
    def get_url(self):

        if self._type_of_reference() == "DOI":
            doi = hf.doi_regexp.match(self.reference).group(2)

            try:
                resp = self._request("https://doi.org/{}".format(doi))
                resp.raise_for_status()

            except HTTPError:
                return doi

            return resp.url

        else:
            return self.reference
