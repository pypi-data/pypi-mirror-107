from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import pytest
from gcloud.rest.datastore import Datastore
from gcloud.rest.datastore import Key
from gcloud.rest.datastore import Operation
from gcloud.rest.datastore import PathElement
from gcloud.rest.datastore import Value


class TestDatastore(object):
    @staticmethod
    def test_make_mutation_from_value_object(key):
        value = Value(30, exclude_from_indexes=True)
        properties = {'value': value}

        results = Datastore.make_mutation(Operation.INSERT, key, properties)

        assert results['insert']['properties']['value'] == value.to_repr()

    @staticmethod
    @pytest.fixture(scope='session')
    def key()       :
        path = PathElement(kind='my-kind', name='path-name')
        return Key(project='my-project', path=[path], namespace='my-namespace')
