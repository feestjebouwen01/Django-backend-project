import requests
from dateutil import parser
from requests.exceptions import RequestException

API_KEY = 'a25fc6aecf551494d9cd4f81c40fea29'
API_SECRET = '9e056b7102ebb125e8482e5dcf296ed3'
CLUSTER_URL = 'api.webshopapp.com'
SHOP_LANGUAGE = 'nl'

def get_customers(page=1):
    """ Fetch a page of customers from the API. """
    url = f'https://{API_KEY}:{API_SECRET}@{CLUSTER_URL}/{SHOP_LANGUAGE}/customers.json?page={page}&limit=250'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        customers = data['customers']
        # Check if there's a next page; adjust depending on the API's response structure
        has_more = bool(customers) and ('nextPage' in data or page < 2)
        return customers, has_more
    except RequestException as e:
        print(f"Failed to fetch customers: {str(e)}")
        return [], False

def fetch_all_customers():
    page = 1
    all_customers = []
    max_pages = 1
    while page <= max_pages:
        customers, has_more = get_customers(page)
        if not customers:
            break
        for customer in customers:
            customer_data = {
                'customer_id': customer['id'],
                'first_name': customer.get('firstname', ''),
                'last_name': customer.get('lastname', ''),
                'email': customer.get('email', ''),
                'created_at': parser.parse(customer['createdAt']) if customer.get('createdAt') else None,
                'updated_at': parser.parse(customer['updatedAt']) if customer.get('updatedAt') else None
            }
            all_customers.append(customer_data)
        if not has_more:
            break
        page += 1
    return all_customers
