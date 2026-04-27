from pythonforandroid.recipe import PyProjectRecipe


class VideoNativeRecipe(PyProjectRecipe):
    version = '1.0.0'
    url = 'https://github.com/Novfensec/VideoNative/archive/main.zip'
    name = 'videonative'
    hostpython_prerequisites = ['scikit-build-core', 'pybind11', 'cmake', 'ninja']
    depends = ['python3', 'ffmpeg']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        ffmpeg_recipe = self.get_recipe('ffmpeg', self.ctx)
        ffmpeg_build_dir = ffmpeg_recipe.get_build_dir(arch.arch)

        env['SKBUILD_CMAKE_ARGS'] = (
            f"-DANDROID_FFMPEG_INCLUDE={ffmpeg_build_dir}/include"
            f"-DANDROID_FFMPEG_LIB={ffmpeg_build_dir}/lib"
        )

        return env

recipe = VideoNativeRecipe()
