install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

build-container:
	docker build -t reels-automation-subtitles-generator .

run-container:
	docker run --rm -it reels-automation-subtitles-generator --mount type=bind, src="/home/porky/Downloads/vosk-model-small-es-0.42", dst=model