# reviewComment_to_CSV_sample
プルリクエストおよびそのレビューコメントをCSV出力するGitHubActionsのサンプル

## Description
[手動トリガー](https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/)で、以下の正規化されたデータが出力される。

- output_pr.csv
プルリクエスト一覧。
- output_cm.csv
プルリクエストに対するコメント一覧。
特定ファイル・特定行に対してのコメントはその対象も表示する。
