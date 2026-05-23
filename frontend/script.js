async function uploadImage() {

    const fileInput =
        document.getElementById("imageInput");

    const formData = new FormData();

    formData.append(
        "image",
        fileInput.files[0]
    );

    const response = await fetch(
        "http://127.0.0.1:5000/upload",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    document.getElementById("result")
        .innerText = data.text;
}
