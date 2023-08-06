import os, sys, shutil, subprocess

here = os.getcwd()
code = os.path.dirname(__file__)


class UnitTest:

    def setup_method(self, method):
        """create files and folders"""
        test = method.__name__
        os.mkdir(f'{code}/{test}')
        os.chdir(f'{code}/{test}')
        if test != 'test_lgr_3':

            # instantiate a cue ledger in the test dir
            subprocess.run(['cue', 'init'])
            subprocess.run(['cue', 'commit'])

        # if there's any sample data, copy it in
        try:
            shutil.copytree(f'{code}/sample_data/{test}',
                            f'{code}/{test}',
                            dirs_exist_ok=True)
        except OSError:
            pass

    def teardown_method(self, method):
        """delete files and folders"""
        test = method.__name__
        os.chdir(here)
        shutil.rmtree(f'{code}/{test}')

        # unload cue modules
        modules = list(sys.modules.keys())
        for m in modules:
            if m.startswith('cue'):
                del(sys.modules[m])
