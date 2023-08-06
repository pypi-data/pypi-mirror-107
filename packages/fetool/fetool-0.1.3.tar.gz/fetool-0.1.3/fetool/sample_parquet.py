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

import logging
from pyspark.sql import SparkSession


def sample_parquet_args(args):
    sample_parquet(args.parquet_path)


def sample_parquet(parquet_path, rows_threshold=100000):
    spark_app_name = "SampleParquet"
    spark = SparkSession.builder.appName(spark_app_name).getOrCreate()

    # Read input parquet
    df = spark.read.parquet(parquet_path)
    count = df.count()
    logging.warning("The count of dataframe is {}, target threshold is {}".format(count, rows_threshold))

    # Count ratio and sample dataset
    if count > rows_threshold:
        ratio = rows_threshold / count
        df = df.sample(ratio)
        logging.warning("Sample with ratio {} and get the final count {}".format(ratio, df.count()))
    else:
        logging.warning("Do not sample data for the dataset under threshold")

    # Save output sampled parquet
    if parquet_path.endswith("/"):
        output_parquet_path = "{}_sampled/".format(parquet_path[:-1])
    else:
        output_parquet_path = "{}_sampled/".format(parquet_path)
    logging.warning("Save output parquet after sampling in {}".format(output_parquet_path))
    df.write.parquet(output_parquet_path, mode="overwrite")
