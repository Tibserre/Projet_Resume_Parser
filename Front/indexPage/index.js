document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");
  
    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });
  
    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });
  
    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });
  
    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });
  
    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
  
      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }
  
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  
  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
  
    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }
  
    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }
  
    thumbnailElement.dataset.label = file.name;
  
    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
  
      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }



  

  window.onload = function () {

  };

  function CheckState() {
      var chkBox = document.getElementById('FuzzyState');
      console.log(chkBox.checked);
  }

  function afficherLocalStorage() {
      localJson = JSON.parse(localStorage.getItem('resumes_parsed'));
      console.log(localJson);
  }

  function EmptyLocalStorage() {
      localStorage.removeItem('resumes_parsed');

  }
  function getResult(){
      console.log("inside getResult");
      fetch("http://127.0.0.1:2000/resume-parser")
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  }

  function SendPost() {
      console.log("inside SendPost");
      var fileInput = document.querySelector('input[type="file"]')
      var formdata = new FormData();
      formdata.append("files[]", fileInput.files[0]);
      var chkBox = document.getElementById('FuzzyState');
      formdata.append("fuzzy", chkBox.checked.toString());

      var requestOptions = {
          method: 'POST',
          body: formdata,
          redirect: 'follow'
      };
      event.preventDefault();
      fetch("http://127.0.0.1:2000/resume-parser?files[]=", requestOptions)
          .then(response => response.json())
          .then(result => {
              console.log(result);
              localStorage.setItem("resumes_parsed", JSON.stringify(result));
              //window.open("/Front/uploadPage/upload.html", '_blank');

          })
          .catch(error => console.log('error', error));

  }
