from util import elastalert_logger, EAException
from elastalert.alerts import Alerter
from confluent_kafka import Producer, KafkaError

class KafkaAlerter(Alerter):
    """ Push a message to Kafka topic """
    required_options = frozenset(['kafka_brokers', 'kafka_groupID', 'kafka_topic'])

    def __init__(self, rule):
        super(KafkaAlerter, self).__init__(rule)
        self.kafka_brokers = self.rule['kafka_brokers']
        self.kafka_groupID = self.rule['kafka_groupID']
        self.kafka_topic = self.rule['kafka_topic']
        self.kafkaInstance = Producer({
            'bootstrap.servers': self.kafka_brokers,
            'group.id': self.kafka_groupID,
        })

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None: # Not breaking
            elastalert_logger.info('[*] Message Delivery Error: {}'.format(err))
            elastalert_logger.info('Message Delivery: {}'.format(msg))

    def alert(self, matches):
        try:
            body = self.create_alert_body(matches)
            self.kafkaInstance.poll(0)
            self.kafkaInstance.produce(self.kafka_topic, body, callback=self.delivery_report)
            self.kafkaInstance.flush()
        except Exception as e:
            EAException("[*] [KafkaAlert] %s" % str(e))

        elastalert_logger.info("[*] [KafkaAlert] %s" % str(e))

    def get_info(self):
        return {
            'type': 'kafka',
            'brokers': self.kafka_brokers,
            'groupID': self.kafka_groupID,
            'topic': self.kafka_topic,
        }


