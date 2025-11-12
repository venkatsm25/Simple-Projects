# Mook Mitra - Text-to-Speech Handler
def speak(text, wait_for_completion=False):
    """
    Speaks text using the OS's native voice.
    """
    import sys
    import subprocess

    if not text or not isinstance(text, str):
        return

    command = ''
    if sys.platform == 'win32':
        # Sanitize text for PowerShell command
        sanitized_text = text.replace("'", "''")
        command = f'powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{sanitized_text}\');"'
    elif sys.platform == 'darwin': # macOS
        command = ['say', text]
    else: # Linux
        command = ['espeak', text]

    # Use run() for waiting, Popen() for non-blocking
    if wait_for_completion:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)