from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('fullName')
            phone_number = data.get('phoneNumber')
            email = data.get('email')
            reason = data.get('reason')
            message = data.get('message')

            # Basic validation
            if not full_name or not phone_number or not email or not reason or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Create email content
            subject = f"New Contact Form Submission: {reason}"
            email_message = f"""
            Name: {full_name}
            Phone: {phone_number}
            Email: {email}
            Message: {message}
            """

            # Send the email
            send_mail(
                subject,
                email_message,
                email,  # From email (user's email)
                ['nikhilrai662@gmail.com'],  # To email
                fail_silently=False,
            )

            return JsonResponse({"message": "Form submitted successfully!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=400)
