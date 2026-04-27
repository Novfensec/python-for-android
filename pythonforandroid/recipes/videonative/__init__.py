from os.path import join
from pythonforandroid.recipe import PyProjectRecipe

class VideoNativeRecipe(PyProjectRecipe):

    version = '1.0.0'
    url = 'https://github.com/Novfensec/VideoNative/archive/main.zip'
    name = 'videonative'
    site_packages_name = 'videonative'
    hostpython_prerequisites = ['scikit-build-core', 'pybind11', 'cmake', 'ninja']
    depends = ['python3', 'ffmpeg']

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)

        ffmpeg_recipe = self.get_recipe('ffmpeg', self.ctx)
        ffmpeg_build_dir = ffmpeg_recipe.get_build_dir(arch.arch)

        env['SKBUILD_STRICT_CONFIG'] = 'false'

        toolchain_file = join(self.ctx.ndk_dir, 'build', 'cmake', 'android.toolchain.cmake')

        env['SKBUILD_CMAKE_ARGS'] = (
            f"-DCMAKE_TOOLCHAIN_FILE={toolchain_file};"
            f"-DANDROID_ABI={arch.arch};"
            f"-DANDROID_PLATFORM=android-{self.ctx.ndk_api};"
            f"-DANDROID_FFMPEG_INCLUDE={join(ffmpeg_build_dir, 'include')};"
            f"-DANDROID_FFMPEG_LIB={join(ffmpeg_build_dir, 'lib')};"
        )

        return env

recipe = VideoNativeRecipe()
