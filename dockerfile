ARG JRE_VERSION=11-jre
FROM openjdk:${JRE_VERSION} AS base

# Define default Spark version
ARG SPARK_VERSION_DEFAULT=3.2.2
# Define default Hadoop version
ARG HADOOP_VERSION_DEFAULT=3.2
# Define default Hadoop aws jar version
ARG HADOOP_AWS_VERSION_DEFAULT=3.2.0

# Define ENV variables
ENV SPARK_VERSION=${SPARK_VERSION_DEFAULT}
ENV HADOOP_VERSION=${HADOOP_VERSION_DEFAULT}
ENV HADOOP_AWS_VERSION=${HADOOP_AWS_VERSION_DEFAULT}

RUN apt-get update \
    && apt-get install -y bash tini libc6 libpam-modules krb5-user libnss3 procps

FROM base AS spark-base

# Download and extract Spark
RUN curl -L https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

FROM spark-base AS sparkbuilder

# Set SPARK_HOME
ENV SPARK_HOME=/opt/spark

# Extend PATH environment variable
ENV PATH=${PATH}:${SPARK_HOME}/bin

# Create the application directory
RUN mkdir -p /app


ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

RUN apt-get update -y \
    && apt-get install -y python3 python3-pip \
    && pip3 install --upgrade pip setuptools \
    # Removed the .cache to save space
    && rm -r /root/.cache && rm -rf /var/cache/apt/*

WORKDIR /app
ADD . /app

# Install application specific python dependencies
RUN pip3 install -r requirements.txt

USER root

CMD ["/bin/bash", "run_pa.sh" ]
