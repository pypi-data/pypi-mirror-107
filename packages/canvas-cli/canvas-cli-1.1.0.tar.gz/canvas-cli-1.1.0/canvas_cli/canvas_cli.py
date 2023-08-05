#!/usr/bin/env python

import glob
import importlib.util
import json

from os.path import basename, exists, join
from pathlib import Path
from typing import Any, cast, Dict, List, TypedDict, Union

import arrow
import click
import requests

from canvas_workflow_sdk.patient import Patient
from canvas_workflow_sdk.serializers.protocol import ProtocolSerializer
from canvas_workflow_sdk.timeframe import Timeframe

from stringcase import camelcase
from tini import Tini

mocks_path = 'TODO'


def get_settings_path() -> Path:
    return Path.home() / '.canvas' / 'config.ini'


def read_settings() -> Dict[str, Any]:
    settings = Tini(filenames=[get_settings_path()])

    if not settings.items or not settings.items['canvas_cli']:
        raise click.ClickException(
            f'Please add your configuration at "{get_settings_path()}"; you can set '
            'defaults using `canvas-cli create-default-settings`.')

    if not settings.canvas_cli['url']:
        raise click.ClickException(f'Ensure that "url" is specified in "{get_settings_path()}".')

    if not settings.canvas_cli['api-key']:
        raise click.ClickException(f'Ensure that "api-key" is specified in "{get_settings_path()}".')

    return cast(Dict[str, Any], settings.canvas_cli)


class PatientData(TypedDict):
    billingLineItems: List
    conditions: List
    imagingReports: List
    immunizations: List
    instructions: List
    interviews: List
    labReports: List
    medications: List
    referralReports: List
    vitalSigns: List
    patient: Dict[str, Any]
    protocolOverrides: List
    changeTypes: List
    protocols: List


def load_patient(fixture_folder: Path) -> Patient:
    data: PatientData = {
        'billingLineItems': [],
        'conditions': [],
        'imagingReports': [],
        'immunizations': [],
        'instructions': [],
        'interviews': [],
        'labReports': [],
        'medications': [],
        'referralReports': [],
        'vitalSigns': [],
        'patient': {},
        'protocolOverrides': [],
        'changeTypes': [],
        'protocols': [],
    }

    file_loaded = False

    for filepath in fixture_folder.glob('*.json'):
        file_loaded = True

        filename = str(basename(filepath))
        field = camelcase(filename.split('.')[0])

        with open(filepath, 'r') as file:
            if field not in data:
                raise click.ClickException(
                    f'Found file that does not match a known field: "{field}"')

            data[field] = json.load(file)  # type: ignore

    if not file_loaded:
        raise click.ClickException(f'No JSON files were found in "{fixture_folder}"')

    data['patient']['key'] = fixture_folder.name

    # click.echo(json.dumps(data, indent=2))

    return Patient(data)


# def load_patient_data(patient_key: str, field: str) -> List:
#     """
#     Load data from mock data JSON files dumped by the dump_patient command.
#     """
#     filename = f'{mocks_path}/{patient_key}/{field}.json'

#     if not exists(filename):
#         if field == 'patient':
#             raise Exception(f'Missing mock patient data for "{patient_key}"!')

#         return []

#     with open(filename, 'r') as file:
#         return json.load(file)  # type: ignore


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['settings'] = read_settings()


@cli.command()
def create_default_settings():
    settings_path = get_settings_path()
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    click.echo(f'Writing default settings to "{settings_path}"...')

    settings_path.write_text('''[canvas_cli]
url =
api-key =
''')


@cli.command()
@click.argument('patient-key')
@click.argument('fixture-name')
@click.pass_context
def fixture_from_patient(ctx, patient_key: str, fixture_folder: str):
    click.echo(f'Getting fixture from patient "{patient_key}"...')

    response = requests.get(f'{ctx.obj["settings"]["url"]}/patient/{patient_key}/protocol-fixture/')
    response.raise_for_status()
    response_json = response.json()


def green(string: str) -> str:
    return click.style(string, fg='green')


@cli.command()
@click.argument('module-name')
@click.argument('class-name')
@click.argument('fixture-folder')
@click.option('--date')
def test_fixture(module_name: str, class_name: str, fixture_folder: str, date: str = None):
    module_path = Path(module_name)
    module_and_class = f'{module_path.stem}.{class_name}'

    click.echo(f'Executing "{green(module_and_class)}" with fixture "{green(fixture_folder)}"...')

    # 1. load module to test
    spec = importlib.util.spec_from_file_location(basename(module_name), module_name)

    if not spec:
        raise click.ClickException(f'Unable to load "{module_name}".')

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)  # type: ignore

    Class = getattr(module, class_name)

    # 2. load JSON folder of fixture data
    patient = load_patient(Path(fixture_folder))

    # if date:
    #     date = arrow.get(date)
    # else:
    #     date = arrow.now()  # utc?

    start = arrow.get('2017-10-23 13:24:56')
    end = arrow.get('2018-08-23 13:24:56')
    date = arrow.get('2018-08-23 13:24:56')

    timeframe = Timeframe(start=start, end=end)

    # 3. instantiate module
    protocol = Class(patient=patient, date=date, timeframe=timeframe)
    results = protocol.compute_results()

    serialized = ProtocolSerializer(protocol).data

    # 4. return results
    click.echo('\nOutput:\n')
    click.echo(json.dumps(serialized, indent=2))


@cli.command()
def upload():
    click.echo('Uploading...')


@cli.command()
@click.argument('module-name')
@click.argument('version')
def set_active(module_name: str, version: str):
    click.echo(f'Setting version "{version}" of "{module_name}" as active...')


if __name__ == '__main__':
    cli()
