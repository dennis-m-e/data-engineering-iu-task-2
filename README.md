# Data Engineering Project - Task 2

## TL;DR

This project simulates a continuous stream of sensor-like air quality data (from a Kaggle dataset) to build a robust data ingestion system. It leverages **Apache Kafka** for high-throughput streaming, **MongoDB** for raw time-series data storage, and **Docker/Docker Compose** for streamlined deployment. The ultimate goal is to demonstrate a scalable pipeline for a real-world environmental observation system, applicable for municipal use.

## About

Imagine a municipality that has installed a large number of physical sensors across a mid-sized city to gain deeper insights into environmental conditions. Their primary objective is to improve overall air quality and reduce pollution by defining targeted measures. To achieve this, they plan to collect data from all these locations in a streaming fashion.

This project's system is designed to simulate such a target environment and effectively handle large volumes of sensor data streams. Incoming data will be processed in near real-time and stored in a reliable, robust database, making it accessible for further analysis, anomaly detection, metric calculation, and more.

### Technologies

To accomplish this, the following proven technologies have been selected for their suitability in such use cases:

1.  **Python**: Considered a go-to solution for data-intensive tasks and applications like this.
2.  **Apache Kafka**: A popular framework for robust, reliable, scalable, and maintainable data streaming, supporting the implementation of the publish-subscribe pattern. For this use case, a single topic is used to send and receive sensor data via the broker.
3.  **MongoDB**: A widely-used, document-based NoSQL database solution that performs well, particularly for time-series-like data.
4.  **Docker + Docker Compose**: A perfect match for packaging and distributing this application in a multi-container setup.

### Dataset

For simulating the continuous stream of sensor data, the Kaggle dataset [Air Quality and Pollution Assessment](https://www.kaggle.com/datasets/mujtabamatin/air-quality-and-pollution-assessment/data) is used, containing the following key features:

- `Temperature (°C)`: Average temperature of the region.
- `Humidity (%)`: Relative humidity recorded in the region.
- `PM2.5 Concentration (µg/m³)`: Fine particulate matter levels.
- `PM10 Concentration (µg/m³)`: Coarse particulate matter levels.
- `NO2 Concentration (ppb)`: Nitrogen dioxide levels.
- `SO2 Concentration (ppb)`: Sulfur dioxide levels.
- `CO Concentration (ppm)`: Carbon monoxide levels.
- `Proximity to Industrial Areas (km)`: Distance to the nearest industrial zone.
- `Population Density (people/km²)`: Number of people per square kilometer in the region.

The dataset is stored under [`data/sample_air_quality_pollution_data.csv`](data/sample_air_quality_pollution_data.csv) in this repository.

### Kafka Topic

For simplicity, each row of the dataset will be published to and read from one topic called `topic_air_quality_pollution_data`, no matter which sensor the data is coming from. For real-world usage, a dedicated topic structure is preferred, considering different dimensions like sensor type or area the sensor belongs to.

### Architecture

![](docs/images/data_architecture.drawio.svg)

The image above depicts the data system and it's components. They are briefly described in the following chapters.

#### Data streamer

A small component responsible for reading the static dataset and sending it to the kafka broker in a given time interval. The component is containerized and built based on the docker image `python:3.10-slim-bookworm` (see [**`dockerfile.producer`**](dockerfile.producer)). Some parameters can be adjusted in the [**configuration file**](config/config.yml).

#### Kafka broker

A Kafka broker is needed to enable the communication between the data producer and consumer. For this system, the `bitnami/kafka` image has been used. All the configuration with regards to the broker setup is done via the [**`docker-compose.yaml`**](docker-compose.yml) file.

#### Data consumer

This component is based on the image `python:3.10-slim-bookworm` as well and is listening to the topic, where the simulated sensor data is expected to be sent on (can be adapted in the configuration file). Once a new message has been received, it is written to the MongoDB instance afterwards. 

#### MongoDB

For this component, the official `mongo` image is used without any particular changes. For accessibility of the stored data, the mongo default port `27017` is exposed and forwarded to the host system. Accessing the data can be done via the client application MongoDB Compass. Find more information on the [**official website**](https://www.mongodb.com/products/tools/compass).  

### Deployment

In order to ensure reusability and robustness, the application is managed and deployed via docker compose. All containers are hosted in the same bridge network called `app-network`. Only port `27017` of the `mongo` service is forwarded, such that one can access the database from outside (e.g. via [**MongoDB Compass**](https://www.mongodb.com/products/tools/compass) or the MongoDB VS Code extension). Other than that, the folder `/tmp` of all containers is mounted to the host folder of the same name `/tmp` (please make sure this folder exists on the host system!). If kept like this, logs can be found under `/tmp` on the host system (format: {timestamp}_{component}.log). 

Optionally, the `/data/db` folder of the `mongo` container can be mounted to one existing on the host system in order to pertain the data between individual system runs (see docker compose file in the respective section). If not mounted, the data will be gone after a restart via docker compose.

For more information, have a look into the docker compose file located in the [**root of the repository**](docker-compose.yml). 

### Design descisions

#### `pydantic`

`pydantic` is used for both the configuration handling as well as for modelling the simulated sensor data. It's a great choice when it comes to validating serialized or "type-less" data and provides great features for reading data from e.g. `*.yaml` files into pre-defined types.

#### Type annotations

The Python-native `typing` module is heavily used throughout the codebase in order to improve readability and utilize editor-support when it comes to type handling. Having that available, mistakes and errors with regards to data handling can be avoided already during the development phase.

### Configuration

To provide configurability to some extend, a configuration interface has been prepared.
The file for changing some of the most important application parameters is stored under [**`config/config.yml`**](config/config.yml) and adheres to the following format:

```yaml
kafka:
  topic_name: topic_air_quality_pollution_data # Name of the Kafka topic to which the producer will send data
  bootstrap_servers: kafka # Kafka broker
  port: 9092 # Port on which the Kafka broker is running

streamer:
  interval_in_seconds: 2.0 # Interval in seconds for the data streamer to fetch new data
  is_infinite: false # If true, the streamer will run indefinitely; if false, it will stop after fetching data once

database:
  host: mongodb # Hostname of the MongoDB server
  port: 27017 # Port on which MongoDB is running
  name: air_quality_pollution_db # Name of the MongoDB database
  collection_name: air_quality_pollution_data # Name of the MongoDB collection where data will be stored

app:
  logs:
    folder: /tmp # folder inside the container where the logs shall be stored - make sure this matches the settings in the docker compose file
    filemode: w # "a" for append, "w" for overwrite

```

If further configuration parameters are needed, they must be implemented in the `pydantic` [**data model for the configuration**](src/data_engineering_iu_task_2/config.py) as well.

### Implementation

The implementation of the system is separated into two different modules (`data_streamer` and `data_consumer`, see description under [**Architecture**](#architecture)). Other than that, some code has been prepared, which is used by both of the modules (e.g. data models and configuration interface).

Some tests (just for demonstration - not all code is covered!) can be found under [**`tests/`**](tests/).

### Improvements

As this application serves as an exemplary implementation to showcase the capabilities of data frameworks like Kafka or MongoDB, it is far from complete or perfect. Hence, there are several improvements, which are worth to be considered, if such a data system would be used in in the real-world, as described above. See a three examples below:

- **Database security**: In order to make sure data can only be accessed by certain people, proper security and user accounts should be prepared.
- **Automated deployment**: Docker compose is already a nice way to manage a multi-container application. However, in production a proper release strategy and the respective CI system is needed in order to bring code reliable and fast into the target environment.
- **Container Orchestration**: For such a simulated use case, it is enough to have a small setup like this. However, in production the amount of data can be huge and varies heavily over time. Container orchestration (e.g. with Kubernetes) would be a good way to scale such an application in a robust way and even handle peaks properly by adding or removing additional container instances fast.

## Getting started

### Prerequisites

To make use of the prepared resources and run the entire data system, the following dependencies are required:

*   `Docker`
*   `Docker Compose`
*   `git`
*   `/tmp` folder must exist &rarr; unix system. If not possible, change the docker compose file accordingly.

For development purposes, additional tools and frameworks are needed:

*   `Python 3.10`
*   `uv 0.8.0`
*   `ruff (0.12.4)`

### Usage

Assuming all mentioned prerequisites are covered, you can start using the application by following the below described steps.

1) Open a new terminal and clone this repository to your local machine

```bash
cd <path/to/your/desired/directory> && git clone https://github.com/dennis-m-e/data-engineering-iu-task-2.git
```

1) Start the system via docker compose from the same terminal. Please note that the startup procedure can take some time and you might have to wait a one or two minutes until data appears in the database!

```bash
cd data-engineering-iu-task-2 && docker compose up --build
```

3) View the logs under `/tmp` (or the name you used in case you did change the default value) of your host system

```bash
cat /tmp/{timestamp}_{component-name}.log
```

4) Check the MongoDB data by means of MongoDB Compass (installation required) or via the VS Code extension **MongoDB for VS Code**. You can open the client application and connect to the database on `localhost:27017` (port is forwarded).

5) In case you want to shut the application again, press `Ctrl+C` and run `docker compose down` afterwards.

### Run tests

In order to run the unit tests, stored under [**`tests/`**](tests/), you have to execute the following command

```bash
uv run pytest . -v
```

## Troubleshooting

### Container already in use

If you end up with an error like the following 

```bash
Error response from daemon: Conflict. The container name <container-name> is already in use by container ...
```

after running `docker compose up --build`, you might have to run `docker compose down && docker container prune` from the root of the repository.  

