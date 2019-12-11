index.html: slides.md
	darkslide -r -t theme -l no slides.md
	sed -e "s,../../a/envs/py38/lib/python3.8/site-packages/darkslide/themes/default/,,g" presentation.html >index.html

clean:
	rm -f index.html presentation.html
