import unittest
import patchutils

class TestPatchMerger(unittest.TestCase):
    def test_adding_removing(self):
        patch2 = {
            "files_removed": ["abc1.txt"],
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        removal_test(self, "abc1.txt", p)
        
    
    def test_plain_removing(self):
        patch2 = {
            "files_removed": ["abc4.txt"]
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertIn("abc4.txt", p['files_removed'])
        self.assertNotIn("abc4.txt", p['hash'])
    
    def test_modify_removing(self):
        patch2 = {
            "files_removed": ["abc3.txt"]
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertNotIn("abc3.txt", p['files_modified'])
        self.assertIn("abc3.txt", p["files_removed"])
        self.assertNotIn("abc3.txt", p['hash'])
    
    def test_remove_adding(self):
        patch2 = {
            "files_added": ["abc2.txt"],
            "hash": {"abc2.txt": "hash.abc2.txt.added"}
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertIn("abc2.txt", p["files_modified"])
        self.assertNotIn("abc2.txt", p['files_removed'])
        self.assertIn("abc2.txt", p["hash"])
    
    def test_plain_adding(self):
        patch2 = {
            "files_added": ["abc4.txt"],
            "hash": {"abc4.txt": "plain.added.abc4.txt.hash"}
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertIn("abc4.txt", p['files_added'])
        self.assertIn("abc4.txt", p['hash'])
    
    def test_add_modify(self):
        patch2 = {
            "files_modified": ["abc1.txt"],
            "hash": {"abc1.txt": "add.modify.abc1.txt.hash"}
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertIn("abc1.txt", p['files_added'])
        self.assertIn("abc1.txt", p["hash"])
        self.assertNotIn("abc1.txt", p["files_modified"])

    def test_plain_modify(self):
        patch2 = {
            "files_modified": ["abc4.txt"],
            "hash": {"abc4.txt": "plain.modify.abc4.txt.hash"}
        }
        add_defaults(patch2)
        p = patchutils.merge_patches(self.patch_test, patch2)
        self.assertIn("abc4.txt", p["files_modified"])
        self.assertIn("abc4.txt", p['hash'])

    def setUp(self):
        self.patch_test = {
            "files_added": [
                "abc1.txt",
            ],
            "files_removed": [
                "abc2.txt"
            ],
            "files_modified": [
                "abc3.txt"
            ],
            "directories_added": [
                "abcd1"
            ],
            "directories_removed": [
                "abcd2"
            ],
            "hash": {
                "abc1.txt": "abc_hash1.txt",
                "abc3.txt": "abc_hash3.txt"
            }
        }


def removal_test(self, k, p):
    self.assertNotIn(k, p['files_added'])
    self.assertNotIn(k, p['files_removed'])
    self.assertNotIn(k, p['hash'])
    self.assertNotIn(k, p['files_modified'])


def add_defaults(d: dict):
    d.setdefault("files_added", [])
    d.setdefault("files_removed", [])
    d.setdefault("files_modified", [])
    d.setdefault("directories_added", [])
    d.setdefault("directories_removed", [])
    d.setdefault("hash", {})


if __name__ == "__main__":
    unittest.main()
