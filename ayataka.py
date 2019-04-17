{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#ラベリングによる学習/検証データの準備\n",
    "\n",
    "from PIL import Image\n",
    "import os, glob\n",
    "import numpy as np\n",
    "import random, math"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#画像が保存されているルートディレクトリのパス\n",
    "root_dir = \"tea_datasets\"\n",
    "# 商品名\n",
    "categories = [\"綾鷹\",\"お〜いお茶\",\"伊右衛門　贅沢冷茶\",\"爽健美茶\",\n",
    "              \"綾鷹　茶葉のあまみ\",\"お〜いお茶　ほうじ茶\",\"伊右衛門\",\"お〜いお茶　濃い茶\",\n",
    "              \"生茶\",\"十六茶\"]\n",
    "\n",
    "# 画像データ用配列\n",
    "X = []\n",
    "# ラベルデータ用配列\n",
    "Y = []\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#画像データごとにadd_sample()を呼び出し、X,Yの配列を返す関数\n",
    "def make_sample(files):\n",
    "    global X, Y\n",
    "    X = []\n",
    "    Y = []\n",
    "    for cat, fname in files:\n",
    "        add_sample(cat, fname)\n",
    "    return np.array(X), np.array(Y)\n",
    "\n",
    "#渡された画像データを読み込んでXに格納し、また、\n",
    "#画像データに対応するcategoriesのidxをY格納する関数\n",
    "def add_sample(cat, fname):\n",
    "    img = Image.open(fname)\n",
    "    img = img.convert(\"RGB\")\n",
    "    img = img.resize((150, 150))\n",
    "    data = np.asarray(img)\n",
    "    X.append(data)\n",
    "    Y.append(cat)\n",
    "\n",
    "#全データ格納用配列\n",
    "allfiles = []\n",
    "\n",
    "#カテゴリ配列の各値と、それに対応するidxを認識し、全データをallfilesにまとめる\n",
    "for idx, cat in enumerate(categories):\n",
    "    image_dir = root_dir + \"/\" + cat\n",
    "    files = glob.glob(image_dir + '/*.jpg')#*は何でもいいけど、.jpgのファイルのすべてを対象にとっている\n",
    "    for f in files:\n",
    "        allfiles.append((idx, f))\n",
    "        \n",
    "        \n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#シャッフル後、学習データと検証データに分ける\n",
    "random.shuffle(allfiles)\n",
    "th = math.floor(len(allfiles) * 0.8)\n",
    "train = allfiles[0:th]\n",
    "test  = allfiles[th:]\n",
    "X_train, y_train = make_sample(train)\n",
    "X_test, y_test = make_sample(test)\n",
    "xy = (X_train, X_test, y_train, y_test)\n",
    "#データを保存する（データの名前を「tea_data.npy」としている）\n",
    "np.save(\"/Users/arimachishun/Desktop/ayataka/tea_data.npy\", xy)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#モデルの構築\n",
    "\n",
    "from keras import layers, models\n",
    "\n",
    "model = models.Sequential()\n",
    "model.add(layers.Conv2D(32,(3,3),activation=\"relu\",input_shape=(150,150,3)))\n",
    "model.add(layers.MaxPooling2D((2,2)))\n",
    "model.add(layers.Conv2D(64,(3,3),activation=\"relu\"))\n",
    "model.add(layers.MaxPooling2D((2,2)))\n",
    "model.add(layers.Conv2D(128,(3,3),activation=\"relu\"))\n",
    "model.add(layers.MaxPooling2D((2,2)))\n",
    "model.add(layers.Conv2D(128,(3,3),activation=\"relu\"))\n",
    "model.add(layers.MaxPooling2D((2,2)))\n",
    "model.add(layers.Flatten())\n",
    "model.add(layers.Dense(512,activation=\"relu\"))\n",
    "model.add(layers.Dense(10,activation=\"sigmoid\")) #分類先の種類分設定\n",
    "\n",
    "#モデル構成の確認\n",
    "model.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#モデルのコンパイル\n",
    "\n",
    "from keras import optimizers\n",
    "\n",
    "model.compile(loss=\"binary_crossentropy\",\n",
    "              optimizer=optimizers.RMSprop(lr=1e-4),\n",
    "              metrics=[\"acc\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#データの準備\n",
    "\n",
    "from keras.utils import np_utils\n",
    "import numpy as np\n",
    "\n",
    "categories = [\"綾鷹\",\"お〜いお茶\",\"伊右衛門　贅沢冷茶\",\"爽健美茶\",\n",
    "              \"綾鷹　茶葉のあまみ\",\"お〜いお茶　ほうじ茶\",\"伊右衛門\",\"お〜いお茶　濃い茶\",\n",
    "              \"生茶\",\"十六茶\"]\n",
    "nb_classes = len(categories)\n",
    "\n",
    "X_train, X_test, y_train, y_test = np.load(\"/Users/arimachishun/Desktop/ayataka/tea_data.npy\")\n",
    "\n",
    "#データの正規化\n",
    "X_train = X_train.astype(\"float\") / 255\n",
    "X_test  = X_test.astype(\"float\")  / 255\n",
    "\n",
    "#kerasで扱えるようにcategoriesをベクトルに変換\n",
    "y_train = np_utils.to_categorical(y_train, nb_classes)\n",
    "y_test  = np_utils.to_categorical(y_test, nb_classes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "#モデルの学習\n",
    "\n",
    "model = model.fit(X_train,\n",
    "                  y_train,\n",
    "                  epochs=10,\n",
    "                  batch_size=6,\n",
    "                  validation_data=(X_test,y_test))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#学習結果を表示\n",
    "\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "acc = model.history['acc']\n",
    "val_acc = model.history['val_acc']\n",
    "loss = model.history['loss']\n",
    "val_loss = model.history['val_loss']\n",
    "\n",
    "epochs = range(len(acc))\n",
    "\n",
    "plt.plot(epochs, acc, 'bo', label='Training acc')\n",
    "plt.plot(epochs, val_acc, 'b', label='Validation acc')\n",
    "plt.title('Training and validation accuracy')\n",
    "plt.legend()\n",
    "plt.savefig('精度を示すグラフのファイル名')\n",
    "\n",
    "plt.figure()\n",
    "\n",
    "plt.plot(epochs, loss, 'bo', label='Training loss')\n",
    "plt.plot(epochs, val_loss, 'b', label='Validation loss')\n",
    "plt.title('Training and validation loss')\n",
    "plt.legend()\n",
    "plt.savefig('損失値を示すグラフのファイル名')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#モデルの保存\n",
    "\n",
    "json_string = model.model.to_json()\n",
    "open('/Users/arimachishun/Desktop/ayataka/tea_predict.json', 'w').write(json_string)\n",
    "\n",
    "#重みの保存\n",
    "\n",
    "hdf5_file = \"/Users/arimachishun/Desktop/ayataka/tea_predict.hdf5\"\n",
    "model.model.save_weights(hdf5_file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from PIL import Image\n",
    "import os, glob\n",
    "import numpy as np\n",
    "import random, math\n",
    "\n",
    "# 画像が保存されているディレクトリのパス\n",
    "root_dir = \"tea_datasets\"\n",
    "# 画像が保存されているフォルダ名\n",
    "categories = [\"綾鷹\",\"お〜いお茶\",\"伊右衛門　贅沢冷茶\",\"爽健美茶\",\n",
    "              \"綾鷹　茶葉のあまみ\",\"お〜いお茶　ほうじ茶\",\"伊右衛門\",\"お〜いお茶　濃い茶\",\n",
    "              \"生茶\",\"十六茶\"]\n",
    "\n",
    "X = [] # 画像データ\n",
    "Y = [] # ラベルデータ\n",
    "\n",
    "# フォルダごとに分けられたファイルを収集\n",
    "#（categoriesのidxと、画像のファイルパスが紐づいたリストを生成）\n",
    "allfiles = []\n",
    "for idx, cat in enumerate(categories):\n",
    "    image_dir = root_dir + \"/\" + cat\n",
    "    files = glob.glob(image_dir + \"/*.jpg\")\n",
    "    for f in files:\n",
    "        allfiles.append((idx, f))\n",
    "\n",
    "for cat, fname in allfiles:\n",
    "    img = Image.open(fname)\n",
    "    img = img.convert(\"RGB\")\n",
    "    img = img.resize((150, 150))\n",
    "    data = np.asarray(img)\n",
    "    X.append(data)\n",
    "    Y.append(cat)\n",
    "\n",
    "x = np.array(X)\n",
    "y = np.array(Y)\n",
    "\n",
    "np.save(\"tea_data_test_X/tea_data_test_X_150.npy\", x)\n",
    "np.save(\"tea_data_test_Y/tea_data_test_Y_150.npy\", y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# モデルの精度を測る\n",
    "\n",
    "#評価用のデータの読み込み\n",
    "test_X = np.load(\"tea_data_test_X/tea_data_test_X_150.npy\")\n",
    "test_Y = np.load(\"tea_data_test_Y/tea_data_test_Y_150.npy\")\n",
    "\n",
    "#Yのデータをone-hotに変換\n",
    "from keras.utils import np_utils\n",
    "\n",
    "test_Y = np_utils.to_categorical(test_Y, 10)\n",
    "\n",
    "score = model.model.evaluate(x=test_X,y=test_Y)\n",
    "\n",
    "print('loss=', score[0])\n",
    "print('accuracy=', score[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#綾鷹を選ばせるプログラム\n",
    "\n",
    "from keras import models\n",
    "from keras.models import model_from_json\n",
    "from keras.preprocessing import image\n",
    "import numpy as np\n",
    "\n",
    "#保存したモデルの読み込み\n",
    "model = model_from_json(open('/Users/arimachishun/Desktop/ayataka/tea_predict.json').read())\n",
    "#保存した重みの読み込み\n",
    "model.load_weights('/Users/arimachishun/Desktop/ayataka/tea_predict.hdf5')\n",
    "\n",
    "categories = [\"綾鷹\",\"お〜いお茶\",\"伊右衛門　贅沢冷茶\",\"爽健美茶\",\n",
    "              \"綾鷹　茶葉のあまみ\",\"お〜いお茶　ほうじ茶\",\"伊右衛門\",\"お〜いお茶　濃い茶\",\n",
    "              \"生茶\",\"十六茶\"]\n",
    "\n",
    "#画像を読み込む\n",
    "img_path = str(input())\n",
    "img = image.load_img(img_path,target_size=(150, 150, 3))\n",
    "x = image.img_to_array(img)\n",
    "x = np.expand_dims(x, axis=0)\n",
    "\n",
    "#予測\n",
    "features = model.predict(x)\n",
    "\n",
    "#予測結果によって処理を分ける\n",
    "if features[0,0] == 1:\n",
    "    print (\"選ばれたのは、綾鷹でした。\")\n",
    "\n",
    "elif features[0,4] == 1:\n",
    "    print (\"選ばれたのは、綾鷹（茶葉のあまみ）でした。\")\n",
    "\n",
    "else:\n",
    "    for i in range(0,10):\n",
    "          if features[0,i] == 1:\n",
    "              cat = categories[i]\n",
    "    message = \"綾鷹を選んでください。（もしかして：あなたが選んでいるのは「\" + cat + \"」ではありませんか？）\"\n",
    "    print(message)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
