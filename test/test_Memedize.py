import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.memedize.module_memedize import module_memedize
from gdotest.TestUtil import cli_plug, reinstall_module, cli_gizmore, GDOTestCase, WebPlug, install_module, web_plug


class module_memedize_Test(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        install_module('memedize')
        loader.load_modules_db(True)
        WebPlug.COOKIES = {}
        Application.init_cli()
        loader.init_modules(True, True)
        loader.init_cli()

    def test_00_reinstall(self):
        reinstall_module('memedize')
        self.assertIs(type(module_memedize.instance()), module_memedize, "Cannot re-install module memedize.")

    def test_03_overview_cli(self):
        giz =  cli_gizmore()
        out = cli_plug(giz, "$Memedize.overview")
        self.assertIn('/memedize.overview.html', out)
        self.assertNotIn('<img', out)

    def test_02_overview_web(self):
        out = web_plug("memedize.overview.html?_lang=en").exec()
        self.assertIn('Welcome to more MayMay!', out)
        self.assertIn('href="/gdo/memedize/memes/2023-09-23/01_sawtooth_tiger.png"', out)
        self.assertIn('Browse directory', out)
        self.assertIn('<img', out)
        self.assertNotIn('sessions.zip', out)
        image = web_plug('gdo/memedize/memes/2023-09-23/01_sawtooth_tiger.png').exec()
        self.assertTrue(isinstance(image, bytes) and image.startswith(b'\x89PNG\r\n\x1a\n'))
        image = web_plug('gdo/memedize/memes/2023-09-23/02_H%C3%A4nsel_und_Gretel__undRobin.png').exec()
        self.assertTrue(isinstance(image, bytes) and image.startswith(b'\x89PNG\r\n\x1a\n'))


if __name__ == '__main__':
    unittest.main()
