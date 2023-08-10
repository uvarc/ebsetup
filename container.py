from easybuild.toolchains.compiler.dummycompiler import DummyCompiler

CONTAINER_FAMILY = 'CONTAINER'

class Container(DummyCompiler):
    """Dummy toolchain."""
    TOOLCHAIN_FAMILY = CONTAINER_FAMILY
