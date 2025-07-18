# Data Engineering Project - Task 2

## TL;DR

This project simulates a continuous stream of sensor-like air quality data (from a Kaggle dataset) to build a robust data ingestion system. It leverages **Apache Kafka** for high-throughput streaming, **MongoDB** for raw time-series data storage, and **Docker/Docker Compose** for streamlined deployment. The ultimate goal is to demonstrate a scalable pipeline for a real-world environmental observation system, applicable for municipal use.

## About

Imagine a municipality that has installed a large number of physical sensors across a mid-sized city to gain deeper insights into environmental conditions. Their primary objective is to improve overall air quality and reduce pollution by defining targeted measures. To achieve this, they plan to collect data from all these locations in a streaming fashion.

This project's system is designed to simulate such a target environment and effectively handle large volumes of sensor data streams. Incoming data will be processed in near real-time and stored in a reliable, robust database, making it accessible for further analysis, anomaly detection, metric calculation, and more.

To accomplish this, the following proven technologies have been selected for their suitability in such use cases:

1.  **Python**: Considered a go-to solution for data-intensive tasks and applications like this.
2.  **Apache Kafka**: A popular framework for robust, reliable, scalable, and maintainable data streaming, supporting the implementation of the publish-subscribe pattern. For this use case, a single topic is used to send and receive sensor data via the broker.
3.  **MongoDB**: A widely-used, document-based NoSQL database solution that performs well, particularly for time-series-like data.
4.  **Docker + Docker Compose**: A perfect match for packaging and distributing this application in a multi-container setup.

![](docs/images/data_architecture.drawio.svg)

## Prerequisites

To make use of the prepared resources and run the entire data system, the following dependencies are required:

*   `Docker`
*   `Docker Compose`

For development purposes, additional tools and frameworks are needed:

*   `Python 3.10`
*   `uv 0.8.0`
*   `ruff (0.12.4)`

## Usage

tbd.