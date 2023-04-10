CACHEOPS_REDIS = {
    'host': 'redis', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended

    'socket_timeout': 3,   # connection timeout in seconds, optional
    # 'password': '...',     # optional
    # 'unix_socket_path': '' # replaces host and port
}

# Alternatively the redis connection can be defined using a URL:
# CACHEOPS_REDIS = "redis://localhost:6379/1"
# or
# CACHEOPS_REDIS = "unix://path/to/socket?db=1"
# or with password (note a colon)
# CACHEOPS_REDIS = "redis://:password@localhost:6379/1"


CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60},

    # Cache all queries to Permission
    # 'all' is an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    '*.*': {'ops': (), 'timeout': 60*60},

    # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*60},

    # NOTE: binding signals has its overhead, like preventing fast mass deletes,
    #       you might want to only register whatever you cache and dependencies.

    # Finally you can explicitely forbid even manual caching with:
    # 'some_app.*': None,
}
