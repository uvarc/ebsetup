def pre_module_hook(self):
    """add *_ROOT environment variable
    the first character of an env var cannot be a digit
    """
    from easybuild.tools.filetools import convert_name
    if self.name[0].isdigit():
        name = '_' + self.name
    else:
        name = self.name
    self.cfg.update('modextravars', {'%s_ROOT' % convert_name(name, upper=True): self.installdir})

def module_write_hook(self, filepath, module_txt, *args, **kwargs):
    """URL is already taken care of by homepage. Preserve "Application class" in 3.9 for website shortcode."""
    import re
    search = r'whatis\(\[==\[URL:.*'
    replace = 'whatis([==[Application class: %s]==])' % self.cfg['moduleclass']
    return re.sub(search, replace, module_txt)
