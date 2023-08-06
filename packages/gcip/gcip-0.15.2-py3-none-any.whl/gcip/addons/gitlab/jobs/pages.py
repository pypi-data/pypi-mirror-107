import os

from gcip.core.job import Job
from gcip.addons.python import job_scripts as scripts
from gcip.core.variables import PredefinedVariables


def _gitlab_pages_path(subpath: str) -> str:
    """
    Ensures `subpath` is a subpath under `./public`.

    Args:
        subpath (str): Any path string is allowed, with or without leading slash.

    Returns:
        str: The path string `public/<subpath>`
    """
    if subpath != "":
        subpath = os.path.normpath(subpath)

        if os.path.isabs(subpath):
            subpath = subpath[1:]

    return os.path.join("public", subpath)


def asciidoctor(
    source: str,
    out_file: str,
    job_name: str = "asciidoctor-pages",
    job_stage: str = "build",
) -> Job:
    """
    Translate the AsciiDoc source FILE as Gitlab Pages HTML5 file.

    Runs `asciidoctor {source} -o public{out_file}`and stores the output
    as artifact under the `public` directory.

    Args:
        source (str): [description]
        out_file (str): [description]

    Returns:
        Job: [description]
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script=[
            "gem install asciidoctor",
            f"asciidoctor {source} -o {_gitlab_pages_path(out_file)}",
        ],
    )
    job.set_image("ruby:3-alpine")
    job.artifacts.add_paths("public")
    return job


def sphinx(job_name: str = "sphinx-pages", job_stage: str = "build") -> Job:
    """
    Runs `sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}` and installs project requirements
    before (`scripts.pip_install_requirements()`)

    * Requires a `docs/requirements.txt` in your project folder` containing at least `sphinx`
    * Creates it artifacts for Gitlab Pages under `pages`
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script=[
            scripts.pip_install_requirements("docs/requirements.txt"),
            f"sphinx-build -b html -E -a docs {_gitlab_pages_path(PredefinedVariables.CI_COMMIT_REF_SLUG)}",
        ],
    )
    job.artifacts.add_paths("public")
    return job


def pdoc3(
    module: str,
    *,
    output_path: str = "",
    job_name: str = "pdoc3-pages",
    job_stage: str = "build",
) -> Job:
    """Generate a HTML API documentation of you python code as Gitlab Pages.

    Runs `pdoc3 --html -f --skip-errors --output-dir public{path} {module}` and stores the output
    as artifact under the `public` directory.

    Args:
        module (str): The Python module name. This may be an import path resolvable in the current environment, or a file path to a Python module or package.
        output_path (str, optional): A sub path of the Gitlab Pages `public` directory to output generated HTML/markdown files to. Defaults to "/".

    Returns:
        Job: The Gitlab CI job generating Gitlab Pages with pdoc3.
    """
    job = Job(
        name=job_name,
        stage=job_stage,
        script=[
            "pip3 install pdoc3",
            f"pdoc3 --html -f --skip-errors --output-dir {_gitlab_pages_path(output_path)} {module}",
        ],
    )
    job.artifacts.add_paths("public")
    return job
