import os

os.environ.pop("DJANGO_SETTINGS_MODULE", None)
os.environ["DJANGO_SETTINGS_MODULE"] = "planetarium_api.settings_test"
os.environ.setdefault("SECRET_KEY", "test-secret-key")
