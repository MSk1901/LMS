REDIS_CONTAINER=lms-redis-1

redis_dump:
	docker exec $(REDIS_CONTAINER) redis-cli BGSAVE