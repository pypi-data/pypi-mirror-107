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

import os
import logging
import subprocess
from prettytable import PrettyTable


def benchmark_args(args):
    benchmark(args.command)


def run_command_get_result(command, env):
    print("Run the shell command: {}".format(command))
    command_result = subprocess.run(command.split(" "), stdout=subprocess.PIPE, env=env)
    stdout = command_result.stdout.decode('utf-8')
    # TODO: Get result with regex
    result = stdout
    return result


def benchmark(command):
    # Check environment variables
    if "SPARK_HOME" not in os.environ or ("SPARKFE_HOME" not in os.environ):
        print("SPARK_HOME and SPARKFE_HOME should be set for fetool benchmark")
        return -1

    spark_env = os.environ.copy()
    sparkfe_env = os.environ.copy()
    sparkfe_env["SPARK_HOME"] = os.getenv("SPARKFE_HOME")

    spark_result = run_command_get_result(command, spark_env)
    sparkfe_result = run_command_get_result(command, sparkfe_env)

    # Print result as table
    table = PrettyTable()
    table.field_names = ["Spark Result", "SparkFE Result"]
    table.add_row([spark_result, sparkfe_result])
    print(table)
