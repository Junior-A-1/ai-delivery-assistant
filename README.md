# AI Delivery Communication System 

A full-stack mobile + backend system that improves communication between delivery drivers and customers.

## Features

- Real-time driver status updates
- Location-aware responses
- ETA extraction using regex
- AI-ready architecture (OpenAI integration prepared)

## Tech Stack

- React Native (Mobile App)
- FastAPI (Backend)
- Regex + Rule-Based Logic

## Example

Customer: "Where is my order?"

Response:
Driver is near Sydney CBD. Your rider reported: "Restaurant will take 25 minutes". Estimated delivery time is 25 minutes.

## Setup

### Backend

```bash
pip install fastapi uvicorn
python -m uvicorn main:app --reload
```

### Mobile App 
```bash
cd mobile-app/AIDelivery
npm install
npx react-native run-android
```

## Note
OpenAI and Google Maps integrations are implemented but currently commented out to avoid API costs during development. The system is designed to be AI-ready and can be enabled anytime.