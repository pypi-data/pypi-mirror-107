import os, sys, shutil

here = os.getcwd()
code = os.path.dirname(__file__)


class UnitTest:

    def setup_method(self, method):
        """create files and folders"""
        test = method.__name__
        shutil.copytree(f'{code}/sample_data/{test}', f'{code}/{test}')
        os.chdir(f'{code}/{test}')

    def teardown_method(self, method):
        """delete files and folders"""
        os.chdir(here)
        shutil.rmtree(f'{code}/{method.__name__}')

        # unload cue modules
        modules = list(sys.modules.keys())
        for m in modules:
            if m.startswith('cue'):
                del(sys.modules[m])
