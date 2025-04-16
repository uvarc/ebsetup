# EasyBuild setup instructions

## Install new version

```bash
ml easybuild
eb --install-latest-eb-release --prefix /apps/software/EasyBuild/x.y.z
```

### Configuration

Move `/apps/standard/core/EasyBuild/x.y.z.lua` to `/apps/modulefiles/easybuild`. Append:
```lua
setenv("CONTAINERDIR", "/share/resources/containers/apptainer")
```

Create `~/.config/easybuild` if it does not already exist and copy `config.cfg`. A blank file can be generated via
```bash
eb --confighelp > $HOME/.config/easybuild/config.cfg
```
To see just the uncommented lines of the config file:
```bash
$ grep ^[^#] ~/.config/easybuild/config.cfg 
[MAIN]
[basic]
repositorypath=/apps/ebscripts/easybuild/easyconfigs
robot-paths=%(repositorypath)s:%(DEFAULT_ROBOT_PATHS)s
[config]
buildpath=/tmp/uvacse
hooks=/home/uvacse/ebhook/rivanna_hook.py
installpath=/apps
module-naming-scheme=SSZ_HMNS
sourcepath=/share/resources/apps/source
subdir-modules=modulefiles/standard
subdir-software=software/standard
suffix-modules-path=
[container]
[easyconfig]
[github]
[informative]
[job]
[override]
default-opt-level=opt
fixed-installdir-naming-scheme=False
optarch=intel:-march=skylake;GCC:-march=skylake;NVHPC:-tp=px
[package]
[regtest]
[software]
[unittest]
```

## Hook

Copy `rivanna_hook.py` from this repo to `/home/uvacse/ebhook`.

## Module naming scheme

Copy `ssz_hmns.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/tools/module_naming_scheme`. If the syntax has changed, start from `hierarchical_mns.py`:

- Change value of `CORE`/`COMPILER`/`MPI`/`TOOLCHAIN` to lowercase
- `TOOLCHAIN = toolchains`
- `class SSZ_HMNS`
- `det_short_module_name`: (Pseudocode) `return ec['name'].lower() if not 'R'`
- `det_module_subdir`: `return subdir.lower()`

```python
if tc_comps is None:
    # no compiler in toolchain, system toolchain => Core module
    self.log.debug('ec.toolchain.TOOLCHAIN_FAMILY=%s', ec.toolchain.TOOLCHAIN_FAMILY)
    if ec['moduleclass'] == 'toolchain':
        subdir = TOOLCHAIN
    else:
        subdir = CORE
```

- `det_modpath_extensions`: Add `.lower()` to all names; `excluded_comps = ['GCC', 'NVHPC', 'intel']`

- Add `is_short_modname_for` from `mns.py`. Add `.lower()` to `name` and `short_modname`.

## Container toolchain

1. In `lib/pythonX.Y/site-packages/easybuild/tools/module_naming_scheme/toolchain.py`:

    ```python
    from easybuild.tools.toolchain.container import CONTAINER_FAMILY
    ...
    if ec.toolchain.is_system_toolchain() or ec.toolchain.name == 'apptainer':
    ```

1. (Skip if copying `ssz_hmns.py` from this repo.) In `lib/pythonX.Y/site-packages/easybuild/tools/module_naming_scheme/ssz_hmns.py`:
    
    ```python
    CONTAINER = 'container'
    CONTAINER_TOOLCHAINS = ['apptainer']
    MODULECLASS_CONTAINER = 'containersystem'

    # Under det_module_subdir:
            if tc_comps is None:
                ...
                elif ec.toolchain.TOOLCHAIN_FAMILY == 'CONTAINER':
                    subdir = os.path.join(CONTAINER, ec.toolchain.name, ec.toolchain.version)
    ```

1. Copy `container.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/tools/toolchain`. (If syntax has changed, start from `toolchains/compiler/systemcompiler.py`.)

1. Copy `apptainer.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/toolchains`.

1. In `lib/pythonX.Y/site-packages/easybuild/tools/toolchain/toolchain.py`:
    
    ```python
    def prepare(self...
    ...
    #                                    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            if self.is_system_toolchain() or self.name == 'apptainer':

                # define minimal build environment when using system toolchain;
                # this is mostly done to try controlling which compiler commands are being used,
                # cfr. https://github.com/easybuilders/easybuild-framework/issues/3398
                self.set_minimal_build_env()
    ```

1. Copy `apptainerimage.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/easyblocks/a`. (If syntax has changed, compare with `lib/pythonX.Y/site-packages/easybuild/easyblocks/generic/binary.py`.)

## Custom Easyblocks

(Optional) In `lib/pythonX.Y/site-packages/easybuild/easyblocks/generic/conda.py` add `or get_software_root('miniforge')` for the `conda_cmd = 'mamba'` case.

# Citation

R. Sun and K. Siller, HPC Container Management at the University of Virginia, PEARC '24: Practice and Experience in Advanced Research Computing 2024: Human Powered Computing 73, 1 (2024). [doi:10.1145/3626203.3670568](https://doi.org/10.1145/3626203.3670568)
