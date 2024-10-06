from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import QRBarcodeImage
import cv2
from pyzbar.pyzbar import decode
from django.http import HttpResponse
import qrcode
from io import BytesIO

def decode_qr_barcode(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)
    
    result = []
    for obj in decoded_objects:
        result.append({
            'type': obj.type,
            'data': obj.data.decode('utf-8'),
            'rect': obj.rect
        })
    return result

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)

        # Save to database
        qr_image = QRBarcodeImage(image=image)
        qr_image.save()

        # Decode the QR/barcode
        decoded_data = decode_qr_barcode(qr_image.image.path)

        return render(request, 'result.html', {'data': decoded_data, 'image': qr_image})
    return render(request, 'upload.html')


def create_qr_code(request):
    return render(request, 'create_qr.html')

def generate_qr_code(request):
    if request.method == 'POST':
        data = request.POST['data']

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO stream
        img_stream = BytesIO()
        img.save(img_stream)
        img_stream.seek(0)

        # Return the image as a response
        return HttpResponse(img_stream.getvalue(), content_type="image/png")

    return HttpResponse("Invalid request", status=400)
