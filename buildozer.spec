[app]
title = Noche de Película
package.name = nochedepelicula
package.domain = com.nicolasjaeline
source.dir = .
source.include_exts = py,json,png,jpg,kv
version = 1.0.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

# Android
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET
android.private_storage = True
android.allow_backup = True
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
