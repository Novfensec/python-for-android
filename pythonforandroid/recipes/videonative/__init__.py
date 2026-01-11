# your_app/pythonforandroid/recipes/libvideo/__init__.py
from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import shprint
from pythonforandroid.toolchain import current_directory
import sh
import os

class VideoNativeRecipe(Recipe):
    #name = 'libvideo'
    version = '0.1'
    src_filename = 'libvideo.c'
    # We compile a single C file into a shared library
    # No Python sources to install; we’ll load via ctypes.
    depends = ['ffmpeg']  # ensure ffmpeg recipe is built before this
    # If you use a custom ffmpeg recipe name, update this dependency.

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        # Include and lib paths from the ffmpeg recipe
        ffmpeg_recipe = self.get_recipe('ffmpeg')
        ffmpeg_build_dir = ffmpeg_recipe.get_build_dir(arch)
        ffmpeg_lib_dir = os.path.join(ffmpeg_build_dir, 'lib')
        ffmpeg_inc_dir = os.path.join(ffmpeg_build_dir, 'include')

        # Common FFmpeg libs
        env['CFLAGS'] = f"{env.get('CFLAGS','')} -I{ffmpeg_inc_dir}"
        env['LDFLAGS'] = f"{env.get('LDFLAGS','')} -L{ffmpeg_lib_dir}"
        env['LIBS'] = ' -lavformat -lavcodec -lavutil -lswscale'

        # Android NDK flags
        env['CFLAGS'] += ' -fPIC'
        env['LDFLAGS'] += ' -shared'

        return env

    def build_arch(self, arch):
        # Compile libvideo.c into libvideo.so
        build_dir = self.get_build_dir(arch)
        src = os.path.join(build_dir, 'libvideo.c')
        out = os.path.join(build_dir, 'libvideo.so')

        env = self.get_recipe_env(arch)
        cc = sh.Command(self.ctx.ndk.cc(arch))

        with current_directory(build_dir):
            shprint(cc,
                    '-o', out,
                    src,
                    env['CFLAGS'],
                    env['LDFLAGS'] + env['LIBS'])

        # Install into libs dir so it’s packaged with the APK
        dest_dir = self.ctx.get_libs_dir(arch)
        shprint(sh.cp, out, dest_dir)

recipe = VideoNativeRecipe()
