# RealityDiff

AI-powered real-time scene change analyzer.

Detect what was:
🟢 ADDED
🟡 MOVED
🔴 REMOVED

## Tech Stack

- YOLO26
- BoT-SORT
- OpenCV
- Python
- Supabase
- Streamlit

## Architecture

Camera
↓
YOLO26
↓
BoT-SORT
↓
Scene State
↓
Temporal Memory
↓
Change Detection
↓
Supabase
↓
Streamlit Dashboard