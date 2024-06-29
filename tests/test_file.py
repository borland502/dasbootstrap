import os
import shutil
import tempfile
import unittest
from pathlib import Path
from utils.file import pack, unpack
from faker import Faker

class TestFileUtil(unittest.TestCase):
    # "faker.providers"
    faker_provider_names: list[str] = ["lorem.en_US", "file", "misc"]
    faker_providers: list[str] = ["faker.providers." + p for p in faker_provider_names]

    def setUp(self):
        self.fake: Faker = Faker(["en_US"], providers=self.faker_providers)

        with (tempfile.TemporaryDirectory(delete=False) as tmp_src_dir):
            self.src_dir = Path(tmp_src_dir)
            for _ in range(20):
                tmp_file: Path = Path.joinpath(self.src_dir, self.fake.file_path(absolute=False))
                tmp_file.parent.mkdir(parents=True, exist_ok=True)
                tmp_file.write_text(
                    self.fake.text(max_nb_chars=200), encoding="utf-8"
                )

    def test_pack_default(self):
        pack(src_dir=self.src_dir, out_file=f"{self.src_dir}.zst")
        self.assertTrue(Path(f"{self.src_dir}.zst").exists())
        self.assertFalse(Path(f"{self.src_dir}.tar").exists())
        self.assertGreater(Path(f"{self.src_dir}.zst").stat().st_size, 0)

    def test_unpack_default(self):
        self.test_pack_default()
        with (tempfile.TemporaryDirectory(delete=False) as tmp_src_dir):
            unpack(f"{self.src_dir}.zst", tmp_src_dir)
            out_dir = Path.joinpath(Path(tmp_src_dir), self.src_dir)
            self.assertTrue(out_dir.exists())
            self.assertTrue(out_dir.is_dir())
            self.assertEqual(20, len(os.listdir(out_dir)))

    def tearDown(self):
        shutil.rmtree(path=self.src_dir)
