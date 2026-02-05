# EchoHola

EchoHola is a project designed to recognize people and greet them personally by name. The main goal is to create a natural and friendly interaction between humans and systems by combining person recognition with voice feedback.

The system identifies an individual using recognition technologies (such as facial recognition, voice recognition, or other identification methods) and automatically generates a personalized greeting like “Hello, Salvador.” This approach enhances user experience and makes interactions feel more human and engaging.

EchoHola can be applied in different environments, including offices, schools, smart homes, or access-controlled areas, where welcoming users in a personalized way adds value. The project is modular and extensible, allowing different recognition methods and voice engines to be integrated easily.

Overall, EchoHola aims to demonstrate how recognition technologies and speech synthesis can work together to create simple, friendly, and intelligent greeting systems.

## Prerequisites

Before running EchoHola, ensure you have the following installed:
- **Docker & Docker Compose** (to run the DeepFace API)
- **Python 3** (to run the recognition script)
- **Required Python Libraries**: `pip install requests`
- **EchoVoice**: The custom voice engine used for greetings.

## Getting Started

### 1. Start the DeepFace Service
Use Docker Compose to launch the recognition engine in the background:
```bash
docker compose up -d
```

### 2. Configure the Face Database
Create a folder structure inside the `db/` directory. Each subfolder should be named after the person and contain one or more clear photos of their face:
```text
db/
├── salvador/
│   └── photo1.jpg
└── unknown/
```

## Usage

To recognize a person from a new image and greet them personally:

```bash
python3 recognize.py path/to/your_capture.jpg
```

The script will:
1. Extract the face from the provided image.
2. Query the DeepFace service to find a match in the `db/` folder.
3. Use `echovoice` to greet the identified person by name.
