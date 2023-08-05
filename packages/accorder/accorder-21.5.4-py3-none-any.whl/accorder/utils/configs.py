import os
import click
import configparser
import collections
import pathlib
import uuid


def read_config(app_name):
    cfg = pathlib.Path(click.get_app_dir(app_name)).joinpath("accorder.ini")

    if not pathlib.Path(cfg).exists():
        pathlib.Path(click.get_app_dir(app_name)).mkdir(parents=True, exist_ok=True)
        with open(cfg, "w") as f:
            f.write("[_calibre]\nfoo = bar\n")

    parser = configparser.ConfigParser()
    parser.read(cfg)
    nested_dict = lambda: collections.defaultdict(nested_dict)
    conf = nested_dict()
    for section in parser.sections():
        profile, context = section.split("_")
        for key, value in parser.items(section):
            conf[profile][context][key] = value
    return conf


def write_config(app_name, options):
    cfg = os.path.join(click.get_app_dir(app_name), "accorder.ini")
    if not pathlib.Path(cfg).exists():
        os.makedirs(click.get_app_dir(app_name), exist_ok=True)

    parser = configparser.ConfigParser()
    parser.read(cfg)
    for option in options:
        parser.remove_section("_calibre")
        if not parser.has_section(option["section"]):
            parser.add_section(option["section"])
        parser.set(option["section"], option["option"], option["value"])
    with open(cfg, "w") as f:
        parser.write(f)


def check_sections(config, profile):
    return [
        section
        for section in ["meta", "calibre", "motw", "rsync", "tunnel", "rclone"]
        if section in config[profile].keys()
    ]


def edit_config(app_name, profile, directory=None, librarian=None, bibtex=None):
    config = read_config(app_name)

    if not directory:
        if "local_directory" in config[profile]["calibre"]:
            directory = config[profile]["calibre"]["local_directory"]
        else:
            click.echo(
                f"A local Calibre's collection directory for {profile} is missing. HINT: Use `-d` flag."
            )
            click.get_current_context().exit()

    if directory[:-1] != "/":
        directory += "/"

    while "/" * 2 in directory:
        directory = directory.replace("//", "/")

    if not pathlib.Path(f"{ directory}metadata.db").is_file() and not bibtex:
        click.echo(
            f"{ directory} provided does not point to the root of Calibre library. Please, check again and provide the correct path."
        )
        click.get_current_context().exit()

    new_sections = [
        {
            "section": f"{profile}_calibre",
            "option": "local_directory",
            "value": directory,
        }
    ]

    if not librarian:
        if "librarian" in config[profile]["calibre"]:
            librarian = config[profile]["calibre"]["librarian"]
        else:
            click.echo(
                f"A librarian name (max 40 chars) for {profile} is missing. HINT: Use `-l` flag."
            )
            click.get_current_context().exit()

    new_sections.append(
        {
            "section": f"{profile}_calibre",
            "option": "librarian",
            "value": librarian[:48],
        }
    )

    if "library_uuid" not in config[profile]["calibre"]:
        new_sections.append(
            {
                "section": f"{profile}_calibre",
                "option": "library_uuid",
                "value": str(uuid.uuid4()),
            }
        )

    if "library_secret" not in config[profile]["calibre"]:
        new_sections.append(
            {
                "section": f"{profile}_calibre",
                "option": "library_secret",
                "value": uuid.uuid4().hex,
            }
        )

    write_config(app_name, new_sections)

    return read_config(app_name)
