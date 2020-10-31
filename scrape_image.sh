if [ "$(uname)" == "Darwin" ]; then
	"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  --headless --screenshot --window-size=900,1000 --default-background-color=0  https://www.google.com/search?q=weather
else
	chromium-browser --headless --screenshot --window-size=900,1000 --default-background-color=0  https://www.google.com/search?q=weather
fi
