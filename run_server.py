import uvicorn
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_server.py [local|server]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "local":
        host = "127.0.0.1"
        print("Starting server in local (127.0.0.1:8000)")
    elif mode == "server":
        host = "0.0.0.0"
        print("Starting server in server mode (0.0.0.0:8000)")
    else:
        print(f"Invalid mode: {mode}")
        print("Usage: python run_server.py [local|server]")
        sys.exit(1)
    
    uvicorn.run("server.main:app", host=host, port=8000, reload=True)
    