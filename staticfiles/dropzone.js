var Drop = Dropzone.options.DidDropzone = {

  autoProcessQueue: false, //stops from uploading files until user submits form
  paramName: "csv_file", // The name that will be used to transfer the file
  maxFilesize: 0.5, // Maximum size of file that you will allow (MB)
  clickable: true, // This allows the dropzone to select images onclick
  acceptedFiles: '.csv', //accepted file types
  maxFiles: 1, //Maximum number of files/images in dropzone
  parallelUploads: 10,
  addRemoveLinks: true,
  // previewTemplate: '<div class="dz-preview dz-image-preview">'+
  //                     '<div class="dz-image">'+
  //                     '<img data-dz-thumbnail />'+
  //                     '</div>'+

  //                   '<div class="dz-details">'+
  //                     '<div class="dz-filename"><span data-dz-name></span></div>'+
  //                     '<div class="dz-size" data-dz-size></div>'+
  //                   '</div>'+

  //                   '<div class="dz-success-mark"><span>✔</span></div>'+
  //                   '<div class="dz-error-mark"><span>✘</span></div>'+
  //                   '<div class="dz-error-message"><span data-dz-errormessage></span></div>'+
  //                 '</div>',
  init: function () {
    // add a close button
    // Create the remove button
    // var removeButton = Dropzone.createElement("<a class='boxclose' id='boxclose'></a>")

    // const dropArea = document.querySelector(".dropzone");
    // let button = `<a class="boxclose" id="boxclose"></a>`;
    // dropArea.innerHTML = button;
    var submitButton = document.querySelector("#drop_csv")
    var url = $('#DidDropzone').attr("action")
    myDropzone = this;
    
    //process the queued images on click
    submitButton.addEventListener("click", function () {
      myDropzone.processQueue();
    });

    //fire the images to url
    myDropzone.on("processing", function (file) {
      myDropzone.options.url = url;
    });

    // clear the dropzone when complete
    myDropzone.on("complete", function (file) {
      myDropzone.removeFile(file);
    });
    myDropzone.on("success", function (file, response) {
      window.location.href = "csv_upload"
    });
  },
}