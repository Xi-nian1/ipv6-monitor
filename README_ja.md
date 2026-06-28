[简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Français](README_fr.md)

# IPv6 Monitor & Email Notifier

これは、Windows の**起動時**または**スリープ/休止状態からの復帰時**に、ローカルマシンのパブリック IPv6 アドレスを自動的に検出し、指定されたメールアドレスに SMTP 経由で送信する、非常に軽量なバックグラウンドアプリケーションです。

## 特徴
- **依存関係ゼロ**: Python に組み込まれている標準ライブラリ（`urllib`、`smtplib`、`socket` など）のみを使用します。サードパーティのパッケージを `pip install` する必要はありません。
- **1回のみ実行**: 無限ループでバックグラウンドに常駐することはありません。1回実行してメールを送信すると直ちに終了し、システムリソースを厳格に節約します。
- **システムレベルのトリガー**: システムイベントをトリガーする Windows タスク スケジューラと完全に統合されています。

## 使い方

> [!IMPORTANT]
> **準備:** 使い始める前に、ローカル環境に合わせて次の 2 つのファイルを変更する必要があります:
> 1. **`config.json`**: 送信者のメールアドレス、SMTP 認証コード、および受信者のメールアドレスを入力する必要があります。
> 2. **`task.xml`**: 自動起動を設定する場合は、内部のプレースホルダー パスを実際の絶対パスに置き換える必要があります。


### 1. 設定
`config.example.json` をコピーして `config.json` に名前を変更し、メール設定を入力します：
```json
{
    "from_email": "your_sender_email@qq.com",
    "auth_code": "your_smtp_auth_code",
    "to_email": "receiver_email@qq.com",
    "check_interval": 300,
    "retry_times": 3,
    "log_file": "ipv6_sender.log",
    "ip_check_services": [
        "https://ipv6.icanhazip.com",
        "https://v6.ident.me",
        "https://ipv6.lookup.test-ipv6.com/ip/"
    ]
}
```
*(注意: JSONファイルには `//` などのコメントを含めることはできません)*

### 2. スクリプトの実行
Python を使用して直接実行します：
```bash
python ipv6.py
```

### 3. EXE 実行ファイルとしてのビルド (オプション)
コンソール ウィンドウなしでバックグラウンドで静かに実行するには、`.exe` ファイルにパッケージ化することを強くお勧めします：
```bash
pip install pyinstaller
pyinstaller -F -w ipv6.py
```
ビルド後、生成された `ipv6.exe` をプロジェクトのルートディレクトリに移動します（`config.json` と同じディレクトリにあることを確認してください）。

### 4. Windows タスク スケジューラの自動復帰の設定

**起動時**および**スリープからの復帰時**に `ipv6.exe` が自動的に実行されるように構成する必要があります：

1. **XML パスの変更**: メモ帳で `task.xml` を開きます。一番下にある `<Command>` および `<WorkingDirectory>` タグを見つけ、`C:\path\to\your\folder` を `ipv6.exe` を保存した実際の絶対パスに置き換え、ファイルを保存します。
2. **ターミナルを開く**: `Win + X` を押して、**Windows PowerShell (管理者)** または **ターミナル (管理者)** を開きます。
3. **タスクのインポート**: `cd` コマンドを使用してプロジェクトディレクトリに移動し、次のコマンドを実行してタスクをインポートします：
```powershell
schtasks /create /tn "IPv6_Monitor" /xml .\task.xml /f
```
4. インポートが成功すると、システムが起動または休止状態から復帰するたびに、スクリプトがバックグラウンドで自動的に実行され、メールが送信されます。
