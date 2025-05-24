# GenAI漫才ジェネレーター

このプロジェクトは、GoogleのGemini APIを利用して、漫才の台本を生成し、その台本に基づいた音声ファイルを生成するPythonアプリケーションです。

## 概要

ユーザーが指定したテーマ（現在は「taniとtakedaの漫才」で固定）に基づいて、Gemini APIが30秒程度の漫才スクリプトを生成します。生成されたスクリプトは、`tani:` と `takeda:` の形式で出力されます。

その後、生成されたスクリプトを元に、再度Gemini APIを利用して音声データを生成します。各登場人物（taniとtakeda）には、それぞれ異なる声（LedaとGacrux）が割り当てられています。

最終的に、生成された音声データは `output.wav` というファイル名で保存されます。

## 主な機能

- Gemini API (gemini-2.0-flash) を利用した漫才スクリプトの生成
- Gemini API (gemini-2.5-flash-preview-tts) を利用した音声データの生成
- 生成された音声データのWAVEファイル形式 (.wav) での保存

## 必要なもの

- Python 3.x
- `uv` (Pythonパッケージインストーラおよび仮想環境マネージャー)
- `google-generativeai` ライブラリ
- `python-dotenv` ライブラリ

## セットアップ

1. **リポジトリのクローン:**
   ```bash
   git clone https://github.com/あなたのユーザー名/genai-speech.git
   cd genai-speech
   ```

2. **必要なライブラリのインストール:**
   プロジェクトのルートディレクトリで以下のコマンドを実行して、`pyproject.toml` と `uv.lock` に基づいて依存関係をインストールします。
   ```bash
   uv sync
   ```

3. **環境変数の設定:**
   プロジェクトのルートディレクトリに `.env` ファイルを作成し、Gemini APIキーを設定します。`.example.env` ファイルをコピーして作成できます。
   ```
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
   `YOUR_API_KEY_HERE` を実際のAPIキーに置き換えてください。

## 使い方

プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
uv run main.py
```

実行が完了すると、プロジェクトのルートディレクトリに `output.wav` という音声ファイルが生成されます。
