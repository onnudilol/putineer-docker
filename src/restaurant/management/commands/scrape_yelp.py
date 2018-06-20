from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from restaurant.models import Restaurant
from yelp_api.yelpbot import YelpBot


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--location', type=str)
        parser.add_argument('--coord')
        parser.add_argument('term', nargs='+', type=str)

    @staticmethod
    def process_results(restaurant):
        fields = {'name': restaurant['name'],
                  'yelp_url': restaurant['url'],
                  'image_url': restaurant['image_url'],
                  'address': ' '.join(restaurant['location']['display_address']),
                  'coords': Point(restaurant['coordinates']['latitude'],
                                  restaurant['coordinates']['longitude'])}

        r, created = Restaurant.objects.get_or_create(yelp_id=restaurant['id'], defaults=fields)

        if created:
            print(f'New! {r.name}')

            return True

    def handle(self, *args, **options):
        yb = YelpBot()
        params = {'location': options['location'], 'term': options['term']}

        if options['coord']:
            coords = options['coord'].split(', ')
            params['latitude'] = coords[0]
            params['longitude'] = coords[1]

        restaurants = yb.business_search(params)
        total = restaurants['total']
        offset = 0
        new_items = 0
        print(f'total: {total}')

        while offset < total:
            params['offset'] = offset
            restaurants = yb.business_search(params)
            len_results = len(restaurants['businesses'])

            if restaurants['businesses']:

                for restaurant in restaurants['businesses'][:-1]:
                    created = self.process_results(restaurant)

                    if created:
                        new_items += 1

                else:
                    created = self.process_results(restaurants['businesses'][-1])

                    if created:
                        new_items += 1

                    offset += len_results

            # The yelp api returns an inconsistent total, so I gotta check if the results are not null
            # See https://github.com/Yelp/yelp-api/issues/162
            else:
                break

        print(f'Added {new_items} new entries')
