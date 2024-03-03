# FastAPI Test

## Port(Host:Container)

- FastAPI 8000:8000

## How to Use

### 前提

- [Development Container](https://github.com/yoshi0518/devcontainer)の準備が終わっていること

### 開発環境準備

```bash
# fastapi-testリポジトリをクローン
$ rm -fr api
$ git clone git@github.com:yoshi0518/fastapi-test.git api && cd api

# 仮想環境作成、パッケージをインストール
$ poetry config virtualenvs.in-project true
$ poetry install

# 仮想環境を確認
$ poetry env list
$ poetry env info

# 仮想環境に接続
$ poetry shell

# FastAPIを起動(開発環境)
$ task start

# FastAPIを起動(本番環境)
$ ./cmd_startup.sh
```

### Poetry コマンド実行方法

```bash
# 仮想環境に接続
$ poetry shell

# パッケージを追加
$ poetry add [パッケージ名]
$ poetry add -D [パッケージ名]

# パッケージを削除
$ poetry remove [パッケージ名]
$ poetry remove -D [パッケージ名]

# パッケージ一覧を確認
$ poetry show

# コマンド一覧を確認
$ task --list

# 開発用サーバー起動
$ task start

# Format
$ task fmt

# Lint
$ task lint
```

### Alembic コマンド実行方法

```bash
# 仮想環境に接続
$ poetry shell

# マイグレーションファイル作成(SQLAlchemy Modelから自動作成)
$ alembic revision --autogenerate

# マイグレーションファイル作成(手動作成)
$ alembic revision

# アップグレード(最新)
$ alembic upgrade head

# アップグレード(最新) ※シェルスクリプト
$ chmod 700 /work/api/cmd_migrate_up.sh
$ /work/api/cmd_migrate_up.sh

# アップグレード(現バージョンから相対参照)
$ alembic upgrade +1
$ alembic upgrade +2

# ダウングレード(現バージョンから相対参照)
$ alembic downgrade -1
$ alembic downgrade -2

# ダウングレード(初期化)
$ alembic downgrade base

# ダウングレード(初期化) ※シェルスクリプト
$ chmod 700 /work/api/cmd_migrate_down.sh
$ /work/api/cmd_migrate_down.sh

# 現時点の情報を確認
$ alembic current

# マイグレーション履歴を確認
$ alembic history
$ alembic history --verbose
```

### requirements.txt の作成方法

```
# Poetry仮想環境からrequirements.txtを作成(パッケージの追加・変更を行った際にrequirements.txtを最新化する)
$ poetry export -f requirements.txt --output requirements.txt
```
