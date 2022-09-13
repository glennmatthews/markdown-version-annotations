"""Tasks for use with Invoke."""
from invoke import task


def run_cmd(context, exec_cmd):
    """Run an Invoke task command.

    Args:
        context (invoke.task): Invoke task object.
        exec_cmd (str): Command to run.

    Returns:
        result (obj): Contains Invoke result from running task.
    """
    print(f"Running command {exec_cmd}")
    return context.run(exec_cmd, pty=True)


@task
def black(context):
    """Run black to check that Python files are consistently formatted."""
    exec_cmd = "black --check --diff ."
    run_cmd(context, exec_cmd)


@task
def flake8(context):
    """Run flake8 code analysis."""
    exec_cmd = "flake8 ."
    run_cmd(context, exec_cmd)


@task
def pylint(context):
    """Run pylint code static analysis."""
    exec_cmd = 'find . -name "*.py" | xargs pylint'
    run_cmd(context, exec_cmd)


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting adheres to standards."""
    exec_cmd = "pydocstyle ."
    run_cmd(context, exec_cmd)


@task
def bandit(context):
    """Run bandit to validate basic static code security analysis."""
    exec_cmd = "bandit --recursive ./ --configfile pyproject.toml"
    run_cmd(context, exec_cmd)


@task
def tests(context):
    """Run all linters and tests for this repository."""
    black(context)
    flake8(context)
    pylint(context)
    pydocstyle(context)
    bandit(context)

    print("All checks have passed!")
