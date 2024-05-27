"""
Entrypoint for CLI.
"""
import click
from rez.config import config
import packages


@click.command()
@click.option(
    "--release",
    "-r",
    is_flag=True,
    help="Release to release path instead of local path",
)
@click.option(
    "--packages_path", "-p", help="Release to custom path, overrides --release"
)
@click.option(
    "--python_version",
    help="Release specific version (latest if not set)",
)
def cli(release, packages_path, python_version):
    if not packages_path:
        packages_path = (
            config.release_packages_path if release else config.local_packages_path
        )
    
    packages.create_platform_package(packages_path)
    packages.create_arch_package(packages_path)
    packages.create_os_package(packages_path)
    packages.create_python_package(packages_path, python_version=python_version)

if __name__=="__main__":
    cli()