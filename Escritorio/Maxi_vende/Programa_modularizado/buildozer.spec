[app]

title = Kompra Venta
package.name = komproventa
package.domain = org.juandominguez

source.dir = .

# Extensiones para incluir
source.include_exts = py,kv,png,jpg,jpeg,db,ttf,txt,json

# Carpetas adicionales
source.include_patterns = assets/*,images/*.png,fuentes/*,database/*,actualizaciones/*

# Versión de la app (cada actualización aumentá esto: 1.0.1, 1.0.2...)
version = 1.0.0

# Requisitos
requirements = python3,kivy,requests

# Presplash e icono
presplash.filename = images/carrito_compras.png
icon.filename = images/carrito_compras.png

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.wakelock = True

# Arquitecturas (ambas: 64 y 32 bits)
android.archs = arm64-v8a, armeabi-v7a


# ===== FIRMA ANDROID =====
android.release_keystore = my-release-key.keystore
android.release_keyalias = androidreleasekey
android.release_keystore_pass = juankompraventa123
android.release_keyalias_pass = juankompraventa123

# Formato final del release:
android.release_artifact = apk

#
# iOS — ignorar
#

[buildozer]
log_level = 2
warn_on_root = 1
