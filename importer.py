from mb_editor import *

import os, shutil


def run_import(source_dir, mb_home_dir):
    mission_dest_dir = mb_home_dir + "/data/missions_pq/custom"

    print("copying missions from '{}' to '{}', creating directories if necessary".format(source_dir, mission_dest_dir))
    os.makedirs(mission_dest_dir, mode=0o777, exist_ok=True)

    interiors = []

    for root_dir, dirs, basenames in os.walk(source_dir):
        for mission_source_basename in basenames:
            if mission_source_basename.endswith(".mis"):
                mission_source_path = os.path.join(root_dir, mission_source_basename)
                mission_dest_path = os.path.join(mission_dest_dir, mission_source_basename)

                print("\ncopying mission '{}' to '{}'".format(mission_source_path, mission_dest_path))
                shutil.copyfile(mission_source_path, mission_dest_path)

                picture_basename = mission_source_basename.replace(".mis", ".png")
                picture_source_path = os.path.join(root_dir, picture_basename)
                picture_dest_path = os.path.join(mission_dest_dir, picture_basename)

                if os.path.exists(picture_source_path):
                    print("copying associated mission image '{}' to '{}'".format(picture_source_path, picture_dest_path))
                    shutil.copyfile(picture_source_path, picture_dest_path)
                else:
                    print("associated mission image '{}' not found".format(picture_source_path))

                print("scanning mission '{}' for interior references".format(mission_source_basename))
                mission = Mission.from_file(mission_source_path)
                for interior in mission.descendants():
                    if isinstance(interior, Interior) and interior.interiorFile not in [i.interiorFile for i in interiors]:
                        print("found reference to interior at source path '{}'".format(interior.interiorFile))
                        interiors.append(interior)

    print("\nsearching for interiors")
    for root_dir, dirs, basenames in os.walk(source_dir):
        for interior_source_basename in basenames:
            if interior_source_basename.endswith(".dif"):
                interior_source_path = os.path.join(root_dir, interior_source_basename)

                for interior in interiors:
                    interior_dest_path = interior.interiorFile.replace("~", mb_home_dir)
                    interior_dest_dir = os.path.dirname(interior_dest_path)
                    interior_dest_basename = os.path.basename(interior_dest_path)

                    if interior_source_basename == interior_dest_basename:
                        print("copying interior '{}' to '{}', creating directories if necessary".format(interior_source_path, interior_dest_path))
                        os.makedirs(interior_dest_dir, mode=0o777, exist_ok=True)
                        shutil.copyfile(interior_source_path, interior_dest_path)


def tests():
    run_import(source_dir="data", mb_home_dir="mb_home_dir")


if __name__ == '__main__':
    tests()
