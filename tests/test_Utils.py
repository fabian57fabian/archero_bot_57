import os
import shutil
from unittest import TestCase

from Utils import getCoordFilePath


class Test(TestCase):
    def setUp(self) -> None:
        self.test_datas_dir = "datas"
        if not os.path.exists(self.test_datas_dir):
            os.mkdir(self.test_datas_dir)

    def tearDown(self) -> None:
        if os.path.exists(self.test_datas_dir):
            shutil.rmtree(self.test_datas_dir)

    def test_getCoordFilePath_size(self):
        res_path = getCoordFilePath("buttons.json", size=(1080, 1920))
        expect_path = "datas/1080x1920/coords/buttons.json"
        assert os.path.normpath(expect_path) == os.path.normpath(res_path), "got wrong path"

    def test_getCoordFilePath_sizePath(self):
        res_path = getCoordFilePath("buttons.json", sizePath="1080x1920")
        expect_path = "datas/1080x1920/coords/buttons.json"
        assert os.path.normpath(expect_path) == os.path.normpath(res_path), "got wrong path"
