import logging
import click
from rez.config import config
from . import packages


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


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
    if packages_path:
        log.info(f"Using provided packages path: { packages_path }")

    if not packages_path:
        packages_path = (
            config.release_packages_path if release else config.local_packages_path
        )
    
    if release:
        log.info(f"Using release packages path: { packages_path }")
    else:
        log.info(f"Using local packages path: { packages_path }")
    
    
    packages.create_platform_package(packages_path)
    packages.create_arch_package(packages_path)
    packages.create_os_package(packages_path)
    packages.create_python_package(packages_path, python_version=python_version)

if __name__=="__main__":
    cli()