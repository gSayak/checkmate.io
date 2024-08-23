# Checkmate.io ♕

---

[Checkmate.io](http://checkmate.io/) is an API service that facilitates interactions between experts and consumers. It offers endpoints for expert registration, login, service creation, and booking management. Consumers can browse available services, book sessions, and send priority messages. The system supports both video meetings and priority direct messages. Key features include JWT authentication for experts, service creation with customizable types and durations, and a booking system that generates unique IDs for tracking. The API also allows experts to view their bookings and check messages from priority DMs, providing a comprehensive platform for managing expert-consumer interactions.

# Features:

1. Authentication using JWT
2. Comprehensive platform for managing expert-consumer interactions
3. Validation using pydantic 
4. Database hosted using supabase.com

# Links:

[Github](http://Github.com) :

 https://github.com/gSayak/checkmate.io

Postman Collection: 

[https://checkmate-0060.postman.co/workspace/Checkmate-Workspace~0c28f72b-094d-4fc1-8ae8-f60d2d991784/collection/37486291-88bf9ade-bbd5-48c8-9a0a-3bf2089bf945?action=share&source=collection_link&creator=37486291](https://checkmate-0060.postman.co/workspace/Checkmate-Workspace~0c28f72b-094d-4fc1-8ae8-f60d2d991784/collection/37486291-88bf9ade-bbd5-48c8-9a0a-3bf2089bf945?action=share&source=collection_link&creator=37486291)"

## Endpoints :

### For Experts :

1. `/api/experts/`  - To register new experts
2. `/api/login` - To login into experts account to get the JWT to
3. `/api/services/` - To create new services once logged in
4. `/api/get-status` - To check all the bookings made for an experts services
5. `/api/bookings/messages/[?booking_id=](https://checkmateio.vercel.app/api/bookings/messages/?booking_id=)<booking_id>` - To check the messages sent in priority dm using booking id

### For Consumers:

1. `/api/bookings` - For Consumers to book a service by expert
2. `/api/experts-services` - To check all the experts and all the services
3. `/api/bookings/send-message` - To send a priority dm using your booking ID
4. `/` - The base url

# The working of the APIs 🤗

1. Registering as an expert: 

To register as an expert we go to :

url :  [`https://checkmateio.vercel.app/api/experts/`](https://task-one-lyart.vercel.app/api/experts/) 

method : POST

body:

```bash
{
    "name": "Sayak Ghosh", 
    "email": "gsayak@gmail.com", 
    "password": "topmateisbest", 
    "bio": "Django Engineer", 
    "profile_picture_url": "http://example.com/sayak.jpg"
}
```

response : 

```bash
{
    "email": "gsayak22@gmail.com",
    "id": "63c144ec-f83e-4361-ba29-ccd8b41aaba4",
    "name": "Sayak Ghosh 2"
}
```

---

1. Log in into this account to gather the JWT token

url : [`https://checkmateio.vercel.app/api/login/`](https://checkmateio.vercel.app/api/login/)

method : POST

body :

```json
{
    "email": "gsayak22@gmail.com", 
    "password": "topmateisbest"
}
```

response:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDQwNTAyNiwianRpIjoiOTcwMTE0OWYtODkzZC00NTZlLTg2NWUtYTBiOGEwNDRhNmM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYzYzE0NGVjLWY4M2UtNDM2MS1iYTI5LWNjZDhiNDFhYWJhNCIsIm5iZiI6MTcyNDQwNTAyNiwiY3NyZiI6ImNhNmFlNTE1LTA0M2UtNDVkNS05NzgzLTU2ZmJhZmJiYWNmMiIsImV4cCI6MTcyNDQwNTkyNn0.Frtvk7eWk8Lfk644kW2X-Wnynbr0GPi301UunGnEepY"
}
```

Now that we got the JWT token, we can use this to create services

---

1. Creating a service when logged in 

url : [`https://checkmateio.vercel.app/api/services/`](https://checkmateio.vercel.app/api/services/)

method: POST

body:

```json
{
    "service_type": "priority_dm", 
    "title": "AI Consultation", 
    "description": "Contact Me",
    "price": 150.0, 
    "duration": 30
}
```

Here, the service_type can either be “priority_dm” or “video_meeting” and the JWT token we got from the previous response need to be sent as the AUTH token along with the request.

<aside>
💡 Auth : <JWT TOKEN>

</aside>

response:

```json
{
    "id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
    "service_type": "priority_dm",
    "title": "AI Consultation"
}
```

This would create a service called `AI Consultation` along with a service ID, which would be used by consumers to book their services. 

---

1. Customer checking all the available services

Now the customer can come and check out whatever services are provided by the different experts, to do so:

url: [`https://checkmateio.vercel.app/api/experts-services`](https://checkmateio.vercel.app/api/experts-services)

method: GET

response: 

```json
[
    {
        "expert_bio": "Expert in AI",
        "expert_name": "John Doe",
        "profile_picture_url": "http://example.com/john.jpg",
        "services": [
            {
                "description": "A 30-minute AI consultation session",
                "duration": 30,
                "price": 150.0,
                "service_id": "c7cf2c86-7b1f-43e3-ab00-804ca3448986",
                "service_type": "video_meeting",
                "title": "AI Consultation"
            },
            {
                "description": "Priority DM!",
                "duration": 30,
                "price": 150.0,
                "service_id": "76367e32-9733-4eb9-83fa-67a843ebf21f",
                "service_type": "priority_dm",
                "title": "AI Consultation"
            }
        ]
    },
    {
        "expert_bio": "AI Specialist",
        "expert_name": "Dohn Joe",
        "profile_picture_url": "http://example.com/john.jpg",
        "services": [
            {
                "description": "A 30-minute AI consultation session",
                "duration": 30,
                "price": 150.0,
                "service_id": "bf667916-3909-4f0e-8c99-a2f29057c252",
                "service_type": "video_meeting",
                "title": "AI Consultation"
            }
        ]
    },
    {
        "expert_bio": "Django Engineer",
        "expert_name": "Sayak Ghosh 2",
        "profile_picture_url": "http://example.com/sayak.jpg",
        "services": [
            {
                "description": "Contact Me",
                "duration": 60,
                "price": 150.0,
                "service_id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
                "service_type": "priority_dm",
                "title": "AI Consultation"
            }
        ]
    }
]
```

---

1. Booking a video service

Now suppose the customer wants to do a video session with `Don Joe`

```json
    {
        "expert_bio": "AI Specialist",
        "expert_name": "Don Joe",
        "profile_picture_url": "http://example.com/john.jpg",
        "services": [
            {
                "description": "A 30-minute AI consultation session",
                "duration": 30,
                "price": 150.0,
                "service_id": "bf667916-3909-4f0e-8c99-a2f29057c252",
                "service_type": "video_meeting",
                "title": "AI Consultation"
            }
        ]
    }
```

The customer can check that the service id is `"bf667916-3909-4f0e-8c99-a2f29057c252"`

Then he can use this service id to book a session using :

url : [`https://checkmateio.vercel.app/api/bookings/`](https://checkmateio.vercel.app/api/bookings/)

method: POST

body:

```json
{
    "service_id": "bf667916-3909-4f0e-8c99-a2f29057c252",
    "user_email": "customer@gmail.com"
}
```

response:

```json
{
    "expiry_time": "Sun, 25 Aug 2024 09:40:28 GMT",
    "id": "de0a6736-8fb0-4c2b-84f2-8e407bcbfe26",
    "service_id": "bf667916-3909-4f0e-8c99-a2f29057c252",
    "status": "pending",
    "user_email": "customer@gmail.com"
}
```

The customer just uses his own `email id` and the `service-id` for booking a service, and he will get a `booking ID` for his reservation.

---

1. Booking a priority_dm 

Now suppose the customer wanted to book a priority_dm of  `Sayak Ghosh`

```json
{
        "expert_bio": "Django Engineer",
        "expert_name": "Sayak Ghosh",
        "profile_picture_url": "http://example.com/sayak.jpg",
        "services": [
            {
                "description": "Contact Me",
                "duration": 60,
                "price": 150.0,
                "service_id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
                "service_type": "priority_dm",
                "title": "AI Consultation"
            }
        ]
    }
```

Now again he notes down the service_id for the priority_dm `"1a28f64f-61c4-434e-8d21-86c82fc83ff1"` 

Then he can use this service id to book a session using :

url: [`https://checkmateio.vercel.app/api/bookings/`](https://checkmateio.vercel.app/api/bookings/)

method: POST

body:

```json
{
    "service_id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
    "user_email": "customer@gmail.com"
}
```

response:

```json
{
    "expiry_time": "Sun, 25 Aug 2024 09:46:51 GMT",
    "id": "b92686ca-c653-44a2-8624-6302f2835a9e",
    "service_id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
    "status": "pending",
    "user_email": "customer@gmail.com"
}
```

Now the booking has been done , the customer can use this `booking-id` to send a priority dm to the expert

---

1. Sending a priority dm to an expert

After booking and receiving the `booking-id`, the user can send it using:

url: [`https://checkmateio.vercel.app/api/bookings/send-message/`](https://checkmateio.vercel.app/api/bookings/send-message/)

method: POST

body:

```json
{
  "booking_id": "b92686ca-c653-44a2-8624-6302f2835a9e",
  "message": "Please hire me!!."
}
```

response:

```json
{
    "booking_id": "b92686ca-c653-44a2-8624-6302f2835a9e",
    "id": "e3509c68-b325-458a-8df7-db4d50eab1c7",
    "message": "Please hire me!!.",
    "sent_at": "Fri, 23 Aug 2024 09:49:55 GMT"
}
```

---

1. Expert checking all the bookings done on his services

Now the expert can check later on who has booked his services using :

url: `https://checkmateio.vercel.app/api/get-status/`

method: GET

<aside>
💡 Auth: <JWT TOKEN>

</aside>

response:

```json
[
    {
        "booking_time": "Fri, 23 Aug 2024 09:46:51 GMT",
        "expiry_time": "Sun, 25 Aug 2024 09:46:51 GMT",
        "id": "b92686ca-c653-44a2-8624-6302f2835a9e",
        "service_id": "1a28f64f-61c4-434e-8d21-86c82fc83ff1",
        "service_title": "AI Consultation",
        "service_type": "priority_dm",
        "status": "pending",
        "user_email": "customer@gmail.com"
    }
]
```

The expert can check the booking time, expiry time, the user email of who has booked and which service he has booked.

---

1. Checking the messages in case of priority_dms

The expert can check what message has been sent to him in priority_dms using :

url: [`https://checkmateio.vercel.app/api/bookings/messages/?booking_id=](https://checkmateio.vercel.app/api/bookings/messages/?booking_id=)<booking_id>`

method: GET

params: booking_id

For example, 

url: [`https://checkmateio.vercel.app/api/bookings/messages/?booking_id=b92686ca-c653-44a2-8624-6302f2835a9e`](https://task-one-lyart.vercel.app/api/bookings/messages/?booking_id=b92686ca-c653-44a2-8624-6302f2835a9e) 

response: 

```json
[
    {
        "booking_id": "b92686ca-c653-44a2-8624-6302f2835a9e",
        "id": "e3509c68-b325-458a-8df7-db4d50eab1c7",
        "message": "Please hire me!!.",
        "sent_at": "Fri, 23 Aug 2024 09:49:55 GMT"
    }
]
```

---

# To-do List

- [ ]  Making document accesible, where experts can upload a doc and whenever someone books that, the user is sent a mail of the document
- [ ]  Another endpoint where experts can accept the video meetings and that would send an email with the meet link to the user email.