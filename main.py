import eel
import cv2
import base64
import numpy as np

eel.init('web')

def resize_image(img_np, max_dimension=800):
    height, width = img_np.shape[:2]
    if height > max_dimension or width > max_dimension:
        if height > width:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        else:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        img_np = cv2.resize(img_np, (new_width, new_height))
    return img_np

@eel.expose
def process_image(image_data, filter_type):
    try:
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Оптимизация: изменение размера изображения перед обработкой
        img_np = resize_image(img_np)

        gray_image = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        if filter_type == 'blur':
            filtered_image = cv2.GaussianBlur(img_np, (15, 15), 0)
        elif filter_type == 'gaussian':
            kernel_size = (5, 5)
            sigma = 1.5
            kernel = cv2.getGaussianKernel(kernel_size[0], sigma)
            gaussian_kernel = kernel * kernel.T
            filtered_image = cv2.filter2D(img_np, -1, gaussian_kernel)
        elif filter_type == 'laplacian':
            filtered_image = cv2.Laplacian(img_np, cv2.CV_64F)
        elif filter_type == 'sobel':
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
            gradient_image = cv2.magnitude(sobel_x, sobel_y)
            filtered_image = cv2.convertScaleAbs(gradient_image)
        elif filter_type == 'canny':
            edges = cv2.Canny(gray_image, 100, 200)
            filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        is_success, buffer = cv2.imencode(".png", filtered_image)
        result_image_data = base64.b64encode(buffer).decode('utf-8')

        return result_image_data

    except Exception as e:
        print(f"Ошибка обработки изображения: {e}")
        return None

# eel.start('index.html', size=(700, 500))
eel.start('index.html', size=(700, 500), mode='chrome', port=8080)
