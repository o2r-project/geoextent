# Import libraries
import requests


def get_number_of_records(parameters):
    """
    :param parameters: Dictionary with parameters of query to Zenodo API (dict)
    :return: Number of records retrieved from the query (int)
    """
    response_hits = requests.get('https://zenodo.org/api/records/', params=parameters)
    hits = response_hits.json()['hits']['total']
    return hits


def get_info_records(parameters):
    """
    :param parameters: Dictionary with parameters of query to Zenodo API (dict)
    :return: Dictionary with metadata of records resulting from query to Zenodo API (dict)
    """
    hits = get_number_of_records(parameters)

    if hits >= 10000:
        print("Maximum number of records exceeded.")
        hits = 10000
    zenodo_search = {}
    if hits > 0:
        parameters["size"] = str(hits)
        response = requests.get('https://zenodo.org/api/records/',
                                params=parameters)
        content = response.json()

        for i in range(0, hits):
            files = content['hits']['hits'][i]['files']
            size = round(sum(f['size'] for f in files) / 2 ** 20, 1)
            record_id = content['hits']['hits'][i]['conceptrecid']
            doi = content['hits']['hits'][i]['doi']
            title = content['hits']['hits'][i]['metadata']['title']
            license = content['hits']['hits'][i]['metadata']['license']['id']

            try:
                location = content['hits']['hits'][i]['metadata']['location']
            except:
                location = None
            zenodo_search[record_id] = {"doi": doi, "title": title, "license": license, "size_mb": size}
        return zenodo_search
