#!/usr/bin/env python3

from argparse import ArgumentParser
import os

from copr.v3 import Client


def _get_argument_kws(env_name):
    if env_name in os.environ:
        kws = {"default": os.environ[env_name]}
    else:
        kws = {"required": True}

    return kws


def parse_arguments():
    parser = ArgumentParser(prog="copr_trigger", description="Trigger a build on COPR")

    parser.add_argument(
        "--copr-url", type=str, default="https://copr.fedorainfracloud.org", help="The base URL of COPR"
    )
    parser.add_argument(
        "-l",
        "--login",
        type=str,
        help="The login name (overrides $CT_LOGIN)",
        **_get_argument_kws("CT_LOGIN"),
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="The login token (overrides $CT_TOKEN)",
        **_get_argument_kws("CT_TOKEN"),
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="The username on COPR (overrides $CT_USERNAME)",
        **_get_argument_kws("CT_USERNAME"),
    )
    parser.add_argument(
        "--owner",
        type=str,
        help="The name of the project owner (overrides $CT_OWNER)",
        **_get_argument_kws("CT_OWNER"),
    )
    parser.add_argument(
        "--project",
        type=str,
        help="The name of the project (overrides $CT_PROJECT)",
        **_get_argument_kws("CT_PROJECT"),
    )
    parser.add_argument(
        "--package",
        type=str,
        help="The name of the package (overrides $CT_PACKAGE)",
        **_get_argument_kws("CT_PACKAGE"),
    )
    parser.add_argument("--version", type=str, required=True, help="The version of the PyPI package")

    args = parser.parse_args()

    return args


def trigger_build(args):
    config = {
        "copr_url": args.copr_url,
        "login": args.login,
        "token": args.token,
        "username": args.username,
    }
    client = Client(config)

    print(f"Changing version of the package to {args.version}...")
    source_dict = {
        "pypi_package_name": args.package,
        "pypi_package_version": args.version,
        "spec_template": "fedora",
        "python_versions": [3],
    }
    client.package_proxy.edit(args.owner, args.project, args.package, source_type="pypi", source_dict=source_dict)

    print("Scheduling new build...")
    client.package_proxy.build(args.owner, args.project, args.package)


def main():
    args = parse_arguments()

    trigger_build(args)


if __name__ == "__main__":
    main()
