#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2021 4Paradigm
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import logging
import yaml
from pyspark.sql import SparkSession


def run_yaml_args(args):
    run_yaml(args.yaml_path)


def run_yaml(yaml_path):
    # TODO: Check if necessary keys are exist

    # Read yaml file
    try:
        yaml_config = yaml.load(open(yaml_path, "r"))
    except yaml.YAMLError as exc:
        mark = exc.problem_mark
        logging.error("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
        exit(-1)

    # Create SparkSession
    spark_builder = SparkSession.builder
    for k, v in yaml_config.get("sparkConfig", {}).items():
        if k == "name":
            spark_builder = spark_builder.appName(v)
        elif k == "master":
            spark_builder = spark_builder.master(v)
        else:
            spark_builder = spark_builder.config(k, v)
    spark = spark_builder.getOrCreate()

    # Register tables
    for k, v in yaml_config.get("tables", {}).items():
        spark.read.parquet(v).createOrReplaceTempView(k)

    # Read SQL file
    if "sql_file" in yaml_config:
        with open(yaml_config.get("sql_file"), "r") as f:
            sql_text = f.read()
    else:
        sql_text = yaml_config.get("sql_text")

    # Read output path
    output_path = yaml_config.get("output_path", "file:///tmp/fetool_output/")

    # Run SparkSQL
    output_df = spark.sql(sql_text)
    start = time.time()
    output_df.write.mode("overwrite").parquet(output_path)
    end = time.time()
    print("Execution time: {}".format(end - start))
