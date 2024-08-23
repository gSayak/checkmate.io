from flask import Flask, request, jsonify
from pydantic import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from api.models.expert import Expert
from api.models.service import Service
from api.models.booking import Booking
from api.models.message import Message
from api.models import db
from api.schemas import ExpertCreateSchema, ServiceCreateSchema, BookingCreateSchema, MessageCreateSchema


def register_routes(app):

    # Route for registering new experts
    @app.route('/api/experts/', methods=['POST'])
    def register_expert():
        data = request.get_json()
        try:
            validated_data = ExpertCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        expert = Expert(
            name=validated_data.name,
            email=validated_data.email,
            bio=validated_data.bio,
            profile_picture_url=validated_data.profile_picture_url
        )
        expert.set_password(validated_data.password)
        db.session.add(expert)
        db.session.commit()
        return jsonify({
            'id': str(expert.id),
            'name': expert.name,
            'email': expert.email
        }), 201

    # Route for registering a new service
    @app.route('/api/services/', methods=['POST'])
    @jwt_required()  
    def create_service():
        current_expert_id = get_jwt_identity()  
        data = request.get_json()
        try:
            validated_data = ServiceCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        service = Service(
            expert_id=current_expert_id,  
            service_type=validated_data.service_type,
            title=validated_data.title,
            description=validated_data.description,
            price=validated_data.price,
            duration=validated_data.duration
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({
            'id': str(service.id),
            'service_type': service.service_type,
            'title': service.title
        }), 201

    @app.route('/api/bookings/', methods=['POST'])
    def book_service():
        data = request.get_json()
        try:
            validated_data = BookingCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        service = Service.query.get(validated_data.service_id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        booking_time = datetime.utcnow()
        expiry_time = datetime.utcnow() + timedelta(days=2)

        booking = Booking(
            service_id=service.id,
            user_email=validated_data.user_email,
            booking_time=booking_time,
            expiry_time=expiry_time
        )
        db.session.add(booking)
        db.session.commit()

        return jsonify({
            'id': str(booking.id),
            'service_id': str(booking.service_id),
            'user_email': booking.user_email,
            'status': booking.status,
            'expiry_time': booking.expiry_time
        }), 201

    # Route for checking bookings made by the logged-in expert
    @app.route('/api/get-status/', methods=['GET'])
    @jwt_required()  
    def get_bookings():
        current_expert_id = get_jwt_identity()  
        service_type = request.args.get('service_type')
        status = request.args.get('status')

        query = db.session.query(Booking, Service).join(Service, Booking.service_id == Service.id).filter(Service.expert_id == current_expert_id)
        if service_type:
            query = query.filter(Service.service_type == service_type)

        if status:
            query = query.filter(Booking.status == status)
        results = query.all()
        return jsonify([{
            'id': str(booking.id),
            'service_id': str(service.id),
            'service_type': service.service_type,
            'service_title': service.title,
            'user_email': booking.user_email,
            'status': booking.status,
            'booking_time': booking.booking_time,
            'expiry_time': booking.expiry_time
        } for booking, service in results]), 200

    # API for checking all the services provided by all experts
    @app.route('/api/experts-services/', methods=['GET'])
    def get_all_experts_with_services():
        experts = Expert.query.all()
        if not experts:
            return jsonify({'message': 'No experts found'}), 200

        expert_service_list = []
        for expert in experts:
            services = Service.query.filter_by(expert_id=expert.id).all()
            expert_info = {
                'expert_name': expert.name,
                'expert_bio': expert.bio,
                'profile_picture_url': expert.profile_picture_url,
                'services': []
            }
            for service in services:
                service_info = {
                    'service_id': str(service.id),
                    'service_type': service.service_type,
                    'title': service.title,
                    'description': service.description,
                    'price': service.price,
                    'duration': service.duration
                }
                expert_info['services'].append(service_info)
            expert_service_list.append(expert_info)

        return jsonify(expert_service_list), 200

    # Login
    @app.route('/api/login/', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        expert = Expert.query.filter_by(email=email).first()
        if expert and expert.check_password(password):
            access_token = create_access_token(identity=str(expert.id))
            return jsonify(access_token=access_token), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Route for sending a priority DM message
    @app.route('/api/bookings/send-message/', methods=['POST'])
    def send_priority_dm():
        data = request.get_json()
        try:
            validated_data = MessageCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        booking_id = validated_data.booking_id
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        message = Message(
            booking_id=booking.id,
            message=validated_data.message
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({
            'id': str(message.id),
            'booking_id': str(message.booking_id),
            'message': message.message,
            'sent_at': message.sent_at
        }), 201
    
    @app.route('/api/bookings/messages/', methods=['GET'])
    def get_messages_for_booking():
        booking_id = request.args.get('booking_id')
        if not booking_id:
            return jsonify({'error': 'booking_id is required'}), 400
        messages = Message.query.filter_by(booking_id=booking_id).all()
        if not messages:
            return jsonify({'error': 'No messages found for this booking'}), 404
        return jsonify([{
            'id': str(message.id),
            'booking_id': str(message.booking_id),
            'message': message.message,
            'sent_at': message.sent_at
        } for message in messages]), 200

    # Default Route
    @app.route("/")
    def home():
        return "Welcome to Checkmate.io !!"