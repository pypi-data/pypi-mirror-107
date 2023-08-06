# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import base64
import json
import typing as t


def serialize_for_confpy(obj: t.Optional[t.Any]) -> str:#TODO move?!
    return f"json.loads(base64.b64decode({repr(base64.b64encode(json.dumps(obj).encode()))}))"
