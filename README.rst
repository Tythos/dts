DTS
===

DTS illustrates a simple and robust method for constructing service-oriented
architectures (SOAs) behind an Nginx reverse-proxy. This provides static file
web applications (like those hosted under the "user" image) a single-origin
behind which services can be accessed, as well as an agnostic frontend (Nginx)
that can be extended to support HTTPS/SSL, OAuth protocols, and other measures.

This example also includes a data layer that is hidden from the front end.
Instead, the "wsgi" service (a Flask-based Python server) uses internal
addressing to open a Redis connection to the data service, exposing specific
API endpoints through the reverse-proxy. This significantly improves security
and can be combined with other Nginx/Redis features like caching and sharding.

The fundamental architecture looks something like this, and can be easily
extended with additional services:

* "data", "user", and "wsgi" define specific Docker images (and can be tested
  on their own isolation for debugging and verification)

* "revprox" defines an Nginx-based reverse-proxy for exposing/routing specific
  requests to specific endpoints (as identified by URL pattern and service
  name, respectively). Note that this does NOT include the "data" layer.

* "docker-compose.yml" defines how all four services can be built and "spun up"
  in coordination with one another. This includes external port exposure ONLY
  for the reverse-proxy, which will hand of relevant inter-service connections
  internally. This also defines the service names, which will be used for DNS
  lookup on the internal network, and service dependencies.

You can build all services referenced in the compose file from the command
line::

 > docker-compose build

Then, a basic "up" command will launch the suite::

 > docker-compose up

Once the suite is running, you can verify several endpoints:

* The root endpoint "/" will route (by default) to the "user" service (see
  lines 9 and 13 of the reverse-proxy configuration, "nginx.conf").

* The "/user" endpoint will route to the "user-svc" service.

* The "/wsgi" endpoint will route to the "wsgi-svc" service.

* The "/wsgi/getFoo" endpoint will return an entry, through logic within the
  "wsgi-svc" service, stored in the "data-svc" Redis database.
