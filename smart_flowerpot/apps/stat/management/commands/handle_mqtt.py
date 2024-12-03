import hashlib
from django.utils import timezone
from decimal import Decimal
from django.core.management.base import BaseCommand
from paho.mqtt.client import Client as MQTTClient
from apps.stat.models import Flowerpot, EnvironmentData

class Command(BaseCommand):
    help = 'MQTT listener'

    def handle(self, *args, **options):
        mqtt_broker = '52.225.128.180'
        mqtt_port = 8883
        mqtt_topic = 'test'

        mqtt_client = MQTTClient(client_id="django_mqtt_listener")
        mqtt_client.tls_set(ca_certs='/etc/mosquitto/certs/ca.crt',
                            certfile='/home/iot/certs/test_kamil.crt',
                            keyfile='/home/iot/certs/test_kamil.key',
                            tls_version=2)
        mqtt_client.username_pw_set(username="brysia", password="brysia")

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS('Connected to MQTT broker'))
            else:
                self.stderr.write(self.style.ERROR(f'Failed to connect. Return code {rc}'))

        def on_message(client, userdata, message):
            try:
                payload = message.payload.decode('utf-8').split("|")
                if len(payload) < 4:
                    self.stderr.write(self.style.ERROR(f"Incomplete payload: {payload}"))
                    return

                flowerpot_slug = payload[0]
                temperature = Decimal(payload[1])
                soil_moisture = Decimal(payload[2])
                air_humidity = Decimal(payload[3])
                created_at = timezone.now()
                try:
                    flowerpot = Flowerpot.objects.get(slug=flowerpot_slug)
                except Flowerpot.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f"Flowerpot with slug '{flowerpot_slug}' does not exist"))
                    return


                env_data = EnvironmentData(
                    flowerpot=flowerpot,
                    temperature=temperature,
                    soil_moisture=soil_moisture,
                    air_humidity=air_humidity
                )
                env_data.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Message received and saved: {flowerpot.slug} {temperature} {soil_moisture} {air_humidity} {created_at}'
                ))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing message: {str(e)}'))


        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        mqtt_client.connect(mqtt_broker, mqtt_port)
        mqtt_client.subscribe(mqtt_topic)
        mqtt_client.loop_forever()

    @staticmethod
    def generate_hash(slug, temperature, soil_moisture, air_humidity, created_at):
        """Generate a unique hash based on flowerpot slug and environmental data."""
        hash_source = f"{slug}{temperature}{soil_moisture}{air_humidity}{created_at}"
        return hashlib.md5(hash_source.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    Command().handle(None, None)
