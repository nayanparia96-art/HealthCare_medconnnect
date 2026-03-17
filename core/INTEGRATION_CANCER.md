Cancer Detector — Integration Instructions

Quick summary
- Feature added under `core` app: views, templates, static CSS, and model loader.
- Model expected at `model/cancer_model.h5` (Keras .h5 file).

Files added/changed
- [core/views.py](core/views.py): cancer detector views, model loader and preprocessing.
- [core/urls.py](core/urls.py): routes `/cancer-detector/` and `/cancer-result/`.
- [core/templates/core/cancer_detector.html](core/templates/core/cancer_detector.html): upload + inline result display.
- [core/templates/core/cancer_result.html](core/templates/core/cancer_result.html): optional result page.
- [core/static/core/cancer.css](core/static/core/cancer.css): styling.
- [model/README.txt](model/README.txt): place model instructions.

Step-by-step integration
1. Put your pre-trained Keras model file into the project `model/` folder and name it exactly:
   - `model/cancer_model.h5`
   - Model should accept RGB images sized 224x224 and output a single probability (0..1) for cancer presence. If your model outputs logits, adapt the postprocessing in `core/views.py`.

2. Install required Python packages (venv active):
```bash
pip install tensorflow pillow numpy
```
- Use `tensorflow-cpu` or a specific TF version to match your environment if needed.

3. Static files and templates
- Static CSS file is at [core/static/core/cancer.css](core/static/core/cancer.css).
- If you use `collectstatic` in production, run it after adding the static files.

4. Run the server and test
```bash
python manage.py runserver
```
Open: `http://127.0.0.1:8000/cancer-detector/`

5. How the detector behaves
- Uploaded image is converted to RGB, resized to 224x224, normalized (/255.0) and passed to the model.
- The view treats predictions >= 0.5 as "Cancer Detected". Adjust threshold or postprocessing in `core/views.py` if needed.
- If `tensorflow` isn't installed or model file missing, the page shows a clear error message.

6. Adjusting for different model outputs
- If your model returns an array like `[ [0.2, 0.8] ]` or multi-class outputs, update `get_prediction()` in `core/views.py` to extract the appropriate class probability.

7. Security & file handling
- This implementation keeps uploaded images in memory; for large files or production, enforce file-size limits and validate file types.
- Consider adding server-side scanning, size limits, and storing images temporarily if you need later review.

8. Customization points
- Threshold: change the `detected = prob >= 0.5` line in `core/views.py`.
- Advice text: edit the advice dictionaries inside `cancer_detector` view.
- Separate result page: `cancer_result.html` is available if you prefer redirecting after POST.

9. Troubleshooting
- "AI model not found" → ensure `model/cancer_model.h5` exists and Django `settings.BASE_DIR` points to project root.
- "tensorflow not installed" → install TF in your virtualenv.
- Model prediction errors → verify input shape and model signature (use a small script to run a sample prediction).

Optional: sample prediction script (run from project root)
```python
# sample_predict.py
from PIL import Image
import numpy as np
import tensorflow as tf
img = Image.open('sample.jpg').convert('RGB').resize((224,224))
arr = np.array(img).astype('float32')/255.0
arr = np.expand_dims(arr,0)
model = tf.keras.models.load_model('model/cancer_model.h5')
print(model.predict(arr))
```

If you want, I can:
- run a simulated local test (you can upload a sample image here), or
- create a git branch and prepare a small test checklist.

