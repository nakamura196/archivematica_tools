import configparser
import re

# 設定ファイルのパス
file_path = '../settings.ini'

# configparserの初期化
config = configparser.ConfigParser()

# 設定ファイルの読み込み
config.read(file_path)

# 現在のバージョンの取得
current_version = config.get('DEFAULT', 'version')

# バージョン番号のインクリメント
major, minor, patch = map(int, current_version.split('.'))
new_version = f'{major}.{minor}.{patch+1}'

# 新しいバージョンの設定
config.set('DEFAULT', 'version', new_version)

# 設定ファイルの書き込み
with open(file_path, 'w') as configfile:
    config.write(configfile)

print(f'Updated version from {current_version} to {new_version}')