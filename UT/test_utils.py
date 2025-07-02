import unittest
import os
import json
from unittest.mock import patch, mock_open

# テスト対象のutils.pyをインポート
# プロジェクトルートからの相対パスでインポートできるように、sys.pathを一時的に変更
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
sys.path.pop(0) # パスを元に戻す

class TestUtils(unittest.TestCase):

    def setUp(self):
        # テスト前に一時的な設定ファイルを削除
        if os.path.exists(utils.CONFIG_FILE):
            os.remove(utils.CONFIG_FILE)
        if os.path.exists(utils.HASHED_CONFIG_FILE):
            os.remove(utils.HASHED_CONFIG_FILE)

    def tearDown(self):
        # テスト後に一時的な設定ファイルを削除
        if os.path.exists(utils.CONFIG_FILE):
            os.remove(utils.CONFIG_FILE)
        if os.path.exists(utils.HASHED_CONFIG_FILE):
            os.remove(utils.HASHED_CONFIG_FILE)

    def test_hash_password(self):
        password = "mysecretpassword"
        hashed_password = utils.hash_password(password)
        self.assertIsInstance(hashed_password, str)
        self.assertNotEqual(password, hashed_password)
        # bcryptのハッシュは$2b$または$2a$で始まる
        self.assertTrue(hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"))
        # 同じパスワードでもハッシュは毎回異なることを確認（ソルトのため）
        another_hashed_password = utils.hash_password(password)
        self.assertNotEqual(hashed_password, another_hashed_password)

    def test_check_password_correct(self):
        password = "mysecretpassword"
        hashed_password = utils.hash_password(password)
        self.assertTrue(utils.check_password(password, hashed_password))

    def test_check_password_incorrect(self):
        password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed_password = utils.hash_password(password)
        self.assertFalse(utils.check_password(wrong_password, hashed_password))

    def test_check_password_invalid_hash(self):
        password = "mysecretpassword"
        invalid_hash = "invalid_hash_string"
        with self.assertRaises(ValueError):
            utils.check_password(password, invalid_hash)

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    @patch('json.load', return_value={"key": "value"})
    def test_load_config_success(self, mock_json_load, mock_file_open):
        config = utils.load_config()
        self.assertEqual(config, {"key": "value"})
        mock_file_open.assert_called_once_with(utils.CONFIG_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print') # print関数をモック化してエラーメッセージを確認
    def test_load_config_file_not_found(self, mock_print, mock_file_open):
        config = utils.load_config()
        self.assertEqual(config, {})
        mock_print.assert_called_once_with(f"Error: {utils.CONFIG_FILE} not found.")

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value') # 不正なJSON
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting property name enclosed in double quotes", "", 0))
    @patch('builtins.print')
    def test_load_config_json_decode_error(self, mock_print, mock_json_load, mock_file_open):
        config = utils.load_config()
        self.assertEqual(config, {})
        mock_print.assert_called_once_with(f"Error: Could not decode JSON from {utils.CONFIG_FILE}.")

    @patch('builtins.open', new_callable=mock_open, read_data='{"hashed_key": "hashed_value"}')
    @patch('json.load', return_value={"hashed_key": "hashed_value"})
    def test_load_hashed_config_success(self, mock_json_load, mock_file_open):
        hashed_config = utils.load_hashed_config()
        self.assertEqual(hashed_config, {"hashed_key": "hashed_value"})
        mock_file_open.assert_called_once_with(utils.HASHED_CONFIG_FILE, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print')
    def test_load_hashed_config_file_not_found(self, mock_print, mock_file_open):
        hashed_config = utils.load_hashed_config()
        self.assertEqual(hashed_config, {})
        mock_print.assert_called_once_with(f"Error: {utils.HASHED_CONFIG_FILE} not found.")

    @patch('builtins.open', new_callable=mock_open, read_data='{"hashed_key": "hashed_value')
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting property name enclosed in double quotes", "", 0))
    @patch('builtins.print')
    def test_load_hashed_config_json_decode_error(self, mock_print, mock_json_load, mock_file_open):
        hashed_config = utils.load_hashed_config()
        self.assertEqual(hashed_config, {})
        mock_print.assert_called_once_with(f"Error: Could not decode JSON from {utils.HASHED_CONFIG_FILE}.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_hashed_config_success(self, mock_json_dump, mock_file_open):
        test_data = {"new_key": "new_value"}
        utils.save_hashed_config(test_data)
        mock_file_open.assert_called_once_with(utils.HASHED_CONFIG_FILE, 'w')
        mock_json_dump.assert_called_once_with(test_data, mock_file_open(), indent=4)

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('builtins.print')
    def test_save_hashed_config_io_error(self, mock_print, mock_file_open):
        test_data = {"new_key": "new_value"}
        utils.save_hashed_config(test_data)
        mock_print.assert_called_once() # エラーメッセージが出力されたことを確認
        self.assertIn(f"Error: Could not write to {utils.HASHED_CONFIG_FILE}.", mock_print.call_args[0][0])

if __name__ == '__main__':
    unittest.main()