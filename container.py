from easybuild.toolchains.compiler.systemcompiler import SystemCompiler

CONTAINER_FAMILY = 'CONTAINER'

class Container(SystemCompiler):
    """Dummy toolchain."""
    TOOLCHAIN_FAMILY = CONTAINER_FAMILY
