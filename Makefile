install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
build-container:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEPLOYMENT' >> .env
	docker build --no-cache -t reels-automation-subtitles-generator .
build-container-no-ffmpeg:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEPLOYMENT' >> .env
	docker build --no-cache --build-arg INSTALL_FFMPEG=false -t reels-automation-subtitles-generator .
run-container:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEPLOYMENT' >> .env
	docker run --rm -it \
  --network reels-automation-docker-compose_local-kafka \
  --network reels-automation-docker-compose_minio-network \
  reels-automation-subtitles-generator

python-run:
	cp .env.development .env
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && python main.py'

python-run-prod:
	cp .env.production .env
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && python main.py'

build-run-no-ffmpeg: build-container-no-ffmpeg run-container 