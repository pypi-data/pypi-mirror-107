import requests


def get_deposits(country='all', deposit_type='all'):
    """
    Fetch petroleum deposits data from public database. Source: PRIO

    Arguments
        country: 'all' or specific country (e.g. 'Norway')
        deposit_type: 'all' or specific type (e.g. 'oil', 'gas', 'oil and gas')

    Returns
        dataset as list of dicts. with 'name', 'country', 'lat', 'long', 'type', 'source', 'info'.
    """

    url = 'https://raw.githubusercontent.com/pro-well-plan/petrodc/develop/data/deposits.json'
    dataset = requests.get(url).json()

    data = []
    for item in dataset:
        include = True
        if country != 'all' and item['country'] != country:
            include = False
        if deposit_type != 'all' and item['type'] != deposit_type:
            include = False
        if include:
            data.append(item)

    return data
