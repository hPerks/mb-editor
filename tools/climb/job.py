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
        shutil.rmtree(source_dir, ignore_errors=True)

    with zipfile.ZipFile(source_zip, 'r') as f:
        f.extractall(source_dir)

    yield ' done.\n\n'

    os.makedirs(mission_dest_dir, mode=0o777, exist_ok=True)

    mission_source_paths = []
    num_bad_missions = 0
    asset_dest_paths = set()

    for dir, _, basenames in os.walk(source_dir):
        for source_basename in basenames:
            if source_basename.startswith('._'):
                continue

            if source_basename.endswith('.mis'):
                mission_source_path = path.join(dir, source_basename)
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

    for dir, _, basenames in os.walk(source_dir):
        for asset_source_basename in basenames:
            asset_source_path = path.join(dir, asset_source_basename)

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

                    with open(asset_source_path, errors='ignore') as f:
                        asset_contents = f.read()

                    for texture_basename in os.listdir(dir):
                        if texture_basename.endswith('.png') or texture_basename.endswith('.jpg'):
                            if texture_basename[:-4] in asset_contents:
                                texture_source_path = path.join(dir, texture_basename)
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

    shutil.rmtree(source_dir, ignore_errors=True)

    yield '\nSuccessfully installed {} mission(s)'.format(len(mission_source_paths) - num_bad_missions) + (
        ''
        if num_bad_missions == 0
        else ' ({} invalid)'.format(num_bad_missions)
    ) + ' with {} asset(s)'.format(len(matched_asset_paths)) + (
        ''
        if num_missing_assets == 0
        else ' ({} missing)'.format(num_missing_assets)
    )


def bundle(mission_file, dest_dir):
    temp_dir = path.platinum('_climb_export')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    os.makedirs(path.join(temp_dir, 'data/missions/custom'), mode=0o777, exist_ok=True)

    try:
        mission = Mission.from_file(mission_file)
        yield 'Successfully parsed mission "{}"\n\n'.format(mission.info.name)
    except Exception as e:
        _, _, e_traceback = sys.exc_info()
        yield (
            '\nError parsing mission:\n' +
            '\n'.join(traceback.format_tb(
                e_traceback)) +
            '\n{}: {}'.format(
                e.__class__.__name__, e.args[0]) +
            '\nSend this text to @hPerks#5581 on Discord for help!'
        )
        return

    shutil.copyfile(mission_file, path.join(temp_dir, 'data/missions/custom', os.path.basename(mission_file)))

    def bundle_asset(asset_source_path):
        if asset_source_path.endswith('/') or not os.path.exists(asset_source_path):
            return ''

        asset_dest_path = path.join(temp_dir, path.relative(asset_source_path)[2:])

        os.makedirs(os.path.dirname(asset_dest_path), mode=0o777, exist_ok=True)
        shutil.copyfile(asset_source_path, asset_dest_path)

        bundled_assets.add(asset_source_path)
        return '{}\n'.format(path.relative(asset_source_path))

    yield 'Bundled asset(s):\n'
    bundled_assets = set()

    for descendant in mission.descendants():
        for attr in ['materialList', 'interiorFile', 'shapeName']:
            if attr in descendant.fields.dict:
                value = descendant.fields.get(attr)
                if path.platinum(value) not in bundled_assets:
                    asset_source_path = path.platinum(value)
                    yield bundle_asset(asset_source_path)

                    with open(asset_source_path, errors='ignore') as f:
                        asset_contents = f.read()

                    asset_source_dir = os.path.dirname(asset_source_path)
                    for texture_basename in os.listdir(asset_source_dir):
                        if texture_basename.endswith('.png') or texture_basename.endswith('.jpg'):
                            if texture_basename[:-4] in asset_contents:
                                texture_path = path.join(asset_source_dir, texture_basename)
                                if texture_path not in bundled_assets:
                                    yield bundle_asset(texture_path)

    if 'music' in mission.info.fields.dict:
        yield bundle_asset(path.platinum('data/sound/music/' + mission.info.music))

    with open(path.join(temp_dir, 'readme.txt'), 'w') as f:
        f.write(
            'Thanks for downloading {}! To install, merge the "data" folder with the one in your PQ home folder - '
            'or use CLIMB, the Custom Level Installer for Marble Blast, by going to tinyurl.com/getclimb.'.format(mission.info.name)
        )

    zip_name = mission.info.name.replace(':', '')
    yield '\nArchiving to "{}.zip"... '.format(path.join(dest_dir, zip_name))
    shutil.make_archive(path.join(dest_dir, zip_name), 'zip', path.join(temp_dir))
    shutil.rmtree(temp_dir, ignore_errors=True)
    yield 'done!'
