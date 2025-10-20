from django.core.management.base import BaseCommand
from insights.models import Region

class Command(BaseCommand):
    help = 'Seeds the database with sample regions'

    def handle(self, *args, **options):
        regions_data = [
            {'name': 'Atlanta', 'lat': 33.7490, 'lng': -84.3880},
            {'name': 'New York', 'lat': 40.7128, 'lng': -74.0060},
            {'name': 'San Francisco', 'lat': 37.7749, 'lng': -122.4194},
            {'name': 'Los Angeles', 'lat': 34.0522, 'lng': -118.2437},
            {'name': 'Chicago', 'lat': 41.8781, 'lng': -87.6298},
            {'name': 'Miami', 'lat': 25.7617, 'lng': -80.1918},
            {'name': 'Seattle', 'lat': 47.6062, 'lng': -122.3321},
            {'name': 'Boston', 'lat': 42.3601, 'lng': -71.0589},
        ]

        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                name=region_data['name'],
                defaults={
                    'lat': region_data['lat'],
                    'lng': region_data['lng']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created region: {region.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Region already exists: {region.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal regions in database: {Region.objects.count()}')
        )

