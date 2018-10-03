# elastalert_kafka
Kafka alert plugin for Elastalert

---

## Quick Introduction

This is an **Kafka Alert Plugin** of [Elastalert](https://github.com/Yelp/elastalert), which means the alert generated from Elastalert will be sent to the specific Kafka topic. This plugin is based on multiple Python libraries, which requires you to install them manually before using.

## Installation

1. Git Clone this project: `git clone https://github.com/windhamwong/elastalert_kafka.git`
2. Copy `elastalert_modules/kafkaAlert.py` into the folder `elastalert_modules` under Elastalert folder. (If you can't find this folder under Elastalert, simply just copy the folder `elastalert_modules/` into Elastalert instead.
3. ...Guess what? Profit!

## Usage
1. You need to specify the path of this library in your rule.

```
alert:
  - "elastalert_modules.kafkaAlert.KafkaAlerter"
```

2. Configure the Kafka info.

```
# Kafka server
kafka_brokers: "localhost:9091"
# Kafka producer name in Zookeeper
kafka_groupID: "elastalert"
# Kafka topic
kafka_topic: "elastalert-alert"
```

2b. Multiple Kafka topics (Untested)

```
alert:
	- "elastalert_modules.kafkaAlert.KafkaAlerter"
		- kafka_brokers: "localhost:9091"
		- kafka_groupID: "elastalert"
		- kafka_topic: "elastalert-alert"
```

## Example

You can see the example rule under `rules`.
