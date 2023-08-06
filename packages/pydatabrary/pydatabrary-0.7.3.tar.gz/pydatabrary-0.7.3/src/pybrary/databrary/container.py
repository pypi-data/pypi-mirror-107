import json
import warnings

from .. import constants

from .recordFactory import RecordFactory
from .record import Record
from .participant import Participant
from .asset import Asset
from .types.release import Release


class Container:
    def __init__(
            self,
            id,
            key,
            name=None,
            date=None,
            top=False,
            release=Release.PRIVATE,
            assets=dict(),
            records=dict(),
    ):
        """
        :param id: 
        :param key: 
        :param name: 
        :param date: 
        :param top: 
        :param release:
        :param assets: A hasmap of asset objects <Asset ID, Asset Object>
        :param records: A hashmap of record object<Record ID, Record Object>
        """
        if id is None:
            raise Exception('A valid id is required for containers')

        self._id = id
        self._key = key
        self._top = top
        self._name = "Container {}".format(key) if name is None else name
        self._assets = assets
        self._records = records
        self._release = release
        self._date = date

    def get_key(self) -> int:
        return self._key

    def get_id(self) -> int:
        return self._id

    def get_assets(self) -> {int, Asset}:
        return self._assets

    def set_assets(self, assets):
        """
        Set a hashmap of assets <Asset id, Asset Obj> to this container
        :param assets:
        :return:
        """
        self._assets = assets

    def get_records(self):
        return self._records

    def set_records(self, records):
        self._records = records

    def add_asset(self, asset):
        """
        Add an Asset Object to the asset hashmap
        :param asset:
        :return:
        """

        id = int(asset.get('id'))
        if id in self._assets:
            raise Exception('Asset id {} already exists in container {}'.format(id, self._id))

        self._assets[id] = asset

    def add_record(self, record):
        """
        Add a Record object to the records hashmap
        :param record:
        :return:
        """
        id = int(record.get('id'))
        if id in self._records:
            raise Exception('Record id {} already exists in container {}'.format(id, self._id))

        self._records[id]= record

    def get_name(self):
        return self._name

    def set_name(self, value):
        if value is None:
            raise Exception('You must provide a valid name for container {}'.format(self._id))

        self._name = value

    def set_release(self, release):
        self._release = release

    def get_asset(self, asset_id):
        return self._assets.get(asset_id)

    def get_record(self, record_id) -> Record:
        return self._records.get(record_id)

    def get_top(self) -> bool:
        return self._top

    def get_release(self) -> Release:
        return self._release

    def get_date(self) -> str:
        return self._date

    def get_participants_list(self) -> [Participant]:
        return list(filter(lambda record: isinstance(record, Participant),self._records.values()))

    def get_participant(self, participant_id) -> Participant:
        for participant in self.get_participants_list():
            if participant.get_participant_id() == participant_id:
                return participant

        return None

    def remove_participant(self, participant_id):
        participant = self.get_participant(participant_id)
        if participant is not None:
            self._records.pop(participant.get_id(), None)

    @staticmethod
    def from_dict(container_dict):
        id = container_dict.get('id')
        name = container_dict.get('name')
        assets = json.loads(container_dict.get('assets'))
        records = json.loads(container_dict.get('records'))
        release = Release[container_dict.get('release')]
        date = container_dict.get('date')
        top = container_dict.get('top')

        return Container(
            key=id,
            id=id,
            name=name,
            release=release,
            top=top,
            date=date,
            assets=assets,
            records=records
        )

    @staticmethod
    def from_databrary(container_dict):
        id = container_dict.get('id')
        date = container_dict.get('date')
        top = container_dict.get('top') is not None
        name = container_dict.get('name')

        records = dict()
        for record_dict in container_dict.get('records'):
            record_id = record_dict.get('id')
            try:
                records[record_id] = RecordFactory.from_databrary(record_dict)
            except Exception as e:
                warnings.warn('Container {} Error: {}'.format(id, e))

        assets = dict()
        for asset_dict in container_dict.get('assets'):
            asset_id = asset_dict.get('id')
            try:
                path_prefix = "{}{}/".format(constants.DEFAULT_SERVER_PREFIX, id)
                assets[asset_id] = Asset.from_databrary(asset_dict, path_prefix)
            except Exception as e:
                warnings.warn('Container {} Error: {}'.format(id, e))

        return Container(
            key=id,
            id=id,
            name=name,
            top=top,
            date=date,
            assets=assets,
            records=records
        )

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "top": self.get_top(),
            "name": self.get_name(),
            "release": self.get_release().value,
        }

        if template:
            result['assets'] = []
            result['records'] = []
        else:
            result['assets'] = list(map(lambda asset: asset.to_dict(), list(self.get_assets().values())))
            result['records'] = list(map(lambda record: record.to_dict(), list(self.get_records().values())))

        if self.get_date() is not None:
            result['date'] = self.get_date()

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

