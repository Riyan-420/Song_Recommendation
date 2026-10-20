# Intelligent Disaster Detection from Social Media Using Word2Vec, RNN and LSTM

**Name:** Riyan Khan Durrani  |  **Reg.no:** 2023611  |  **Course:** AI451-L (NLP LAB)  |  NLP Lab Mid – Question #03 (CLO-2, GA-5) P4

Everything is in one executed notebook: `Disaster_Tweets_Word2Vec_RNN_LSTM.ipynb`
(`Disaster_Tweets_Word2Vec_RNN_LSTM.html` is the same notebook exported for reading without Jupyter).

## Run it
* **Google Colab (quickest):** upload the `.ipynb` to <https://colab.research.google.com> (or open it from GitHub) and choose *Runtime → Run all*.
  Roughly 10–12 minutes on the free CPU runtime. Nothing else to upload: `train.csv` is downloaded and validated automatically
  (7,613 rows, 3,271 / 4,342 labels), falling back to an upload prompt.
* **Locally:** `pip install -r requirements.txt`, then `jupyter nbconvert --to notebook --execute --inplace Disaster_Tweets_Word2Vec_RNN_LSTM.ipynb`
  (or open it in Jupyter). `data/train.csv` is included, so no internet is needed (only the GloVe experiment at the very end downloads
  ~120 MB; offline it is skipped and the saved summary table `outputs/embedding_experiments.csv` is shown instead).

## Task → notebook sections
| Task | Marks | What was done |
|---|---|---|
| Q3.1 | 5 | clean → tokenize → stratified 80:20 split (6,090 / 1,523) → vocabulary from train only → integer encoding → padding (`MAX_LEN` 24) |
| Q3.2 | 5 | 100-d skip-gram Word2Vec trained on the 6,090 training tweets; PCA of 10 words + cosine matrix + interpretation |
| Q3.3 | 5 | Simple RNN and LSTM, identical frozen Word2Vec embedding and identical settings, ≤ 5 epochs (RNN 5, LSTM 4 with early stopping) |
| Q3.4 | 2.5 | accuracy / precision / recall / F1 / AUC, confusion matrices, loss + accuracy curves, McNemar test, 5-seed and duplicate-free robustness checks |
| Q3.5 | 2.5 | one false positive + one false negative analysed (with token-ablation checks); improvement = pre-trained GloVe-Twitter embeddings, tested against a FastText control and a same-vocabulary ablation over 5 seeds |

## Headline results (test set, 1,523 tweets, seed 42)
| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Simple RNN | 0.7965 | 0.8346 | 0.6560 | 0.7346 |
| LSTM | 0.8070 | 0.8346 | 0.6865 | 0.7534 |
| LSTM + GloVe-Twitter, extended vocabulary (proposed improvement) | 0.8234 | 0.8481 | 0.7171 | 0.7771 |

The two models are comparable: the LSTM is nominally ahead in the main run, but the gap is not statistically significant (McNemar p = 0.145) and its recall edge does not hold across seeds. The GloVe improvement is consistent over 5 seeds (mean F1 0.713 → 0.765–0.774); see Q3.5.

## Files
`outputs/` – figures, `metrics.json`, `test_predictions.csv` (per-tweet probabilities), `seed_robustness.csv`, `embedding_experiments.csv`, trained 100-d Word2Vec vectors.
`data/train.csv` – the labelled Kaggle file (only file used; `test.csv` is unlabeled and not needed).

## Reproducibility
Seeds fixed (42), deterministic TensorFlow ops, CPU only, single-threaded Word2Vec with a deterministic hash function.
Results are identical across re-runs with the same library versions (checked on a clean directory). On other TensorFlow/Keras versions the seed-42 headline numbers matched in a Colab-like test, but individual seed runs can differ slightly; the written commentary describes the shipped run and the printed outputs are authoritative.
