# FastAPI Template

## Port(Host:Container)

- FastAPI 8000:8000

## How to Use

### 前提

Python 開発環境構築済

### 開発環境準備

```bash
# リポジトリをクローン
$ rm -fr api
$ git clone git@github.com:yoshi0518/fastapi-template.git api && cd api

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

### requirements.txt の作成方法

```bash
# uv仮想環境からrequirements.txtを作成(パッケージの追加・変更を行った際にrequirements.txtを最新化する)
$ uv export --format=requirements.txt > requirements.txt
```
