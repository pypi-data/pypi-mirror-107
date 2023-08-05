import functools
import os
import pathlib
import shutil

import invoke


@invoke.task
def node_install(ctx):
    """
    Install node and npm in current virtual env if
    the node env is not installed
    """
    active_venv = os.environ.get('VIRTUAL_ENV', None)
    which = functools.partial(
        shutil.which,
        path=pathlib.Path(active_venv) / 'bin',
    )
    shim_path = active_venv and which('shim')
    nodeenv_path = active_venv and which('nodeenv')

    # if python virtual env is active (active_venv)
    # and nodeenv package is installed (nodeenv_path),
    # but nodeenv is not initialized in active virtual env (shim_path)
    # (not relevant for github actions because virtual env is absent)
    if active_venv and nodeenv_path and not shim_path:
        ctx.run('nodeenv -p')


@invoke.task(node_install, iterable=['packages'])
def npm_install(ctx, packages=None):
    packages = ('-g', *packages) if packages else ()
    ctx.run(' '.join(('npm', 'install', '--no-save', *packages)))
