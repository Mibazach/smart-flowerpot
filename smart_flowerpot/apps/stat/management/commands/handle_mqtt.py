# mqtt_listener.py

import os
import sys
import hashlib
from django.core.management.base import BaseCommand
from paho.mqtt.client import Client as MQTTClient
from apps.stat.models import Flowerpot, EnvironmentData
from decimal import Decimal

class Command(BaseCommand):
    help = 'MQTT listener'

    def handle(self, *args, **options):
        mqtt_broker = '52.225.128.180'
        mqtt_port = 1883
        mqtt_topic = 'test'

        mqtt_client = MQTTClient(client_id="django_mqtt_listener")
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS('Connected to MQTT broker'))

            else:
                self.stderr.write(self.style.ERROR(f'Failed to connect. Return code {rc}'))

        def on_message(client, userdata, message):
            payload = None
            flowerpot = None
            
            try:
                payload = message.payload.decode('utf-8').split("|")
                if len(payload) < 7:
                    self.stderr.write(self.style.ERROR(f"Incomplete payload: {payload}"))
                    return
                
                flowerpot_id = int(payload[0])
                temperature = Decimal(payload[1])
                moisture = Decimal(payload[2])
                ph_level = Decimal(payload[3])
                light_level = Decimal(payload[4])
                humidity = Decimal(payload[5])
                created_at = payload[6]
                try:
                    flowerpot = Flowerpot.objects.get(pk=flowerpot_id)
                except Flowerpot.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f"Flowerpot with ID {flowerpot_id} does not exist"))
                    return

                hash = self.generate_hash(flowerpot, temperature, moisture, ph_level, light_level, humidity, created_at)
                env_data = EnvironmentData(flowerpot=flowerpot, temperature=temperature, moisture=moisture, ph_level=ph_level, light_level=light_level, humidity=humidity, hash=hash, created_at=created_at)
                env_data.save()
                self.stdout.write(self.style.SUCCESS(f'Message received and saved: {flowerpot} {temperature} {moisture} {ph_level} {light_level} {humidity} {created_at}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing message: {str(e)}'))

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        # Connect to MQTT broker
        mqtt_client.connect(mqtt_broker, mqtt_port)
        mqtt_client.subscribe(mqtt_topic)

        # Start MQTT loop
        mqtt_client.loop_forever()
    @staticmethod
    def generate_hash(name, temperature, moisture, ph_level, light_level, humidity, created_at):
        """Generate a unique hash based on flowerpot name and environmental data."""
        hash_source = f"{name}{temperature}{moisture}{ph_level}{light_level}{humidity}{created_at}"
        return hashlib.md5(hash_source.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    Command().handle(None, None)

