import os
import shutil
import zipfile

import sys
import traceback

from amble.mission import Mission
from amble.utils import path


def install(source_zip, mission_dest_dir):
    if not source_zip.endswith('.zip'):
        return

    yield 'Extracting zip...'

    source_dir = path.platinum('_climb_export')
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)

    with zipfile.ZipFile(source_zip, 'r') as f:
        f.extractall(source_dir)

    yield ' done.\n\n'

    os.makedirs(mission_dest_dir, mode=0o777, exist_ok=True)

    mission_source_paths = []
    num_bad_missions = 0
    asset_dest_paths = set()

    for root_dir, _, basenames in os.walk(source_dir):
        for source_basename in basenames:
            if source_basename.startswith('._'):
                continue

            if source_basename.endswith('.mis'):
                mission_source_path = path.join(root_dir, source_basename)
                mission_source_paths.append(mission_source_path)

                if len(mission_source_paths) == 1:
                    yield 'Installed mission(s):\n\n'

                try:
                    mission = Mission.from_file(mission_source_path)
                    yield '"{}" ({})\n'.format(
                        mission.info.name,
                        path.relative(mission_dest_dir, source_basename)
                    )
                except Exception as e:
                    _, _, e_traceback = sys.exc_info()
                    num_bad_missions += 1
                    yield (
                        '\nError parsing mission "{}":\n'.format(source_basename) +
                        '\n'.join(traceback.format_tb(
                            e_traceback)) +
                        '\n{}: {}'.format(
                            e.__class__.__name__, e.args[0]) +
                        '\nSend this text to @hPerks#5581 on Discord for help!\n\n'
                    )
                    continue

                asset_dest_paths.add(path.platinum(mission.sky.materialList))
                if 'music' in mission.info.fields.dict:
                    asset_dest_paths.add(path.platinum('data/sound/music', mission.info.music))

                for descendant in mission.descendants():
                    if 'interiorFile' in descendant.fields.dict:
                        asset_dest_paths.add(path.platinum(descendant.interiorFile))
                    elif 'shapeName' in descendant.fields.dict:
                        asset_dest_paths.add(path.platinum(descendant.shapeName))

    if len(mission_source_paths) == 0:
        yield 'No missions found. :(\n'
    yield '\n'

    for mission_source_path in mission_source_paths:
        shutil.copy(mission_source_path, mission_dest_dir)

        for extension in ['.png', '.jpg', '.prev.png']:
            if os.path.exists(mission_source_path.replace('.mis', extension)):
                shutil.copy(mission_source_path.replace('.mis', extension), mission_dest_dir)

    matched_asset_paths = []

    for root_dir, _, basenames in os.walk(source_dir):
        for asset_source_basename in basenames:
            asset_source_path = path.join(root_dir, asset_source_basename)

            for asset_dest_path in asset_dest_paths:
                asset_dest_dir = os.path.dirname(asset_dest_path)
                asset_dest_basename = os.path.basename(asset_dest_path)

                if asset_source_basename == asset_dest_basename:
                    os.makedirs(asset_dest_dir, mode=0o777, exist_ok=True)
                    shutil.copyfile(asset_source_path, asset_dest_path)

                    asset_dest_paths.remove(asset_dest_path)
                    matched_asset_paths.append(asset_dest_path)

                    if len(matched_asset_paths) == 1:
                        yield 'Asset(s) included:\n\n'

                    yield '{}/{}\n'.format(
                        path.relative(asset_dest_dir),
                        asset_source_basename
                    )

                    for texture_basename in os.listdir(root_dir):
                        if texture_basename.endswith('.png') or texture_basename.endswith('.jpg'):
                            with open(asset_source_path, errors='ignore') as f:
                                if texture_basename[:-4] in f.read():
                                    texture_source_path = path.join(root_dir, texture_basename)
                                    texture_dest_path = path.join(asset_dest_dir, texture_basename)

                                    if not texture_dest_path in matched_asset_paths:
                                        shutil.copyfile(texture_source_path, texture_dest_path)

                                        matched_asset_paths.append(texture_dest_path)

                                        yield '{}/{}\n'.format(
                                            path.relative(asset_dest_dir),
                                            texture_basename
                                        )
                    break

    if len(matched_asset_paths) == 0:
        yield 'No assets included.\n'

    num_missing_assets = 0
    for asset_dest_path in asset_dest_paths:
        if asset_dest_path not in matched_asset_paths:
            if not os.path.exists(asset_dest_path):
                if num_missing_assets == 0:
                    yield '\nMissing asset(s):\n'
                num_missing_assets += 1
                yield '{}/{}\n'.format(
                    os.path.dirname(path.relative(asset_dest_path)),
                    os.path.basename(asset_dest_path)
                )

    shutil.rmtree(source_dir)

    yield '\nSuccessfully installed {} mission(s)'.format(len(mission_source_paths) - num_bad_missions) + (
        ''
        if num_bad_missions == 0
        else ' ({} invalid)'.format(num_bad_missions)
    ) + ' with {} asset(s)'.format(len(matched_asset_paths)) + (
        ''
        if num_missing_assets == 0
        else ' ({} missing)'.format(num_missing_assets)
    )
