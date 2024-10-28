from app import app
from config import Config

print(f'DATABASE: {Config.DATABASE}')
print(f'HOST: {Config.HOST}')
print("SERVER BERHASIL DIJALANKAN")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)

