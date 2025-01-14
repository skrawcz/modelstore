#    Copyright 2020 Neal Lathia
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import pytest

import modelstore
from modelstore.meta import metadata

# pylint: disable=protected-access,missing-function-docstring


def test_generate_for_model():
    exp = {
        "domain": "test-model",
        "model_id": "test-model-id",
        "model_type": {"library": "model-library", "name": "model-class"},
    }
    res = metadata.generate_for_model(
        domain="test-model",
        model_id="test-model-id",
        model_info={"library": "model-library", "name": "model-class"},
    )
    assert exp == res


def test_generate_for_code():
    deps_list = ["pytest"]
    res = metadata.generate_for_code(deps_list)
    assert res["runtime"].startswith("python")
    # Warning: not testing for presence of "git" key, as this is flaky
    # when run via Github actions
    assert all([k in res for k in ["user", "created", "dependencies"]])
    assert res["dependencies"]["pytest"] == pytest.__version__
    if "git" in res:
        assert res["git"]["repository"] == "modelstore"


def test_generate():
    res = metadata.generate(model_meta=None, storage_meta=None, code_meta=None)
    assert all(k in res for k in ["model", "storage", "code", "modelstore"])
    assert res["modelstore"] == modelstore.__version__


def test_remove_nones():
    exp = {"a": "value-a"}
    res = metadata._remove_nones({"a": "value-a", "b": None})
    assert exp == res
