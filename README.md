# Web GP-TSM

![Demo](demo.mp4)

## Run the server
Go to the `server/` folder
```
cd server
```

Install necessary packages
```
pip install -r requirements.txt
```

The server needs a valid OPENAI_API_KEY to work. [Make sure you have one](https://platform.openai.com/docs/quickstart) and add it to `openaikey.py`.
```
echo "key='$OPENAI_API_KEY'" > openaikey.py
```

Run the server
```
python server.py
```

**Most of the server code are adjusted from https://github.com/ZiweiGu/GP-TSM**

## Install chrome extension

1. Load unpacked extension to Chrome from the folder `chrome-ext/`
2. Go to any of the `https://en.wikipedia.org/wiki/*` web page
3. Reload the page
4. Enjoy!