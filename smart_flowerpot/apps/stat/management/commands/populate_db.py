import random
import hashlib
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.stat.models import Flowerpot, EnvironmentData

class Command(BaseCommand):
    help = "Populate the database with random flowerpots and environment data."

    def handle(self, *args, **kwargs):
        self.clear_existing_data()
        flowerpots = self.create_flowerpots(num=20)
        environment_data = self.create_environment_data(flowerpots, logs_per_flowerpot=20)

        EnvironmentData.objects.bulk_create(environment_data)
        
        self.stdout.write(self.style.SUCCESS("Successfully populated the database with flowerpots and environment data."))

    def clear_existing_data(self):
        """Delete all existing data for Flowerpot and EnvironmentData models."""
        Flowerpot.objects.all().delete()
        EnvironmentData.objects.all().delete()
        self.stdout.write("Cleared existing data.")

    def create_flowerpots(self, num=20):
        """Generate and bulk create a specified number of flowerpots."""
        flowerpots = [
            Flowerpot(
                name=f"Flowerpot {i + 1}",
                description=f"Description for Flowerpot {i + 1}",
                location=random.choice(["Living Room", "Garden", "Office", "Balcony"])
            )
            for i in range(num)
        ]

        Flowerpot.objects.bulk_create(flowerpots)
        self.stdout.write(f"Created {num} flowerpots.")
        
        return Flowerpot.objects.all()  
    
    def create_environment_data(self, flowerpots, logs_per_flowerpot=20):
        """Generate environment data logs for each flowerpot."""
        environment_data = []

        for flowerpot in flowerpots:
            for _ in range(logs_per_flowerpot):
                data = self.generate_environment_data(flowerpot)
                environment_data.append(data)

        self.stdout.write(f"Generated {logs_per_flowerpot * len(flowerpots)} environment data logs.")
        return environment_data

    def generate_environment_data(self, flowerpot):
        """Generate a single environment data entry with random values and a unique hash."""
        temperature = round(random.uniform(10, 35), 2)
        moisture = round(random.uniform(20, 80), 2)
        ph_level = round(random.uniform(5, 8), 2)
        light_level = round(random.uniform(100, 1000), 2)
        humidity = round(random.uniform(30, 90), 2)
        created_at = timezone.now()

        log_name = self.generate_hash(
            flowerpot.name, temperature, moisture, ph_level, light_level, humidity, created_at
        )

        return EnvironmentData(
            flowerpot=flowerpot,
            temperature=temperature,
            moisture=moisture,
            ph_level=ph_level,
            light_level=light_level,
            humidity=humidity,
            hash=log_name,
            created_at=created_at
        )

    @staticmethod
    def generate_hash(name, temperature, moisture, ph_level, light_level, humidity, created_at):
        """Generate a unique hash based on flowerpot name and environmental data."""
        hash_source = f"{name}{temperature}{moisture}{ph_level}{light_level}{humidity}{created_at}"
        return hashlib.md5(hash_source.encode('utf-8')).hexdigest()
