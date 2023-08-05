"""Utilities for converting observation data to alternative formats"""
from copy import deepcopy
from glob import glob
from logging import getLogger
from os import makedirs
from os.path import basename, dirname, expanduser
from typing import List, Sequence, Union

from flatten_dict import flatten
from pyinaturalist.constants import ResponseObject, ResponseOrObject
from pyinaturalist.models import Observation  # noqa
from requests import Response
from tablib import Dataset

# from pyinaturalist.formatters import simplify_observations
AnyObservation = Union[Dataset, Observation, Response, ResponseOrObject]
logger = getLogger(__name__)


# TODO: Handle Obervation model objects
# TODO: Handle reuqests.Respose objects
# TODO: Handle tablib.Dataset objects
def ensure_list(obj: AnyObservation) -> List:
    if isinstance(obj, dict) and 'results' in obj:
        obj = obj['results']
    if isinstance(obj, Sequence):
        return list(obj)
    else:
        return [obj]


def to_csv(observations: ResponseOrObject, filename: str = None) -> str:
    """Convert observations to CSV"""
    csv_observations = to_dataset(observations).get_csv()
    if filename:
        _write(csv_observations, filename)
    return csv_observations


def to_dataframe(observations: ResponseOrObject):
    """Convert observations into a pandas DataFrame"""
    import pandas as pd

    return pd.json_normalize(simplify_observations(observations))


def to_dataset(observations: ResponseOrObject) -> Dataset:
    """Convert observations to a generic tabular dataset. This can be converted to any of the
    `formats supported by tablib <https://tablib.readthedocs.io/en/stable/formats>`_.
    """
    flat_observations = [flatten(obs, reducer='dot') for obs in simplify_observations(observations)]
    dataset = Dataset()
    headers, flat_observations = _fix_dimensions(flat_observations)
    dataset.headers = headers
    dataset.extend([item.values() for item in flat_observations])
    return dataset


def to_excel(observations: ResponseOrObject, filename: str = None) -> bytes:
    """Convert observations to an Excel spreadsheet (xlsx)"""
    xlsx_observations = to_dataset(observations).get_xlsx()
    if filename:
        _write(xlsx_observations, filename, 'wb')
    return xlsx_observations


def to_parquet(observations: ResponseOrObject, filename: str):
    """Convert observations into a parquet file"""
    df = to_dataframe(observations)
    df.to_parquet(filename)


def simplify_observations(
    observations: ResponseOrObject, align: bool = False
) -> List[ResponseObject]:
    """Flatten out some nested data structures within observation records:

    * annotations
    * comments
    * identifications
    * non-owner IDs
    """
    return [_simplify_observation(o) for o in ensure_list(observations)]


def _simplify_observation(obs):
    # Reduce annotations to IDs and values
    obs = deepcopy(obs)
    obs['annotations'] = [
        {str(a['controlled_attribute_id']): a['controlled_value_id']} for a in obs['annotations']
    ]

    # Reduce identifications to just a list of identification IDs and taxon IDs
    # TODO: Better condensed format that still works with parquet
    obs['identifications'] = [{str(i['id']): i['taxon_id']} for i in obs['identifications']]
    obs['non_owner_ids'] = [{str(i['id']): i['taxon_id']} for i in obs['non_owner_ids']]

    # Reduce comments to usernames and comment text
    obs['comments'] = [{c['user']['login']: c['body']} for c in obs['comments']]
    del obs['observation_photos']

    return obs


# TODO: Do this with tablib instead of pandas?
# OR: use pandas if installed, otherwise fallback to tablib?
def load_exports(*file_paths: str):
    """Combine multiple CSV files (from iNat export tool) into one, and return as a dataframe"""
    import pandas as pd

    resolved_paths = resolve_file_paths(*file_paths)
    logger.info(
        f'Reading {len(resolved_paths)} exports:\n'
        + '\n'.join([f'\t{basename(f)}' for f in resolved_paths])
    )

    df = pd.concat((pd.read_csv(f) for f in resolved_paths), ignore_index=True)
    return df


def resolve_file_paths(*file_paths: str) -> List[str]:
    """Given file paths and/or glob patterns, return a list of resolved file paths"""
    resolved_paths = [p for p in file_paths if '*' not in p]
    for path in [p for p in file_paths if '*' in p]:
        resolved_paths.extend(glob(path))
    return [expanduser(p) for p in resolved_paths]


def _fix_dimensions(flat_observations):
    """Temporary ugly hack to work around missing fields in some observations"""
    # TODO: Use Observation model to get headers instead?
    optional_fields = ['taxon.complete_rank', 'taxon.preferred_common_name']
    headers = set(flat_observations[0].keys()) | set(optional_fields)
    for obs in flat_observations:
        for field in optional_fields:
            obs.setdefault(field, None)
    return headers, flat_observations


def _write(content, filename, mode='w'):
    """Write converted observation data to a file, creating parent dirs first"""
    filename = expanduser(filename)
    logger.info(f'Writing to {filename}')
    if dirname(filename):
        makedirs(dirname(filename), exist_ok=True)
    with open(filename, mode) as f:
        f.write(content)
