# Practical Work Kit · 實用工作四助手

![四種日常 AI 工作助手：檢查成果、挑戰計畫、發展點子、保存交接。](docs/assets/social-preview.png)

四種可重複使用的 AI 技能：檢查成果、挑戰計畫、發展點子，以及讓下一個對話接得上。

[English](README.md) · [完整範例](docs/EXAMPLES.md) · [下載最新版](https://github.com/Yingye107/practical-work-kit/releases/latest)

把已有的內容貼上，直接說需要什麼。短訊息就做短檢查，要三個標題就給三個標題；交接保存真正做過的事與原稿，不強迫填一套表格。

| 助手 | 適合什麼情況 | 技能名稱 |
|---|---|---|
| 成果檢查員 | 文件、預算、設計或程式已做完，想知道是否可用、漏了什麼 | `check-my-work` |
| 計畫挑戰者 | 還沒決定，想找關鍵假設、代價與更可行的做法 | `challenge-my-plan` |
| 創意總監 | 想把點子變成方向、草稿或可以先試的小版本 | `shape-my-idea` |
| 交接助手 | 要換對話、換工具或交給別人，希望保留決策與進度 | `carry-my-context` |

## 一分鐘看懂它能幫什麼

安裝後，貼上這個小例子：

```text
使用 $check-my-work 核對這份預算。
場地 3,000、材料 2,000，總計寫 6,000。
我沒有提供收據，也還沒確認是否含稅。
簡短告訴我哪裡要改、哪些部分還沒驗證。
```

**有用的結果應該是：**總額改成 **5,000**，指出原本多了 **1,000**，並保留「收據與稅額尚未確認」。你可以立刻修正加總，也知道下一步該查什麼。

這是可自行試用的示例，不保證模型每次回覆相同。[完整範例](docs/EXAMPLES.md) 也有挑戰計畫、三個影片標題與換對話交接的輸入／輸出。

## 安裝

使用有 `plugin` 命令的 Codex CLI，執行：

```sh
codex plugin marketplace add Yingye107/practical-work-kit --ref main
codex plugin add practical-work-kit@practical-work-kit
```

安裝後開新的對話。要固定版本，把第一行的 `--ref main` 改成 `--ref v0.1.0`。可用以下命令確認狀態：

```sh
codex plugin list --marketplace practical-work-kit --json
```

也可到 [Releases](https://github.com/Yingye107/practical-work-kit/releases) 下載 ZIP 與 SHA256SUMS，解壓後依 [INSTALL.txt](INSTALL.txt) 安裝。若你的 CLI 不認得 `plugin`，請依 [官方文件](https://developers.openai.com/plugins/build/plugins) 核對宿主支援。

只選一個來源安裝。已啟用本機整合版或同名單一技能時，避免再同時啟用另一份。本專案在 GitHub 發布，並不代表已在 OpenAI 公開插件目錄上架。

## 直接用這四句開始

```text
使用 $check-my-work 檢查這份成果，告訴我是否可用、漏了什麼和先修哪裡。
使用 $challenge-my-plan 挑戰這個計畫，給我有理由的判斷與更可行的做法。
使用 $shape-my-idea 把這個點子變成具體方向，符合我的時間與資源。
使用 $carry-my-context 整理這段對話，給我可貼到新對話的交接。
```

接著貼內容，並說明想要的篇幅。回覆跟隨你的語言；有可讀附件及工具時才能做更深入的檢查。明確點名有助於選對技能，自動選用仍取決於宿主。

例如：「場地 3,000、材料 2,000，總計寫 6,000，幫我核對」應抓到總額多了 1,000；沒有收據就不能宣稱收據也驗過。[範例頁](docs/EXAMPLES.md) 有四個可直接改用的例子。

## 能力與資料界線

安裝包只有技能文字、按需參考資料與介面資訊，不提供 MCP 服務、額外帳號連接、背景 hook 或執行腳本。原始碼內的 Python 驗證／封裝工具只供維護者手動或 CI 執行。

審查、發想或交接本身不授權修改、付費、發訊息、上傳或發布。交接不會讓另一台電腦取得舊附件，也不保證永久記憶。這些是 AI 指引，不能保證答案正確或取代宿主的權限隔離；請勿放入金鑰與不必要的私人資料。資安通報與限制見 [SECURITY.md](SECURITY.md)。

## 開源與貢獻

歡迎提供有實際案例的改善：錯誤示範、較容易使用的說法、適用領域或必要修正。請先去除敏感資料，參考 [貢獻說明](CONTRIBUTING.md) 與 [行為準則](CODE_OF_CONDUCT.md)。不需要為小改善新增一整套流程。

準備 Python 3.11 以上與 Git，在專案根目錄執行，無需額外 pip 套件：

```sh
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build_release.py --output dist
```

由 [YINGYE Studio](https://github.com/Yingye107) 發布，採 [Apache-2.0](LICENSE)。採用方法的原始来源與各自授權保留在 [SOURCE_NOTICES.txt](SOURCE_NOTICES.txt)、[licenses/](licenses/) 與 [provenance.json](provenance.json)。轉載或改作請一併保留。版本內容見 [CHANGELOG.md](CHANGELOG.md)。
