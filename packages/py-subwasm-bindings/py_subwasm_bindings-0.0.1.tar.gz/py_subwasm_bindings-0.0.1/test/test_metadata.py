# Python SR25519 Bindings
#
# Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import unittest

import subwasm


class MyTestCase(unittest.TestCase):

    def test_metadata_local_wasm(self):
        metadata_str = subwasm.get_metadata("fixtures/runtime_000.wasm")
        metadata_json = json.loads(metadata_str)
        self.assertIsNotNone(metadata_json)

    def test_metadata_rpc_url(self):
        metadata_str = subwasm.get_metadata("wss://rpc.polkadot.io/")
        metadata_json = json.loads(metadata_str)
        self.assertIsNotNone(metadata_json)


if __name__ == '__main__':
    unittest.main()
