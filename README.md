# HASC Corpus内のデータの時間調節プログラム
HASC Corpusに含まれる加速度と角速度のデータ先頭時間とデータサイズ(行数)を揃えるプログラム using Python3
for AxisCorrection

## 使い方
1. pythonファイルと同ディレクトリにdataディレクトリを用意.
2. dataディレクトリにHASCコーパスのデータを入れる.
3. 以下のコマンドを実行

##### コマンド
```
python3 ArrangeTime_for_HASC.py
```


### データのディレクトリ構成
```
.  
data  
├── 1_stay  
│  ├── person0001  
│  │   ├── HASCXXXXXX-acc.csv  
│  │   ├── HASCXXXXXX-gyro.csv  
│  │   ├── HASCXXXXXX-mag.csv  
│  │   └── ...  
│  ├── person0002  
│  └── ...  
├── 2_walk  
│　├── person0001  
│　│   ├── HASCXXXXXX-acc.csv  
│　│   ├── HASCXXXXXX-gyro.csv  
│　│   ├── HASCXXXXXX-mag.csv  
│　│   └── ...  
│　├── person0002  
│　└── ...  
└── ...
```


### 　
Developed by icchi  
2016/05/19
