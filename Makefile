presentation.html: slides.md
	darkslide -t theme -l no slides.md

clean:
	rm presentation.html
