from django.utils import timezone
from decimal import Decimal
from django.core.management.base import BaseCommand
from paho.mqtt import client as MQTTClient

class Command(BaseCommand):
    help = 'MQTT Publisher'

    def send_threshold(self, mqtt_client, flowerpot_id, moisture_threshold):
        try:
            message = f"{flowerpot_id}|{moisture_threshold}"
            mqtt_client.publish('prog', message)
            self.stdout.write(self.style.SUCCESS(f"Sent threshold update: {message} on topic prog"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error sending threshold update: {str(e)}"))

    def add_arguments(self, parser):
        parser.add_argument('flowerpot_id', type=str)
        parser.add_argument('moisture_thresh', type=int)


    def handle(self, *args, **options):
        flow_id = options['flowerpot_id']
        moist_thresh = options['moisture_thresh']
        mqtt_broker = '52.225.128.180'
        mqtt_port = 1883
        mqtt_topic = 'prog'

        mqtt_client = MQTTClient.Client(client_id="django_mqtt_publisher")
        mqtt_client.username_pw_set(username="brysia", password="brysia")

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connect dziala")
                self.stdout.write(self.style.SUCCESS('Connected to MQTT broker'))
            else:
                print("Connect niedzlaa")
                self.stderr.write(self.style.ERROR(f'Failed to connect. Return code {rc}'))

        mqtt_client.on_connect = on_connect
        mqtt_client.connect(mqtt_broker, mqtt_port)
        mqtt_client.loop_start()
        self.send_threshold(mqtt_client, flow_id, moist_thresh)
        mqtt_client.loop_stop()


if __name__ == '__main__':
    Command().handle(None, None)
