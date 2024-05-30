build-workshop:
	./build-workshop.sh

run:
	$(MAKE) clean
	docker compose --profile prod up --wait -d

cli:
	docker exec -it nso-workshop /bin/bash

clean: 
	docker compose --profile prod down

follow:
	docker logs --follow nso-workshop