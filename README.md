# Képfeldolgozás tárgy - Plate Recognition
Ez a repository a BME VIK Képfeldolgozás című tárgy (BMEVIIIAD00) házifeladatának megoldása.

## VS Code beállítása és Jupyter Notebook installálása

Előfeltétel:
- Python3
- Visual Studio Code

```pip install jupyter``` paranccsal letöltődik a jupyter package a pythonhoz.
Ezután a VS Code-ban <b>Crtl+Shift+P</b> paranccsal előjön a <b>Command Palette</b>, és a <b>Python: Select Interpreter</b> kiválasztása után a már telepített Python környezetet kell kiválasztani.

## NVIDIA Cuda telepítése

NVIDIA kártya esetén a CUDA Toolkit letöltésével a videókártyán a gyorsabb tanítás érdekében tudunk dolgozni, ehhez itt az útmutató.

https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

Az alábbi linkről le kell tölteni a nekünk megfelelő verziót, többnyire Windows/x86_64/(Windows 10 vagy 11)/exe(local) kell nekünk. Ezt utána az alap beállításokkal telepítenünk kell.

Ezután a pytorch packaget a CUDA-nak megfelelően kell telepíteni. Az adott linkhez és leíráshoz a következő parancs felel meg. Biztonság kedvéért ajánlott uninstallálni a packageket, mielőtt ezt a parancsot lefuttatjuk.

```pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```

Más oprendszer esetén a https://pytorch.org oldalán lehet további verziókat keresni.

## Google Collab

VGA kártya hiányában lehetőség van a Google Collabot használni. Ebben az esetben a VM elindítása előtt a <b>Futtatókörnyezet -> Futtatókörnyezet módosítása</b> menüpontban be kell állítani a hardveres gyórsítást <b>T4 GPU</b>-ra.