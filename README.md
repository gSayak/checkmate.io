# Checkmate.io

**Checkmate.io** is an API service designed to facilitate interactions between experts and consumers. It provides a platform where experts can register, create services, and manage bookings, while consumers can browse services, book sessions, and send priority messages.

## Features

- **JWT Authentication** for experts
- **Service Creation** with customizable types and durations
- **Booking System** with unique ID generation for tracking
- **Priority Messaging** for consumers to directly communicate with experts

## Endpoints

### For Experts:
- **`POST /api/experts/`** - Register new experts.
- **`POST /api/login`** - Login to an expert account and receive a JWT.
- **`POST /api/services/`** - Create new services after logging in.
- **`GET /api/get-status`** - Check all bookings made for an expert’s services.
- **`GET /api/bookings/messages/?<booking_id>`** - Retrieve messages sent in priority DMs using a booking ID.

### For Consumers:
- **`POST /api/bookings`** - Book a service by an expert.
- **`GET /api/experts-services`** - View all experts and their services.
- **`POST /api/bookings/send-message`** - Send a priority message using your booking ID.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gSayak/checkmate.io.git
   ```
2. Add a `.env` file with the supabase.com:
   ```
   DATABASE_URI: <Database URI>
   ```
3. Start the app using:
  ```bash
  python -m api.index  
  ```
