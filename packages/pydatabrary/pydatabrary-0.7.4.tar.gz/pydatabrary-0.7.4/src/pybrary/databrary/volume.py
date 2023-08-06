import warnings
import json

from jsonschema import validate, ValidationError

from .recordFactory import RecordFactory
from .asset import Asset
from .container import Container
from .. import constants


class Volume:
    """
    A volume is a set is a set of containers(aka Session), assets and record, A container might point to
    assets and records attached to it.
    The volume class is in charge to fetch the correct asset and record from assets and records list respectively
    and generate an ingest dictionary to be processed by the Curation class
    """
    default_schema_file = constants.VOLUME_SCHEMA_FILE
    default_server_path = '/nyu/stage/ingest/'

    def __init__(self, volume_name, containers=dict()):
        """
        Create and instance of a Databrary volume
        :param volume_name: Volume's name | Required
        :param containers: A hashmap of container <Container Id, container obj>
        """
        if volume_name is None or len(volume_name) < 1:
            raise AttributeError('You must provide a valid volume name.')
        else:
            self._name = volume_name

        if containers is None:
            raise AttributeError('Containers are required')
        else:
            self._containers = containers

    @staticmethod
    def from_databrary(volume_dict):
        """
        Parse Volume dictionary and populate containers, assets and records (if Any)
        The method will link assets and records to the appropriate container as well
        :param volume_dict: Volume's JSON file
        :return:
        """
        containers = dict()
        records = dict()

        name = volume_dict.get('name')

        # Databrary volume have records in a separate list
        # the record id is referenced in the container records list
        # We need to fetch records before creating our list of containers
        for record_dict in volume_dict.get('records'):
            record_id = record_dict.get('id')
            if record_id is not None:
                records[record_id] = record_dict


        for container_dict in volume_dict.get('containers'):
            container_records = []

            for container_record in container_dict.get('records'):
                record_id = container_record.get('id')
                record_dict = records.get(record_id)
                if record_dict is None:
                    warnings.warn("Cannot find record {} id in the volume's records list".format(record_id))
                else:
                    container_records.append(record_dict)

            container_dict['records'] = container_records
            try:
                container = Container.from_databrary(container_dict)
                containers[container.get_id()] = container
            except Exception as e:
                warnings.warn("Volume {} Error: {}".format(name, e))

        return Volume(
            volume_name=name,
            containers=containers
        )

    def get_containers(self):
        return self._containers

    def get_container(self, container_id):
        return self._containers.get(container_id)

    def get_volume_assets_list(self):
        # TODO:
        pass

    def get_volume_records_list(self):
        # TODO:
        pass

    def get_volume_participants_list(self):
        # TODO:
        pass

    def remove_participant(self, participant_id):
        container = self.get_container_of_particpant(participant_id)
        container.remove_

    def remove_container(self, container_id):
        self._containers.pop(container_id, None)

    def get_name(self):
        return self._name

    def to_dict(self):
        result = {
            "name": self.get_name(),
        }

        containers = list(map(lambda container: container.to_dict(), list(self._containers.values())))
        result['containers'] =  containers
        Volume.validate(result)

        return result

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    @staticmethod
    def validate(volume_data, schema_file=default_schema_file):
        with open(schema_file) as f:
            schema = json.loads(f.read())
        try:
            validate(volume_data, schema)
        except ValidationError as e:
            raise Exception('Did not pass validation against volume.json schema - Errors: {}'.format(e))

    def get_container_of_record(self, record_id):
        for container in self._containers.values():
            if record_id in container.get_records():
                return container

        return None

    def get_container_of_particpant(self, particpant_id):
        for container in self._containers.values():
            if container.get_participant(particpant_id) is not None:
                return container

        return None

    def get_container_of_asset(self, asset_id):
        for container in self._containers.values():
            if record_id in container.get_assets():
                return container

        return None

    def get_asset(self, asset_id):
        for container in self._containers.values():
            asset = container.get_assets().get(asset_id)
            if asset is not None:
                return asset

        return None

    def get_record(self, record_id):
        for container in self._containers.values():
            record = container.get_records().get(record_id)
            if record is not None:
                return record

        return None

