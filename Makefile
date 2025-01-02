install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
build-container:
	docker build --no-cache -t reels-automation-subtitles-generator .
build-container-no-ffmpeg:
	docker build --no-cache --build-arg INSTALL_FFMPEG=false -t reels-automation-subtitles-generator .
run-container:
	docker run --rm -it \
  --network reels-automation-docker-compose_local-kafka \
  --network reels-automation-docker-compose_minio-network \
  reels-automation-subtitles-generator