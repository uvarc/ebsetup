def pre_module_hook(self):
    """add *_ROOT environment variable by default"""
    from easybuild.tools.filetools import convert_name
    self.cfg.update('modextravars', {'%s_ROOT' % convert_name(self.name, upper=True): self.installdir})

def module_write_hook(self, filepath, module_txt, *args, **kwargs):
    """URL is already taken care of by homepage. Preserve "Application class" in 3.9 for website shortcode."""
    import re
    search = r'whatis\(\[==\[URL:.*'
    replace = 'whatis([==[Application class: %s]==])' % self.cfg['moduleclass']
    return re.sub(search, replace, module_txt)
