# -------------------------------------------------------------------
# Copyright 2021 http-spammer authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# -------------------------------------------------------------------
import time
from typing import Callable, Tuple

__all__ = ['Timestamp', 'CLOCK', 'now', 'now']


#: start-time,endtime tuple
Timestamp = Tuple[float]


#: Sleep interval for loops
CLOCK = 1e-3


#: Get current time
now: Callable[[], float] = lambda: float(time.monotonic())
