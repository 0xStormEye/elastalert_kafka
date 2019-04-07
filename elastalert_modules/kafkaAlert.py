import json
from elastalert.alerts import Alerter
from confluent_kafka import Producer, KafkaError

class KafkaAlerter(Alerter):
  """ Push a message to Kafka topic """
  required_options = frozenset([
    'kafka_brokers',
    'kafka_ca_location',
    'kafka_pub_location',
    'kafka_priv_location',
    'kafka_priv_pass',
    'kafka_groupID',
    'kafka_topic',
  ])

  def __init__(self, rule):
    super(KafkaAlerter, self).__init__(rule)
    self.KAFKA_TOPIC = self.rule['kafka_topic']
    self.kafka_GROUPID = self.rule['kafka_groupID'] if self.rule.get('kafka_groupID', None) else 'elastalert'
    self.KAFKA_CONFIG = {
      'bootstrap.servers': self.rule['kafka_brokers'],
      'security.protocol': 'SSL',
      'ssl.ca.location': self.rule['kafka_ca_location'],
      'ssl.certificate.location': self.rule['kafka_pub_location'],
      'ssl.key.location' : self.rule['kafka_priv_location'],
      'ssl.keystore.password' : self.rule['kafka_priv_pass'],
      'group.id': self.kafka_GROUPID,

      'default.topic.config': {
        'auto.offset.reset': 'earliest'
      }
    }

    self.kafkaInstance = Producer(self.KAFKA_CONFIG)

  def delivery_report(self, err, msg):
    """ Called once for each message produced to indicate delivery result.
      Triggered by poll() or flush(). """
    if err is not None: # Not breaking
      print('[*] Message Delivery Error: {}'.format(err))
      print('Message Delivery: {}'.format(msg))

  def alert(self, matches):
    try:
      body = self.create_alert_body(matches)
      if isinstance(body, dict) or isinstance(body, list):
        body = json.dumps(body)

      self.kafkaInstance.poll(0)
      self.kafkaInstance.produce(self.KAFKA_TOPIC, body, callback=self.delivery_report)
      self.kafkaInstance.flush()
    except Exception as e:
      print("[*] [KafkaAlert] %s" % str(e))

  def get_info(self):
    return {
      'type': 'kafka',
      'config': self.KAFKA_CONFIG,
      'groupID': self.kafka_GROUPID,
      'topic': self.KAFKA_TOPIC,
    }


