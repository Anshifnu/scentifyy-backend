from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import razorpay_client
from .models import RazorpayPayment
from razorpay.errors import SignatureVerificationError

class CreateRazorpayOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")

        razorpay_order = razorpay_client.order.create({
            "amount": int(amount) * 100,  # rupees → paise
            "currency": "INR",
            "payment_capture": 1
        })

        RazorpayPayment.objects.create(
            user=request.user,
            order_id=razorpay_order["id"],
            amount=amount,
        )

        return Response({
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": "INR"
        })






class VerifyRazorpayPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })

            payment = RazorpayPayment.objects.get(
                order_id=data["razorpay_order_id"]
            )
            payment.payment_id = data["razorpay_payment_id"]
            payment.status = "PAID"
            payment.save()

            return Response({"status": "Payment Verified"})

        except SignatureVerificationError:
            return Response(
                {"error": "Invalid payment signature"},
                status=400
            )



