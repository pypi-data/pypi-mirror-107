# Copyright (c) 2021, Fruiti Limited
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime


def convert_custom_timestamp_range(timestamp_range: str) -> list:
    result = timestamp_range.split("_")

    result[0] = convert_timestamp_to_iso_datetime(result[0])
    result[1] = convert_timestamp_to_iso_datetime(result[1])

    return result


def convert_iso_datetime_to_timestamp(iso_datetime: str) -> int:
    return int(datetime.fromisoformat(iso_datetime).timestamp())


def convert_timestamp_to_iso_datetime(timestamp: int) -> str:
    return str(datetime.fromtimestamp(int(timestamp)).isoformat())
