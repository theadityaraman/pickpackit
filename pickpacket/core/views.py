from django.shortcuts import render
from django.http import HttpResponse


def file_upload(request):
    if request.method == "POST":
        # Check if the file is in the request
        if 'myfile' not in request.FILES:
            return HttpResponse("No file part in the request", status=400)

        uploaded_file = request.FILES['myfile']
        if uploaded_file is None:
            return HttpResponse("No file selected", status=400)

        print(f"Uploaded file: {uploaded_file.name} ({uploaded_file.size} bytes)")
        # Placeholder for further file processing

        '''Add file processing and new file creation right here'''

        return HttpResponse("File uploaded successfully")

    # Render the file upload form
    return render(request, "index.html")
