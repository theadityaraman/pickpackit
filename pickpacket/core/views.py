from django.http import HttpResponse
from django.shortcuts import render
import tempfile
import os
import trimesh
import numpy as np
from scipy.optimize import minimize
from django.http import HttpResponse
from django.conf import settings

def file_upload(request):
    if request.method == "POST":
        if 'myfile' not in request.FILES:
            return HttpResponse("No file part in the request", status=400)

        uploaded_file = request.FILES['myfile']
        if uploaded_file is None:
            return HttpResponse("No file selected", status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            file_path = temp_file.name

        try:
            mesh = trimesh.load(file_path)
        except Exception as e:
            os.remove(file_path)
            return HttpResponse(f"Error loading mesh: {str(e)}", status=400)

        if mesh.is_empty:
            os.remove(file_path)
            return HttpResponse("The uploaded file does not contain valid geometry data.", status=400)

        bounding_box = mesh.bounding_box.bounds
        dimensions = {
            'length': bounding_box[1][0] - bounding_box[0][0],
            'width': bounding_box[1][1] - bounding_box[0][1],
            'height': bounding_box[1][2] - bounding_box[0][2]
        }

        volume = mesh.volume

        vol = 1000
        vol_cubic_units = vol

        conv = np.cbrt(vol / volume)

        def surface_area(x):
            r, h = x
            return 2 * np.pi * r * (r + h)

        def volume_constraint(x):
            r, h = x
            return np.pi * r**2 * h - vol_cubic_units

        initial_guess = [dimensions['width'] / 2, dimensions['height']]
        constraints = ({'type': 'eq', 'fun': volume_constraint})
        bounds = [(0, None), (0, None)]

        result = minimize(surface_area, initial_guess, constraints=constraints, bounds=bounds)
        optimized_r, optimized_h = result.x

        optimization_results = {
            'original_dimensions': dimensions,
            'original_volume': volume * conv**3,
            'optimized_radius': optimized_r * conv,
            'optimized_height': optimized_h * conv,
            'original_surface_area': mesh.area * conv**2,
            'optimized_surface_area': surface_area(result.x) * conv**2
        }

        os.remove(file_path)

        optimized_mesh = trimesh.creation.cylinder(radius=optimized_r, height=optimized_h)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp_output:
            optimized_mesh.export(temp_output.name)
            temp_output_path = temp_output.name

        # Pass the file path to the template
        return render(request, "upload.html", {"optimized_results": optimization_results, "file_path": temp_output_path})

    return render(request, "upload.html")


def home(request):
    return render(request, "index.html")


def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sla')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    return HttpResponse("File not found", status=404)