# update/installer.py
import android #type: ignore
from jnius import autoclass, cast #type: ignore

def instalar_apk(path):
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        Intent = autoclass('android.content.Intent')
        context = PythonActivity.mActivity

        file = File(path)
        uri = Uri.fromFile(file)
        intent = Intent(Intent.ACTION_VIEW)
        intent.setDataAndType(uri, "application/vnd.android.package-archive")
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        context.startActivity(intent)
    except Exception as e:
        print("Error al iniciar la instalación:", e)
