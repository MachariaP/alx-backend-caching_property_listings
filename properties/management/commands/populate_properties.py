from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the database with sample property data'

    def handle(self, *args, **kwargs):
        properties = [
            {
                'title': 'Beautiful Beach House',
                'description': 'Stunning beachfront property with panoramic ocean views',
                'price': Decimal('1250000.00'),
                'location': 'Miami, FL'
            },
            {
                'title': 'Modern City Apartment',
                'description': 'Luxury apartment in downtown with all modern amenities',
                'price': Decimal('750000.00'),
                'location': 'New York, NY'
            },
            {
                'title': 'Cozy Mountain Cabin',
                'description': 'Rustic cabin perfect for weekend getaways in the mountains',
                'price': Decimal('350000.00'),
                'location': 'Aspen, CO'
            },
        ]
        
        for prop_data in properties:
            Property.objects.create(**prop_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated properties'))
