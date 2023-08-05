# Copyright (c) 2021, Fruiti Limited
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import logging

from .converters import (
    convert_custom_timestamp_range,
    convert_iso_datetime_to_timestamp,
)

logger = logging.getLogger(__name__)


class SecondState:
    def __init__(self, start: str, finish: str) -> None:
        self.state = self.init_state(start, finish)
        self.state_start = convert_iso_datetime_to_timestamp(start)

    def get_state(self) -> list:
        return self.state

    def init_state(self, start: str, finish: str) -> list:
        difference = convert_iso_datetime_to_timestamp(
            finish
        ) - convert_iso_datetime_to_timestamp(start)

        return [0 for x in range(difference)]

    def toggle(self, start: str, finish: str, set: bool) -> list:
        """
        Toggle position in the state by replacing zeros with ones or vice-versa
        at the relevant seconds.
        """
        start_timestamp = convert_iso_datetime_to_timestamp(start)
        finish_timestamp = convert_iso_datetime_to_timestamp(finish)

        start_difference = start_timestamp - self.state_start
        if start_difference < 0:
            start_difference = 0

        finish_difference = finish_timestamp - self.state_start
        state_length = len(self.get_state())
        if finish_difference >= state_length:
            finish_difference = state_length - 1

        for x in range(start_difference, finish_difference):
            self.state[x] = 1 if set else 0

        return self.get_state()

    def set(self, start: str, finish: str) -> list:
        return self.toggle(start, finish, True)

    def unset(self, start: str, finish: str) -> list:
        return self.toggle(start, finish, False)

    def get(self, minutes=0, seconds=0, custom_format=False) -> list:
        """
        Return a list of datetime ranges that allow enough time for the required
        duration of minutes or seconds
        """
        if minutes > 0:
            seconds = minutes * 60

        if seconds <= 0:
            logger.fatal("Please specify minutes or seconds")
            raise ValueError

        possible_epochs = self.get_possible_epochs()

        result = []

        for epoch in possible_epochs:
            while epoch[0] + seconds - 1 <= epoch[1]:
                start = epoch[0] + self.state_start
                finish = epoch[0] + self.state_start + seconds
                result.append(f"{start}_{finish}")
                epoch[0] += seconds

        if not custom_format:
            iso_datetimes_ranges = []
            for custom_timestamp_range in result:
                iso_datetimes_ranges.append(
                    convert_custom_timestamp_range(custom_timestamp_range)
                )
            result = iso_datetimes_ranges

        return result

    def get_epoch_groups(self, epochs: list) -> list:
        """
        See:
        https://stackoverflow.com/questions/2154249/identify-groups-of-continuous-numbers-in-a-list
        """
        first = last = epochs[0]
        for n in epochs[1:]:
            if n - 1 == last:  # Part of the group, bump the end
                last = n
            else:  # Not part of the group, yield current group and start a new
                yield first, last
                first = last = n
        yield first, last  # Yield the last group

    def get_possible_epochs(self) -> list:
        """
        Return a list of possible epoch ranges
        """
        epochs = []
        for index, value in enumerate(self.state):
            if value == 1:
                epochs.append(index)

        result = []
        if epochs:
            for epoch_range in self.get_epoch_groups(epochs):
                result.append([epoch_range[0], epoch_range[1]])
        return result
