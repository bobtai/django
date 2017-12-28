# Django RESTful API 試做

## apps
在 Django 中，是以 app 來劃分模組。

### trips app (djangosite/trips)
RESTful API 試做，試做[結果](https://bobtai.pythonanywhere.com/)。

### uploader app (djangosite/uploader)
上傳一張數字圖片，使用 Mnist Model 辨識圖片中的真實數字，試做結果如下：

準備一張數字圖片：

![img](https://raw.githubusercontent.com/bobtai/django/master/images/5.png)

上傳結果：

![img](https://raw.githubusercontent.com/bobtai/django/master/images/uploader.png)

## 環境

### Operating System

Mac OS X

### Virtual Environment

Python 3.6 venv

### Python Package

* tensorflow - 低階的深度學習程式庫，學習門檻高。
* keras - 高階的深度學習程式庫，學習門檻低，可幫助初學者快速建立深度學習模型。
* django - 免費且開放原始碼的 Web 應用程式框架。
* h5py - 訓練好的深度學習模型是`.h5`的檔案格式，載入模型需要此套件。

* pandas - 可以直接將 excel 格式的資料集載入。
* xlrd - excel 格式的依賴套件。
