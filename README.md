# EchoHola 🎥🔊

EchoHola is a facial recognition system that greets people by voice when they are identified through a webcam or an image. 

It uses **DeepFace** (running in Docker) for recognition and **Flask** for the web interface.

## 🛠️ Prerequisites

Before running EchoHola, ensure you have:
- **Docker & Docker Compose**
- **Python 3.10+**
- **`echovoice`** installed and available in your PATH (for voice greetings).

## 🚀 Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd EchoHola
   ```

2. **Start DeepFace API**:
   The recognition backend runs in a Docker container.
   ```bash
   docker compose up -d
   ```

3. **Create a Python Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### 🌐 Web Interface (Recommended)
The easiest way to use EchoHola is via the web interface which captures images from your webcam in real-time.

1. **Run the Flask app**:
   ```bash
   python3 app.py
   ```
2. Open [http://localhost:5000](http://localhost:5000) in your browser.
3. Click **"Capture & Verify"**.

### 💻 CLI Recognition
You can also run recognition on a specific image file:
```bash
python3 recognize.py path/to/image.jpg
```

## 📂 Database Configuration
Add photos of people you want to recognize in the `db/` directory, organized by name. Each subfolder should be named after the person:

```text
db/
├── salvador/
│   ├── photo1.jpg
│   └── photo2.jpg
├── joan/
│   └── me.png
└── unknown/
```

## 🛑 Stopping the System

To stop the recognition service, run:
```bash
docker compose down
```
