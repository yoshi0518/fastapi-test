# FastAPI Test

## Port(Host:Container)

- FastAPI 8000:8000

## How to Use

### 前提

Python 開発環境構築済

### 開発環境準備

```bash
# リポジトリをクローン
$ rm -fr api
$ git clone git@github.com:yoshi0518/fastapi-test.git api && cd api

# 環境変数ファイルをコピー、内容修正
$ cp .env.sample .env

# 仮想環境作成、パッケージをインストール
$ uv venv
$ uv sync

# 仮想環境に接続
$ source .venv/bin/activate

# 開発サーバーを起動
$ task start
```

### uv コマンド実行方法

```bash
# 仮想環境に接続
$ source .venv/bin/activate

# パッケージを追加
$ uv add [パッケージ名]
$ uv add --dev [パッケージ名]

# パッケージを削除
$ uv remove [パッケージ名]
$ uv remove --dev [パッケージ名]

# パッケージ一覧を確認
$ uv pip list

# コマンド一覧を確認
$ task --list

# 開発サーバーを起動
$ task start

# Format
$ task fmt

# Lint
$ task lint

# Typecheck
$ task typecheck
```

### Alembic コマンド実行方法

```bash
# マイグレーションファイル作成(SQLAlchemy Modelから自動作成)
$ alembic revision --autogenerate -m "xxx"

# マイグレーションファイル作成(手動作成)
$ alembic revision -m "xxx"

# アップグレード(最新)
$ alembic upgrade head

# アップグレード(現バージョンから相対参照)
$ alembic upgrade +1
$ alembic upgrade +2

# ダウングレード(現バージョンから相対参照)
$ alembic downgrade -1
$ alembic downgrade -2

# ダウングレード(初期化)
$ alembic downgrade base

# 現時点の情報を確認
$ alembic current

# マイグレーション履歴を確認
$ alembic history
$ alembic history --verbose
```

### requirements.txt の作成方法

```bash
# uv仮想環境からrequirements.txtを作成(パッケージの追加・変更を行った際にrequirements.txtを最新化する)
$ uv export --format=requirements.txt > requirements.txt
```
