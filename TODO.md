# TODO List

## First Steps: Core Functionality

1. **Speech-to-Text (STT) Integration**
   - Research and select a local/offline STT engine (e.g., Vosk, Whisper, DeepSpeech).
   - Implement a basic interface to capture voice input and convert it to text.
   - Test STT accuracy and performance on your hardware.

2. **Text-to-Speech (TTS) Integration**
   - Research and select a local/offline TTS engine (e.g., Coqui TTS, eSpeak, Piper).
   - Implement a basic interface to convert assistant responses to speech.
   - Test TTS voice quality and configuration.

3. **Local Chatbot Setup**
   - Choose a local LLM or rule-based chatbot framework (e.g., llama.cpp, GPT4All, Rasa).
   - Integrate the chatbot with the STT and TTS interfaces.
   - Enable basic conversational loop: voice input → text → chatbot → voice output.

4. **Vector Database for Knowledge Storage**
   - Research local vector database options (e.g., ChromaDB, Qdrant, Milvus).
   - Set up the database and test storing/retrieving simple text entries.

---

## Next Steps: Expanding Capabilities

5. **Knowledge Ingestion**
   - Implement ingestion pipelines for text, photos, voice, and video.
   - Add metadata tagging and basic search functionality.

6. **Personal Knowledge Repository**
   - Design a schema for organizing and categorizing knowledge entries.
   - Add CRUD (Create, Read, Update, Delete) operations for knowledge items.

7. **TODO List and Calendar Integration**
   - Design and implement a simple TODO/task manager.
   - Integrate a local calendar (e.g., via ical or CalDAV).
   - Enable voice commands for adding/removing tasks and events.

8. **User Interface**
   - Consider a minimal GUI or web interface for manual input and review.
   - Optionally, add notifications or reminders.

9. **Privacy & Security**
   - Ensure all data is stored locally and securely.
   - Add user authentication if needed.

---

## Long-Term / Future Features

- Multi-modal knowledge linking (e.g., relate a photo to a text note).
- Advanced search and summarization across all knowledge types.
- Daily/weekly journal recap via voice.
- Integration with external APIs (weather, news, etc.) if desired.
- Mobile or remote access options.
