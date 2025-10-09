#!/usr/bin/env python3
"""Start backend and capture initial output"""
import subprocess
import sys
import time

try:
    print("Starting backend...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Capture first 50 lines or until startup complete
    lines_captured = 0
    startup_complete = False
    
    for line in process.stdout:
        print(line, end='')
        lines_captured += 1
        
        if "Application startup complete" in line:
            startup_complete = True
            print("\n✅ Backend started successfully!")
            break
        
        if "error" in line.lower() or "exception" in line.lower():
            print(f"\n❌ Error detected on line {lines_captured}")
        
        if lines_captured >= 100:
            print(f"\n⚠️ Captured {lines_captured} lines, stopping capture...")
            break
    
    if startup_complete:
        print("\n🚀 Backend is running on http://localhost:8000")
        print("Press Ctrl+C to stop")
        process.wait()
    else:
        print("\n⏳ Startup did not complete in captured output")
        process.terminate()
        
except KeyboardInterrupt:
    print("\n\n⏹️ Backend stopped by user")
    process.terminate()
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

