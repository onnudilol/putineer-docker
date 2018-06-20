import requests
import json
import os


class YelpBot:

    def __init__(self):
        self.api_key = os.environ['YELP_API_KEY']
        self.business_url = 'https://api.yelp.com/v3/businesses'
        self.headers = {'Authorization': f'Bearer {os.environ["YELP_API_KEY"]}'}

    @staticmethod
    def return_results(response):
        """
        Returns results if total > 0, else raises TypeError

        Args:
            results: Response from requests GET

        Returns:
            Dictionary of results if total > 0
            Else raises TypeError
        """

        results = json.loads(response.content)

        if results['total'] > 0:
            return results

        else:
            raise TypeError('No search results')

    def business_search(self, params):
        """
        Searches the business endpoint

        https://www.yelp.com/developers/documentation/v3/business_search

        Args:
            params: Dict of search parameters.  Required params are location or latitude and longitude.
            Provide offset parameter to navigate through pages of results up to 1000th result.

        Returns:
            Dictionary of search results
        """

        r = requests.get(f'{self.business_url}/search', headers=self.headers, params=params)

        return self.return_results(r)

    def business_reviews(self, business_id):
        """
        Gets three reviews for a business

        Args:
            business_id: The yelp id of a business

        Returns:
            Dictionary of business reviews
        """

        r = requests.get(f'{self.business_url}/{business_id}/reviews', headers=self.headers)

        return self.return_results(r)

    def business_details(self, business_id):
        """
        Returns the details for a specific business

        Args:
            business_id: The yelp id of a business

        Returns:
            Dictionary of details for a business
        """

        r = requests.get(f'{self.business_url}/{business_id}', headers=self.headers)
        result = json.loads(r.content)

        if not result.get('error'):
            return result

        else:
            raise TypeError('Business not found')
