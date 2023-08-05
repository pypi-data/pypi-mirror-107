from pymongo import MongoClient


def get_deposits(country='all', deposit_type='all'):
    """
    Fetch petroleum deposits data from public database. Source: PRIO

    Arguments
        country: 'all' or specific country (e.g. 'Norway')
        deposit_type: 'all' or specific type (e.g. 'oil', 'gas', 'oil and gas')

    Returns
        dataset as list of dicts. with 'name', 'country', 'lat', 'long', 'type', 'source', 'info'.
    """

    cluster = MongoClient('mongodb+srv://petrodc-user:1234@cluster0.qqzsq.mongodb.net/International?'
                          'retryWrites=true&w=majority')

    db = cluster['International']
    collection = db['Fields']

    df_filter = {}
    if country != 'all':
        df_filter['country'] = country
    if deposit_type != 'all':
        df_filter['type'] = deposit_type

    return list(collection.find(df_filter))
