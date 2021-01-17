__doc__ = """OpenTimelineIO Kdenlive Collection Folder Adapter"""

import os

import opentimelineio as otio


def write_to_file(input_otio, filepath):
    error_suffix = "Needs to be a folder or not exist: {}".format(filepath)
    if os.path.isfile(filepath):
        raise OSError(
            "Path is a file. {}".format(error_suffix)
        )
    if os.path.islink(filepath) and not os.path.exists(filepath):
        raise OSError(
            "Path is a broken symlink. {}".format(error_suffix)
        )
    if os.path.exists(filepath) and not os.path.isdir(filepath):
        raise OSError(
            "Path exists, but isn't a folder. {}".format(error_suffix)
        )

    if not os.path.exists(filepath):
        os.mkdir(filepath)

    if isinstance(input_otio, otio.schema.SerializableCollection):
        collection = input_otio
    else:
        collection = [input_otio]

    for timeline in collection:
        _replace_stacks(timeline)
        path = os.path.join(
            filepath, "{}.kdenlive".format(timeline.name)
        )
        otio.adapters.write_to_file(timeline, path, "kdenlive")


def write_to_string(input_otio):
    raise NotImplementedError(
        "Can only generate multiple files in a given folder. "
        "Only implementing write_to_file."
    )


def _replace_stacks(timeline):
    for stack in timeline.each_child(
            descended_from_type=otio.schema.Stack
    ):
        track = stack.parent()
        clip = otio.schema.Clip(
            media_reference=otio.schema.ExternalReference(
                target_url="{}.kdenlive".format(stack.name),
                available_range=stack.available_range(),
            ),
            source_range=stack.source_range,
        )
        idx = track.index(stack)
        track.remove(stack)
        track.insert(idx, clip)
