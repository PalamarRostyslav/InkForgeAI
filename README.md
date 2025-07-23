# 🎨 AI Tattoo Generator - InkForgeAI

A sophisticated desktop application that combines AI-powered tattoo design generation with intelligent image analysis, built with PyQt6 and featuring a modern Claude-inspired dark theme interface.

## ✨ Features

### 🖼️ AI-Powered Tattoo Generation
- **DALL-E 3 Integration**: Generate unique, professional tattoo designs from text descriptions
- **Multiple Sizes**: Choose from Square (1024×1024), Portrait (1024×1792), or Landscape (1792×1024)
- **Quality Options**: Standard or HD quality for different levels of detail
- **Context-Aware Generation**: Each new design can build upon previous requests in the same session

### 💬 Smart Conversation System
- **Session Management**: Create multiple chat sessions with custom names
- **Conversation History**: All prompts and generated images are saved per session
- **Context Indicators**: Visual indicators show when previous requests are being considered
- **Iterative Design**: Refine your tattoo by adding details through conversation
  - Example: "Dragon tattoo" → "Add flames" → "Make it wrap around the arm"

### 🔍 AI-Powered Image Analysis
- **Claude Integration**: Analyze any generated tattoo to understand its deeper meaning
- **Comprehensive Analysis**:
  - Symbolism & meaning interpretation
  - Artistic style identification (traditional, neo-traditional, realism, etc.)
  - Cultural and historical significance
  - Design element breakdown
  - Personal interpretation and emotional context
- **In-Chat Results**: Analysis appears directly in your conversation history

### 🗂️ Gallery & Organization
- **Visual Gallery**: Browse all generated tattoos in a session
- **Image Export**: Save any tattoo design to your desired location
- **Automatic Organization**: Images are stored by session for easy retrieval
- **Thumbnail Preview**: Quick visual overview with prompt descriptions

### 🎯 Session Management
- **Multiple Sessions**: Work on different tattoo ideas in separate conversations
- **Session Switching**: Easily switch between different design projects
- **Delete Sessions**: Remove unwanted sessions with all associated data
- **Persistent Storage**: All sessions are saved and restored on app restart

### 🌙 Clear Interface
- **AI Chat-Inspired Design**: Clean, dark theme optimized for long design sessions
- **Responsive Layout**: Adjustable panels for chat, gallery, and controls
- **Smooth Animations**: Hover effects and transitions for better UX
- **Async Architecture**: Non-blocking operations ensure smooth performance

### UI Screenshots

<img width="1918" height="1029" alt="image" src="https://github.com/user-attachments/assets/e753a1fe-4eec-4349-85fc-7fa8b291a0fe" />
<img width="1919" height="672" alt="image" src="https://github.com/user-attachments/assets/ceb2dc89-232a-4250-94bc-01ab2cde3f43" />
<img width="1915" height="1032" alt="image" src="https://github.com/user-attachments/assets/6573d137-c760-4b67-aac2-39cb83ef750f" />
<img width="1919" height="1022" alt="image" src="https://github.com/user-attachments/assets/a03f7e40-55e6-4297-878a-c202b860f616" />
<img width="1140" height="896" alt="image" src="https://github.com/user-attachments/assets/464db7a4-90a3-450a-8e46-ee465724e7a8" />
<img width="1919" height="1031" alt="image" src="https://github.com/user-attachments/assets/e98c8fac-2bdd-4421-93c2-17716d6a430d" />

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (required for image generation)
- Anthropic API key (optional, for image analysis)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/PalamarRostyslav/InkForgeAI.git
cd InkForgeAI
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure API keys**:

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # Optional
```

5. **Run the application**:
```bash
python main.py
```

## 📖 How to Use

### Creating Your First Tattoo

1. **Start a New Session**: Click "+ New Chat" and give it a name
2. **Describe Your Vision**: Type your tattoo idea in the input field
3. **Customize Settings**: 
   - Select image size based on placement (portrait for arms, landscape for back)
   - Choose quality (HD for detailed designs)
4. **Generate**: Press Enter or click "Generate"
5. **Iterate**: Add more details in subsequent prompts to refine the design

### Analyzing Your Tattoo

1. **Select a Design**: Navigate to any generated tattoo in the gallery
2. **Click Analyze**: Press the blue "Analyze" button
3. **Read Insights**: Get detailed interpretation of symbolism, style, and meaning
4. **Save Analysis**: The analysis becomes part of your conversation history

### Managing Sessions

- **Switch Sessions**: Click any session in the sidebar to load its history
- **Delete Sessions**: Hover over a session and click the 🗑️ button
- **Export Images**: Click "Export" on any gallery image to save it

### Pro Tips

- **Building Complexity**: Start simple and add elements gradually
  - "Minimalist wolf" → "Add geometric patterns" → "Include moon phases"
- **Style Consistency**: Mention the style in your first prompt for cohesive designs
  - "Traditional Japanese dragon" ensures consistent aesthetic
- **Contextual Refinement**: Reference previous elements naturally
  - "Make the flames more prominent" → "Add smoke effects to the flames"

## 🛠️ Technical Details

### Architecture

- **Backend Services**:
  - `OpenAIService`: Handles DALL-E 3 API integration
  - `ChatService`: Manages sessions and conversation history
  - `TattooAnalysisMCP`: Integrates Claude for image analysis
  
- **Frontend Components**:
  - `ChatArea`: Displays conversation with images
  - `ChatSidebar`: Session management interface
  - `ImageGallery`: Thumbnail grid with actions
  - `InputWidget`: Prompt input with options

- **Storage**:
  - SQLite database for metadata and conversations
  - File system for image storage
  - Organized by session ID for easy management

### Key Technologies

- **PyQt6**: Modern Qt bindings for Python
- **OpenAI API**: DALL-E 3 for image generation
- **Anthropic API**: Claude for image analysis
- **SQLite**: Lightweight database for persistence
- **Async/Await**: Non-blocking operations throughout

## 🎨 Use Cases

### Professional Tattoo Artists
- Generate reference designs for client consultations
- Explore variations quickly before drawing
- Understand symbolism to better advise clients

### Tattoo Enthusiasts
- Visualize ideas before committing
- Explore different styles and compositions
- Understand the meaning behind design elements

### Creative Exploration
- Experiment with unconventional combinations
- Build complex designs iteratively
- Learn about different tattoo traditions

## 🔧 Configuration

### Image Generation Settings

- **Sizes**: Optimized for different body placements
- **Quality**: Balance between detail and generation speed
- **Context Window**: Maintains full conversation history

### Analysis Options

- **Model**: claude-3-haiku
- **Focus Areas**: Symbolism, style, culture, composition
- **Integration**: Seamless in-chat experience

---
