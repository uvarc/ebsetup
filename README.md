# EasyBuild setup instructions

## Install new version

```bash
ml easybuild
eb --install-latest-eb-release --prefix /apps/software/EasyBuild/x.y.z
```

### Edit modulefile

Move `/apps/standard/core/EasyBuild/x.y.z.lua` to `/apps/modulefiles/easybuild`. Append:

```lua
-- CUSTOM FOR DEVEL
local appspath = '/apps'
local arch = 'standard'
prepend_path("PYTHONPATH", pathJoin(appspath,"ebscripts/easybuild/easyblocks"))

local user = os.getenv("USER")
setenv("EASYBUILD_BUILDPATH", pathJoin("/tmp",user))
setenv("EASYBUILD_INSTALLPATH", appspath)
setenv("EASYBUILD_SUBDIR_SOFTWARE", pathJoin("software", arch))
setenv("EASYBUILD_SUBDIR_MODULES", pathJoin("modulefiles", arch))
setenv("EASYBUILD_SUFFIX_MODULES_PATH", "")
setenv("EASYBUILD_MODULES_TOOL", "Lmod")
setenv("EASYBUILD_REPOSITORYPATH", pathJoin(appspath,"ebscripts/easybuild/easyconfigs"))
setenv("EASYBUILD_ROBOT_PATHS", pathJoin(appspath, "ebscripts/easybuild/easyconfigs"))
setenv("EASYBUILD_SOURCEPATH", "/share/resources/apps/source")
setenv("EASYBUILD_MODULE_SYNTAX", "Lua")
setenv("CONTAINERDIR", "/share/resources/containers/apptainer")

-- use custom module naming scheme
setenv("EASYBUILD_MODULE_NAMING_SCHEME", "RivannaHMNS")

-- add custom module classes
setenv("EASYBUILD_MODULECLASSES", "licensed,apptainer,containersystem")

-- set compiler optimization for  intel, gcc, and pgi compilers
setenv("EASYBUILD_DEFAULT_OPT_LEVEL", "opt")
setenv("EASYBUILD_OPTARCH", "intel:xavx -axCORE-AVX2,CORE-AVX512;gcc:march=sandybridge")

-- define hidden modules/dependencies
setenv("EASYBUILD_HIDE_DEPS", "automake,autoconf,binutils,bison,cairo-core,clibs,expat,flex,freetype-core,gcccore,glib,help2man,icc,ifort,iccifort,imkl,iompi,libassuan,libgcrypt,ibffi,libgtextutils,libiconv,libjpeg-turbo,libksba,libgpg-error,libpng,libreadline,libtiff,libtool,libxc,libxml2,m4,ncurses,netcdf-c,netcdf-cxx,netcdf-fortran,npth,pixman,pcre,protobuf,protobuf-python3,szip,tensorflowpkg3,x264,xz,zlib,X11")
setenv("EASYBUILD_HIDE_TOOLCHAINS", "gcccore,iompi")

-- default behavior in 4.x installs all modules as /apps/software/standard/MODULE/VERSION-[TOOLCHAIN-VERSION]
setenv("EASYBUILD_DISABLE_FIXED_INSTALLDIR_NAMING_SCHEME", "")

-- hooks
setenv("EASYBUILD_HOOKS", "/home/uvacse/ebhook/rivanna_hook.py")
```

## Hook

Copy `rivanna_hook.py` from this repo to `/home/uvacse/ebhook`.

## Module naming scheme

Copy `rivanna-hmns.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/tools/module_naming_scheme`. If the syntax has changed, start from `hierarchical_mns.py`:

- Change value of `CORE`/`COMPILER`/`MPI`/`TOOLCHAIN` to lowercase
- `TOOLCHAIN = toolchains`
- `class RivannaHMNS`
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

1. (Skip if copying `rivanna_hmns.py` from this repo.) In `lib/pythonX.Y/site-packages/easybuild/tools/module_naming_scheme/rivanna_hmns.py`:
    
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

1. Copy `container.py` from this repo to `lib/pythonX.Y/site-packages/easybuild/tools/toolchain`. (If syntax has changed, start from `toolchains/compiler/dummy.py`.)

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

Copy `mamba.py` to `lib/pythonX.Y/site-packages/easybuild/easyblocks/generic`.

# Citation

R. Sun and K. Siller, [HPC Container Management at the University of Virginia](https://doi.org/10.1145/3626203.3670568), PEARC '24: Practice and Experience in Advanced Research Computing 2024: Human Powered Computing 73, 1 (2024).
