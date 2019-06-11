########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


from dsl_parser import utils
from dsl_parser.exceptions import (ERROR_MISSING_PROPERTY,
                                   DSLParsingLogicException)


def validate_missing_inputs(inputs, schema_inputs):
    """Check that all inputs defined in schema_inputs exist in inputs"""

    missing_inputs = set(schema_inputs) - set(inputs)
    if missing_inputs:
        if len(missing_inputs) == 1:
            message = "Input '{0}' is missing a value".format(
                missing_inputs.pop())
        else:
            formatted_inputs = ', '.join("'{0}'".format(input_name)
                                         for input_name in missing_inputs)
            message = "Inputs {0} are missing a value".format(formatted_inputs)

        raise DSLParsingLogicException(ERROR_MISSING_PROPERTY, message)


def merge_schema_and_instance_inputs(schema_inputs,
                                     instance_inputs):

    flattened_schema_inputs = utils.flatten_schema(schema_inputs)
    merged_inputs = dict(
            flattened_schema_inputs.items() +
            instance_inputs.items())

    validate_missing_inputs(merged_inputs, schema_inputs)
    return merged_inputs


def operation_mapping(implementation, inputs, executor,
                      max_retries, retry_interval, timeout,
                      timeout_recoverable, timeout_error):
    return {
        'implementation': implementation,
        'inputs': inputs,
        'executor': executor,
        'max_retries': max_retries,
        'retry_interval': retry_interval,
        'timeout': timeout,
        'timeout_recoverable': timeout_recoverable,
        'timeout_error': timeout_error
    }


def no_op():
    return operation_mapping(
            implementation='',
            inputs={},
            executor=None,
            max_retries=None,
            retry_interval=None,
            timeout=None,
            timeout_recoverable=None,
            timeout_error=None
    )


def no_op_operation(operation_name):
    return operation(
            name=operation_name,
            plugin_name='',
            operation_mapping='',
            operation_inputs={},
            executor=None,
            max_retries=None,
            retry_interval=None,
            timeout=None,
            timeout_recoverable=None,
            timeout_error=None
    )


def operation(name,
              plugin_name,
              operation_mapping,
              operation_inputs,
              executor,
              max_retries,
              retry_interval,
              timeout,
              timeout_recoverable,
              timeout_error):
    return {
        'name': name,
        'plugin': plugin_name,
        'operation': operation_mapping,
        'executor': executor,
        'inputs': operation_inputs,
        'has_intrinsic_functions': False,
        'max_retries': max_retries,
        'retry_interval': retry_interval,
        'timeout': timeout,
        'timeout_recoverable': timeout_recoverable,
        'timeout_error': timeout_error
    }
