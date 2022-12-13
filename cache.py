"""
Cache: implement a simple redis based cache with the semantics of dicts.

Deals with the encoding on redis automatically.
"""
import logger
import os
import json
import redis
import time


TTL = int(os.getenv("DEFAULT_TTL", 24 * 3600))


logger = logger.get_module_logger(__name__)


class Cache:
    """Redis cache implementation. Conforms to the dict interface.

    Can save key-value pairs to redis.
    """

    def __init__(self):
        """Construct it."""
        host = os.getenv('REDIS_HOST', 'localhost')
        port = int(os.getenv('REDIS_PORT', '6379'))
        logger.info("Connecting to redis at %s:%d" % (host, port))
        self.r = redis.StrictRedis(host=host, port=port, decode_responses=True)
        self.r.hset(b"cache_metadata", b"created_at", time.time())

    def __contains__(self, key: str) -> bool:
        """Check for existence of the key in the redis cache."""
        return self.r.exists(key)

    def __getitem__(self, key: str) -> str:
        """Get key from redis."""
        return self.r.get(key)

    def __setitem__(self, key: str, value: str, ttl: int = TTL) -> int:
        """Store the key in redis."""
        rv = self.r.set(key, value)
        if ttl:
            self.r.expire(key, ttl)
        return rv

    def __len__(self):
        """Return how many keys are stored in redis."""
        info = self.r.info("keyspace")
        logger.info("type(info) = %s. info=%s" % (type(info), info))
        numkeys = info["db0"]["keys"]
        return numkeys

    def __delitem__(self, key: str) -> int:
        """Delete the key from redis."""
        return self.r.delete(key)

    def clear(self) -> None:
        """Clear the redis cache and make sure the metadata is refreshed."""
        self.r.flushdb()
        self.r.hset(b"cache_metadata", b"created_at", time.time())
        return


if __name__ == "__main__":
    c = Cache()
    c["foo"] = "bar"
    assert "bar" == c["foo"]
    assert "foo" in c
    c['foo44'] = "xyz"
    c['complex_dict'] = json.dumps({'bobo': 'baba', 'barbarella': 68})
    print("complex dict = %r" % json.loads(c['complex_dict']))
    assert "foo44" in c
    assert c['foo44'] == "xyz"
    print("number of entries in the cache dict: %d" % len(c))
    assert len(c) == 4
