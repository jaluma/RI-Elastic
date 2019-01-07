import subprocess
import importlib
import sys

import json

def install_and_import(package, module_name=""):
    if module_name == "":
        module_name = package

    try:
        __import__(module_name)
    except ImportError:
        print("Instalando paquetes necesarios...")
        subprocess.call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        module = importlib.import_module(module_name)

        globals().update(
            {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
            else 
            {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
        })

def serializer(results, filename):
    with open(filename, 'w') as outfile:
        json.dump(results, outfile, sort_keys=True, indent=3)
    print("Cargados correctamente los resultados.\n")
