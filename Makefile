current_dir = $(shell pwd)

database:
	docker run \
		--name postgres \
		-e POSTGRES_PASSWORD=adminpass \
		-v $(current_dir)/init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh \
		-p 5432:5432 \
		-d \
		postgres:13.3-alpine

table:
	cat init-users-table.sh | docker exec -i postgres sh

clean:
	docker rm -f postgres