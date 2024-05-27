import os
import json
import shutil
import logging
import zipfile
import tempfile
import urllib.request
import distutils.dir_util


from rez.system import system
from rez.package_maker import make_package
try:
    from rez.version import Version
except:
    # Fallback for older rez versions
    from rez.vendor.version.version import Version


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def create_python_package(packages_path, python_version=None):
    """Download python package from nuget package gallery, extract portable python
    build and release as rez package. If no desired version is specified, detect
    the latest (non-pre-release) version and release that.
    
    The function creates a temporary folder but tries to clean up after itself.
    """
    if not python_version:
        log.info("No python version specified, getting latest available version")
        python_versions = "https://api.nuget.org/v3-flatcontainer/python/index.json"
        with urllib.request.urlopen(python_versions) as response:
            python_version = (next(i for i in reversed(json.loads(response.read())["versions"]) if not "-" in i))
        log.info(f"Latest python version detected:{ python_version }")

    download_url = f"https://www.nuget.org/api/v2/package/python/{ python_version }"


    temp_folder = tempfile.mkdtemp(prefix="rezpy-")
    filename = os.path.join(temp_folder, f"python.{ python_version }.zip")
    
    log.info("Downloading python from nuget gallery")
    urllib.request.urlretrieve(download_url, filename)

    try:
        log.info("Extracting python from nuget package")
        with zipfile.ZipFile(filename) as archive:
            python_source_folder = os.path.join(temp_folder, "python")
            for file in archive.namelist():
                if file.startswith("tools/"):
                    archive.extract(file, python_source_folder)


        def make_root(variant, path):
            distutils.dir_util.copy_tree(os.path.join(python_source_folder, "tools"), path)

        log.info(f"Creating python pacckages in { packages_path }")
        with make_package("python", packages_path, make_root=make_root, warn_on_skip=False) as pkg:
            pkg.version = python_version
            pkg.description = "Python programming language"
            pkg.authors = ["Python Software Foundation"]
            pkg.uuid = "8c94dcaa-404f-44c7-9ede-25fbb932b98d"
            pkg.homepage = "http://www.python.org"
            pkg.variants = [["platform-windows", "arch-AMD64"]]
            pkg.commands = """import os
env.PATH.append(this.root)
env.PATH.append(os.path.join(this.root, "DLLs"))
"""

        if pkg.skipped_variants:
            log.warning(f"Variants skipped: { ','.join(variant.qualified_package_name for variant in pkg.skipped_variants) }")

    except urllib.error.HTTPError as e:
        log.error(f"Python version not found (tried URL { download_url })")
    except Exception as e:
        raise e

    finally:
        log.info("Removing temporary folder -> " + temp_folder)
        shutil.rmtree(temp_folder)


def create_platform_package(packages_path):
    """Create a rez package for the current platform"""
    version = Version(system.platform)

    log.info(f"Installing platform-{ version }")
    with make_package("platform", packages_path, warn_on_skip=False) as pkg:
        pkg.version = version

    if pkg.skipped_variants:
        log.warning(f"Variants skipped: { ','.join(variant.qualified_package_name for variant in pkg.skipped_variants) }")

    return pkg.installed_variants

def create_arch_package(packages_path):
    """Create a rez package for the current system architecture"""
    version = Version(system.arch)
    
    log.info(f"Installing arch-{ version }")
    with make_package("arch", packages_path, warn_on_skip=False) as pkg:
        pkg.version = version

    if pkg.skipped_variants:
        log.warning(f"Variants skipped: { ','.join(variant.qualified_package_name for variant in pkg.skipped_variants) }")

    return pkg.installed_variants

def create_os_package(packages_path):
    """Create a rez package for the current os"""
    version = Version(system.os)

    log.info(f"Installing os-{ version }")
    with make_package("os", packages_path, warn_on_skip=False) as pkg:
        pkg.version = version
        pkg.requires = [
            "platform-%s" % system.platform,
            "arch-%s" % system.arch
        ]

    if pkg.skipped_variants:
        log.warning(f"Variants skipped: { ','.join(variant.qualified_package_name for variant in pkg.skipped_variants) }")

    return pkg.installed_variants


if __name__ == "__main__":
    # For testing only
    packages_path=r"c:\temp\rez_quickstart"
    create_platform_package(packages_path)
    create_arch_package(packages_path)
    create_os_package(packages_path)
    create_python_package(packages_path)