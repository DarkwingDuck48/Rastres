from cx_Freeze import setup, Executable

exe = Executable(script="mainCore.py", base="Win32GUI")
setup(name="FindRaster",
      version="1.1",
      description="Поиск номера растра по координатам введенным либо вручную, либо подгруженным из DXF файла",
      author="Max",
      author_email="ex@example.ru",
      executables=[exe])

