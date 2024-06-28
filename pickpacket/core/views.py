import trimesh
import numpy as np
from scipy.optimize import minimize
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
import os

def file_upload(request):
    if request.method == "POST":
        # Check if the file is in the request
        if 'myfile' not in request.FILES:
            return HttpResponse("No file part in the request", status=400)

        uploaded_file = request.FILES['myfile']
        if uploaded_file is None:
            return HttpResponse("No file selected", status=400)

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            file_path = temp_file.name

        # Load the mesh
        try:
            mesh = trimesh.load(file_path)
        except Exception as e:
            os.remove(file_path)
            return HttpResponse(f"Error loading mesh: {str(e)}", status=400)

        if mesh.is_empty:
            os.remove(file_path)
            return HttpResponse("The uploaded file does not contain valid geometry data.", status=400)

        # Calculate dimensions
        bounding_box = mesh.bounding_box.bounds
        dimensions = {
            'length': bounding_box[1][0] - bounding_box[0][0],
            'width': bounding_box[1][1] - bounding_box[0][1],
            'height': bounding_box[1][2] - bounding_box[0][2]
        }

        # Calculate volume and surface area
        volume = mesh.volume
        surface_area = mesh.area

        # For demonstration, using a fixed volume (you can get this from user input)
        vol = 1000  # Example volume in mL
        vol_cubic_units = vol  # Assuming 1 mL = 1 cubic unit for simplicity

        conv = np.cbrt(vol / volume)

        # Function to minimize (surface area of the cylinder)
        def surface_area(x):
            r, h = x
            return 2 * np.pi * r * (r + h)

        # Constraint (volume of the cylinder)
        def volume_constraint(x):
            r, h = x
            return np.pi * r**2 * h - vol_cubic_units

        # Initial guess for r and h
        initial_guess = [dimensions['width'] / 2, dimensions['height']]

        # Constraints dictionary for the optimization
        constraints = ({'type': 'eq', 'fun': volume_constraint})

        # Boundaries for r and h (both must be positive)
        bounds = [(0, None), (0, None)]

        # Perform the optimization
        result = minimize(surface_area, initial_guess, constraints=constraints, bounds=bounds)

        # Extract the optimized r and h
        optimized_r, optimized_h = result.x

        # Display results
        optimization_results = {
            'original_dimensions': dimensions,
            'original_volume': volume * conv**3,
            'optimized_radius': optimized_r * conv,
            'optimized_height': optimized_h * conv,
            'original_surface_area': mesh.area * conv**2,
            'optimized_surface_area': surface_area(result.x) * conv**2
        }

        os.remove(file_path)  # Clean up the temporary file

        return render(request, "upload.html", {"optimized_results": optimization_results})

    # Render the file upload form
    return render(request, "upload.html")


def home(request):
    return render(request, "index.html")