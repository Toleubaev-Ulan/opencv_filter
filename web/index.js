function processImage(filterType) {
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = new Image();
      img.onload = function () {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        const imageData = canvas.toDataURL("image/jpeg", 0.7);
        eel.process_image(imageData, filterType)(setImageResult);
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function setImageResult(resultImageData) {
  if (resultImageData === null) {
    alert("Ошибка обработки изображения.");
    return;
  }

  const resultImage = document.getElementById("resultImage");
  resultImage.src = "data:image/png;base64," + resultImageData;
  resultImage.style.display = "block";
}

function removeImage() {
const resultImage = document.getElementById("resultImage");
  resultImage.src = "./assets//images/no-image.jpg";
  resultImage.style.display = "block";
  const fileInput = document.getElementById("imageInput");
  fileInput.value = null;
}

function downloadImage() {
  const resultImage = document.getElementById("resultImage");
  const downloadLink = document.createElement("a");
  downloadLink.href = resultImage.src;
  downloadLink.setAttribute("download", "filtered_image.png");

  downloadLink.style.display = "none";
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}
