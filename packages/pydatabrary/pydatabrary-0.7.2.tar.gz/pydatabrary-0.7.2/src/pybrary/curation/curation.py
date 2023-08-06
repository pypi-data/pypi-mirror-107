import os
import warnings

from ..databrary.recordFactory import RecordFactory
from ..databrary.asset import Asset
from ..databrary.volume import Volume

from ..utils import utils
from ..databrary.container import Container
from ..databrary.types.category import Category
from ..api.pybrary import Pybrary


class Curation:
    @staticmethod
    def from_databrary(username, password, volume_id, superuser=False, check_errors=True):
        pb = Pybrary.get_instance(username, password, superuser)
        volume_data = pb.get_volume_info(volume_id)

        if check_errors:
            errors = Curation.check_errors(volume_data, volume_id)
            if errors:
                raise Exception('Errors in volume {}, Check {}'.format(volume_id, errors))
            else:
                print('No error found in volume {}'.format(volume_id))

        return Volume.from_databrary(volume_data)

    @staticmethod
    def check_errors(volume_data, volume_id):
        errors = dict()
        containers = volume_data.get('containers')
        for container in containers:
            container_id = container.get('id')
            for asset in container.get('assets'):
                asset_id = asset.get('id')
                if asset.get('name') is None:
                    error = 'Missing name for Asset {}: Please update the name here: https://nyu.databrary.org/volume/{}/slot/{}?asset={}'.format(asset_id, volume_id, container_id, asset_id)
                    if container_id in errors:
                        errors.get(container_id).append(error)
                    else:
                        errors[container_id] = [error]
        return errors

    @staticmethod
    def from_files(volume_name, containers_file, assets_file=None, records_file=None):
        if volume_name is None:
            raise AttributeError('You must provide a valid volume name.')
        else:
            name = volume_name

        if containers_file is None:
            raise AttributeError('Containers file is required')
        else:
            containers = Curation.read_containers_csv(containers_file)

        if assets_file is None:
            warnings.warn('Assets found in the containers file will be ignored. PLease provide an assets file')
        else:
            assets = Curation.read_assets_csv(assets_file)

        if records_file is None:
            warnings.warn('Records found in the containers file will be ignored. PLease provide a records file')
        else:
            records = Curation.read_records_csv(records_file)

        return Volume(name, containers, assets, records)

    @staticmethod
    def get_ingest_file(volume, output):
        if output is None:
            raise IOError('Please provide an output path')
        if utils.get_file_extension(output) != 'json':
            output = utils.replace_file_extension(output)
            warnings.warn('Ingest files must be in JSON format, ingest file will be saved in {}'
                          .format(output))

        utils.dump_into_json(volume.to_dict(), output)

    @staticmethod
    def get_files_from_volume(volume, dir_path):
        pass

    @staticmethod
    def generate_assets_list(folder, output=None):
        """
        Find all supported files in a folder (recursively) adds clips for video files.
        return the following structure
            [
                {
                    "release": null,
                    "position": "auto",
                    "name": "FILE_NAME,
                    "file": "FILE_PATH_IN_DATABRARY_STAGING_FOLDER"
                }
            ]
        :param output: dump assets list into a csv file
        :param folder: Folder path where to lookup for assets
        :return: a List of dict with supported assets found in folder
        """
        if not os.path.isdir(folder):
            raise IOError('{} is not a directory'.format(folder))

        print('Parsing {}'.format(os.path.abspath(folder)))
        assets = []
        for root, dirs, files in os.walk(folder):
            for idx, file in enumerate(files):
                try:
                    file_path = os.path.join(root, file)
                    assets.append(Asset(file_path, id=idx))
                except Exception as e:
                    warnings.warn('Error in file {} - '.format(file, e))

        if output is not None:
            Curation.dump_into_csv(assets, output, template=True)
            print('Assets printed in {}'.format(os.path.abspath(output)))

        return assets

    @staticmethod
    def generate_records_list(categories=None, output=None):
        records = []
        idx = 0

        for category, value in categories.items():
            if not Category.has_value(category):
                warnings.warn('Category {} is not valid, it will be ignored'.format(category))
                continue

            if int(value) < 1:
                warnings.warn('The value {} for {} is not valid, it must be > 0'.format(value, category))
                continue

            for i in range(value):
                records.append(
                    RecordFactory(
                        category=Category.get_name(category),
                        key=idx,
                        id=idx
                    )
                )
                idx = idx + 1

        if output is not None:
            Curation.dump_into_csv(records, output, template=True)
            print('Records printed in {}'.format(os.path.abspath(output)))

        return records

    @staticmethod
    def generate_containers_list(value=1, output=None):
        if int(value) < 1:
            raise Exception('The value {} is not valid, it must be > 0'.format(value))

        containers = []
        for i in range(value):
            containers.append(Container(key="{}".format(i)))

        if output is not None:
            Curation.dump_into_csv(containers, output, template=True)
            print('Containers printed in {}'.format(os.path.abspath(output)))

        return containers

    @staticmethod
    def dump_into_csv(data_list, output, template=False):
        result = []
        for data in data_list:
            try:
                result.append(data.to_dict(template=template))
            except Exception as e:
                print('Error {}'.format(e))

        utils.dump_into_csv(result, output)

    @staticmethod
    def read_records_csv(file_path):
        records_list = utils.read_csv(file_path)
        records = []
        ids = {}
        for record_dict in records_list:
            id = record_dict.get('key')
            if id in ids:
                warnings.warn('Found duplicate key {} in {}, the record {} will be ignored'
                              .format(id, file_path, record_dict.get('name')))
                continue
            ids[id] = None
            records.append(RecordFactory.from_dict(record_dict))

        return records

    @staticmethod
    def read_assets_csv(file_path):
        assets_list = utils.read_csv(file_path)
        assets = []
        ids = {}
        for asset_dict in assets_list:
            id = asset_dict.get('id')
            if id in ids:
                warnings.warn('Found duplicate id {} in {}, the asset {} will be ignored'
                              .format(id, file_path, asset_dict.get('name')))
                continue
            ids[id] = None
            asset = Asset.from_dict(asset_dict)
            assets.append(asset)

        return assets

    @staticmethod
    def read_containers_csv(file_path):
        containers_list = utils.read_csv(file_path)
        containers = []
        ids = {}
        for container_dict in containers_list:
            id = container_dict.get('key')
            if id in ids:
                warnings.warn('Found duplicate key {} in {}, the container {} will be ignored'
                              .format(id, file_path, container_dict.get('name')))
                continue
            ids[id] = None
            container = Container.from_dict(container_dict)
            containers.append(container)

        return containers

    @staticmethod
    def generate_sql_query(source, target):
        """
        Generate Databrary DB query that
        :param source: Original Volume ID
        :param target: Target Volume ID
        :return:
        """
        return "COPY (" \
               "select 'mkdir -p /nyu/stage/reda/' || '" + str(source) + "' || '/' || sa.container || ' && ' || E'cp \"/nyu/store/' || substr(cast(sha1 as varchar(80)), 3, 2) || '/' || right(cast(sha1 as varchar(80)), -4) || '\" \"' || '/nyu/stage/reda/' || '" + str(source) + "' || '/' || sa.container || '/' || CASE WHEN a.name LIKE '%.___' IS FALSE THEN a.name || '.' || f.extension[1] || '\"' ELSE a.name || '\"' END from slot_asset sa inner join asset a on sa.asset = a.id inner join format f on a.format = f.id where a.volume = " + str(source) + ") TO '/tmp/volume_" + str(target) + ".sh';"
