from pythonforandroid.recipe import PyProjectRecipe


class VispyRecipe(PyProjectRecipe):
    name = "vispy"
    version = "0.15.2"
    url = 'https://github.com/vispy/vispy/archive/refs/tags//v{version}.tar.gz'
    site_packages_name = "vispy"
    call_hostpython_via_targetpython = False
    install_in_hostpython = False
    install_in_targetpython = True
    depends = ['numpy', 'freetype-py', 'hsluv', 'kiwisolver', 'packaging', 'PySDL2']
    hostpython_prerequisites = ['setuptools>=64', 'wheel', 'Cython', 'numpy', 'build']
    patches = ['disable_freetype.patch',
               'disable_font_triage.patch',
               'vispy_egl_backend.patch']


recipe = VispyRecipe()
