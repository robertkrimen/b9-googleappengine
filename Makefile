.PHONY: test

test:
	PYTHONPATH=lib:appengine:google_appengine:google_appengine/lib/yaml/lib:google_appengine/lib/webob:google_appengine/lib/django py.test pyt/*.py
