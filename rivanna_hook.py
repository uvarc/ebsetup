def pre_module_hook(self):
    from easybuild.tools.filetools import convert_name
    self.cfg.update('modextravars', {'%s_ROOT' % convert_name(self.name, upper=True): self.installdir})
