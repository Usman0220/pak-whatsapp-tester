[app]
title = tester6 APK demo
package.name = tester6demo
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,atlas
source.include_patterns = tester6.py
version = 0.1.0
orientation = portrait
fullscreen = 0

# Full network workflow requirements
# aiohttp and its deps + SSL and certs
requirements = python3,kivy,aiohttp,openssl,certifi,yarl,multidict,async-timeout,aiosignal,frozenlist,attrs,setuptools

# This will create an APK
android.archs = arm64-v8a, armeabi-v7a
android.api = 31
android.minapi = 21
android.sdk = 0
android.ndk = 25b
android.numeric_version = 1

# Permissions required for network access
android.permissions = INTERNET

# Icons (optional)
icon.filename =

# Logging
log_level = 1

[buildozer]
log_level = 2
# Use the docker image for reproducible builds
use_docker = 1
docker_image = kivy/buildozer