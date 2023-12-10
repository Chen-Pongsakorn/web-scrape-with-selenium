TOTAL:=1
ABSOLUTE_LOCAL_PATH:=

run_local:
	python3 src/main.py --total_goods ${TOTAL}

build_docker:
	docker buildx build --platform linux/arm64/v8 --rm -t compare_goods:latest .

run_docker_locally:
	docker run -v ${ABSOLUTE_LOCAL_PATH}:/app/output compare_goods:latest python3 src/main.py --total_goods ${TOTAL}