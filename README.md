# AI Chatbot 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Cohere](https://img.shields.io/badge/Cohere-API-0052CC)](https://cohere.com/)

A simple web-based AI chatbot application built with Flask and Cohere API. Engage in natural conversations with an AI powered by advanced language models.

<img width="1895" height="928" alt="Image" src="https://github.com/user-attachments/assets/54dd5b32-7913-446e-bd53-7eae33eb47ee" />

## ✨ Features

- 💬 Interactive web interface for chatting with AI
- 🧠 Powered by Cohere's advanced language models
- 📱 Responsive design with Bootstrap
- 🔒 Secure form handling with Flask-WTF
- 🎨 Customizable bot image background
- ⚡ Fast and lightweight

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Cohere API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishwaswami24/ai-chatbot.git
   cd ai-chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Cohere API key:**
   - Get your API key from [Cohere](https://cohere.ai/)
   - Create `local_settings.py` (recommended):
     - Copy `local_settings.example.py` to `local_settings.py`
     - Set `COHERE_API_KEY = "..."` and (optionally) tweak the model settings
   - Or set an environment variable:
     - `COHERE_API_KEY=...`

### Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Start chatting!**
   Enter your prompt in the text field and click "Generate Response"

## 📁 Project Structure

```
ai-chatbot/
├── app.py                 # Main Flask application
├── templates/
│   └── home.html          # Main template
├── static/
│   └── bot.webp           # Bot image
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🛠️ Technologies Used

- **[Flask](https://flask.palletsprojects.com/)**: Web framework
- **[Cohere API](https://cohere.ai/)**: AI language model
- **[Flask-WTF](https://flask-wtf.readthedocs.io/)**: Form handling
- **[Bootstrap](https://getbootstrap.com/)**: CSS framework
- **[Font Awesome](https://fontawesome.com/)**: Icons

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Cohere](https://cohere.ai/) for providing the AI API
- [Bootstrap](https://getbootstrap.com/) for the UI framework
- [Flask](https://flask.palletsprojects.com/) for the web framework

