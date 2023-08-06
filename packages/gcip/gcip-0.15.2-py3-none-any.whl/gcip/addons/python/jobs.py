from typing import Union, Optional

from gcip.lib import rules
from gcip.core.job import Job
from gcip.core.image import Image
from gcip.addons.container.images import PredefinedImages

from . import job_scripts as scripts

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


def flake8(job_name: str = "flake8", job_stage: str = "lint") -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade flake8
    flake8
    ```
    """
    return Job(
        name=job_name,
        stage=job_stage,
        script=[
            "pip3 install --upgrade flake8",
            "flake8",
        ],
    )


def mypy(
    package_dir: str,
    job_name: str = "mypy",
    job_stage: str = "lint",
) -> Job:
    """Runs:

    ```python
    pip3 install --upgrade mypy
    mypy package_dir
    ```

    Args:
        package_dir (str): Relativ path to package which should be checked with mypy.

    Returns:
        Job: Job running mypy.
    """
    return Job(
        name=job_name,
        stage=job_stage,
        script=["pip3 install --upgrade mypy", f"mypy {package_dir}"],
    )


def isort(job_name: str = "isort", job_stage: str = "lint") -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade isort
    isort --check .
    ```
    """
    return Job(
        name=job_name,
        stage=job_stage,
        script=[
            "pip3 install --upgrade isort",
            "isort --check .",
        ],
    )


def pytest(job_name: str = "pytest", job_stage: str = "test") -> Job:
    """
    Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `pytest`
    """
    return Job(
        name=job_name,
        stage=job_stage,
        script=[
            scripts.pip_install_requirements(),
            "pytest",
        ],
    )


def evaluate_git_tag_pep440_conformity(job_name: str = "tag-pep440-conformity", job_stage: str = "test", image: Optional[Union[Image, str]] = None) -> Job:
    """
    Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
    https://www.python.org/dev/peps/pep-0440

    This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script="python3 -m gcip.tools.evaluate_git_tag_pep440_conformity",
    )
    job.append_rules(rules.on_tags())
    if image:
        job.set_image(image)
    else:
        job.set_image(PredefinedImages.GCIP)

    return job


def bdist_wheel(job_name: str = "bdist_wheel", job_stage: str = "build") -> Job:
    """
    Runs `python3 setup.py bdist_wheel` and installs project requirements
    before (`scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `setuptools`
    * Creates artifacts under the path `dist/`
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script=[
            scripts.pip_install_requirements(),
            "python3 setup.py bdist_wheel",
        ],
    )
    job.artifacts.add_paths("dist/")
    return job


def twine_upload(
    twine_repository_url: Optional[str] = None,
    twine_username_env_var: Optional[str] = "TWINE_USERNAME",
    twine_password_env_var: Optional[str] = "TWINE_PASSWORD",
    job_name: str = "twine",
    job_stage: str = "deploy",
) -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade twine
    python3 -m twine upload --non-interactive --disable-progress-bar dist/*
    ```

    * Requires artifacts from a build job under `dist/` (e.g. from `bdist_wheel()`)

    Args:
        twine_repository_url (str): The URL to the PyPI repository the python artifacts will be deployed to. Defaults
            to `None`, which means the package is published to `https://pypi.org`.
        twine_username_env_var (Optional[str]): The name of the environment variable, which contains the username value.
            **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_USERNAME`.
        twine_password_env_var (Optional[str]): The name of the environment variable, which contains the password.
            **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_PASSWORD`.
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script=[
            "pip3 install --upgrade twine",
            "python3 -m twine upload --non-interactive --disable-progress-bar dist/*",
        ],
    )
    job.add_variables(
        TWINE_USERNAME=f"${twine_username_env_var}",
        TWINE_PASSWORD=f"${twine_password_env_var}",
    )

    if twine_repository_url:
        job.add_variables(TWINE_REPOSITORY_URL=twine_repository_url)

    return job
