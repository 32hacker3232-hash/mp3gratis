from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app) # Esto es vital para que la web no dé error de conexión

# --- TU MOTOR DE DESCARGA (SIN CAMBIOS EN LA LÓGICA) ---
def motor_de_descarga(url, tipo):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ydl_opts = {
        'noplaylist': True,
        'restrictfilenames': False,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    if tipo == "1":
        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
    else:
        ydl_opts['format'] = 'best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos la info y descargamos
            info = ydl.extract_info(url, download=True)
            archivo_original = ydl.prepare_filename(info)
            
            if tipo == "1":
                nombre_final = os.path.splitext(archivo_original)[0] + ".mp3"
                if os.path.exists(nombre_final): os.remove(nombre_final)
                os.rename(archivo_original, nombre_final)
                return {"status": "success", "file": nombre_final, "title": info.get('title', 'Audio')}
            
            return {"status": "success", "file": archivo_original, "title": info.get('title', 'Video')}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- RUTAS PARA QUE LA WEB FUNCIONE ---
@app.route('/convertir', methods=['POST'])
def convertir():
    data = request.json
    url = data.get('url')
    tipo = data.get('tipo') 
    
    print(f"Solicitud recibida: {url} (Tipo: {tipo})")
    resultado = motor_de_descarga(url, tipo)
    
    if resultado['status'] == 'success':
        return jsonify(resultado)
    else:
        return jsonify(resultado), 500

@app.route('/descargar_archivo')
def descargar_archivo():
    path = request.args.get('path')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Archivo no encontrado", 404

if __name__ == "__main__":
    # IMPORTANTE: Ya no usamos input(), Flask se encarga de recibir los datos
    print("========================================")
    print("SERVIDOR TUBE SYNC ACTIVO")
    print("No cierres esta ventana.")
    print("Ahora ve a tu navegador y usa la web.")
    print("========================================")
    app.run(debug=True, port=5000)