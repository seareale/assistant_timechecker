# assistant_timechecker
assistant_timechecker

## 1. Env
Download the suitable ChromeDriver. [Link](https://chromedriver.chromium.org/)

## 2. Data
Prepare `data.txt` as below.
```txt
{ID} {PW}
{YYYY-MM-DD} {HH:MM:SS} {HH:MM:SS} {TASK}
{YYYY-MM-DD} {HH:MM:SS} {HH:MM:SS} {TASK}
...
```

### 3. Run
```bash
# Before run, check the files below
# chromedriver.exe, data.txt, run.py

$ python3 run.py
```
