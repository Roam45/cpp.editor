from flask import Flask, request, send_file, jsonify
import os
import subprocess

app = Flask(__name__)

# Folder to store temporary files
TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route("/compile", methods=["POST"])
def compile_code():
    """
    Endpoint to compile C++ code and return the compiled executable.
    """
    data = request.json
    code = data.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # File paths for temporary files
    cpp_file = os.path.join(TEMP_FOLDER, "temp_code.cpp")
    exe_file = os.path.join(TEMP_FOLDER, "program.exe")

    # Save the code to a temporary .cpp file
    try:
        with open(cpp_file, "w") as f:
            f.write(code)
    except Exception as e:
        return jsonify({"error": f"Failed to save code: {str(e)}"}), 500

    # Compile the code using g++
    try:
        result = subprocess.run(
            ["g++", cpp_file, "-o", exe_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 400
    except Exception as e:
        return jsonify({"error": f"Compilation failed: {str(e)}"}), 500

    # Return the compiled .exe file
    if os.path.exists(exe_file):
        return send_file(exe_file, as_attachment=True)
    else:
        return jsonify({"error": "Compilation failed, no executable created"}), 500

@app.route("/")
def home():
    return "C++ Compiler Backend is Running!"

if __name__ == "__main__":
    app.run(debug=True)

