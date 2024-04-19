$(document).ready(function () {
  // Function to handle the change event of dropdown menus
  function handleDropdownChange() {
    var sn1 = $("#comp1").val();
    var sn2 = $("#comp2").val();
    var sn3 = $("#comp3").val();
    var polymorph = $("#polym").val();

    // Make an HTTP POST request to the server
    $.ajax({
      url: "/compute",
      method: "POST",
      data: {
        sn1: sn1,
        sn2: sn2,
        sn3: sn3,
        polymorph: polymorph,
      },
      success: function (response) {
        // Table 1
        $("#Results table thead tr:nth-child(1) td:nth-child(2)").text(
          response.refID
        );
        $("#Results table tbody tr:nth-child(1) td:nth-child(2)").text(
          response.chemical_formula
        );
        $("#Results table tbody tr:nth-child(2) td:nth-child(2)").text(
          response.mol_weight_sample
        );
        $("#Results table tbody tr:nth-child(3) td:nth-child(2)").text(
          response.exp_enthalpy
        );
        $("#Results table tbody tr:nth-child(4) td:nth-child(2)").text(
          response.exp_temp
        );

        // Table 2
        $("#Results2 table tbody tr:nth-child(1) td:nth-child(2)").text(
          response.sat_enthalpy_sample
        );
        $("#Results2 table tbody tr:nth-child(1) td:nth-child(4)").text(
          response.hfGCM
        );
        $("#Results2 table tbody tr:nth-child(2) td:nth-child(2)").text(
          response.temp_sample_a
        );
        $("#Results2 table tbody tr:nth-child(2) td:nth-child(3)").text(
          response.temp_sample_b
        );
        $("#Results2 table tbody tr:nth-child(2) td:nth-child(4)").text(
          response.tfGCM
        );

        // Table 3
        $("#Results3 table tbody tr:nth-child(1) td:nth-child(2)").text(
          response.sat_enthalpy_sample_P1L
        );
        $("#Results3 table tbody tr:nth-child(2) td:nth-child(2)").text(
          response.temp_sample_a_P1L
        );
        $("#Results3 table tbody tr:nth-child(2) td:nth-child(3)").text(
          response.temp_sample_b_P1L
        );

        // Handle success response
        console.log("Data sent successfully:", response);
      },
      error: function (xhr, status, error) {
        // Handle error response
        console.error("Error:", error);
      },
    });
  }

  const fileInput = document.getElementById("file-upload");
  const fileNameSpan = document.getElementById("file-name");

  fileInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      fileNameSpan.textContent = file.name;
    } else {
      fileNameSpan.textContent = "No file selected";
    }
  });

  const fileInputSFC = document.getElementById("file-upload-sfc");
  const fileNameSpanSFC = document.getElementById("file-name-sfc");

  fileInputSFC.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      fileNameSpanSFC.textContent = file.name;
    } else {
      fileNameSpanSFC.textContent = "No file selected";
    }
  });

  $("#upload-form").submit(function (e) {
    e.preventDefault();

    var form = $(this);
    var formData = new FormData(form[0]);

    $.ajax({
      url: "/upload_batch",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      async: false,
      cache: false,
      success: function (response, status, xhr) {
        console.log(response.message);
        $("#response-message").text(response.message);

        // Show the download button and set the appropriate download URL
        $("#download-button").show();
        var downloadUrl = "/download/" + response.filename; // Construct the download URL
        console.log(downloadUrl);
        $("#download-button").attr("href", downloadUrl);

        $("#download-button").html("&nbsp;Download File");
      },
      error: function (xhr, status, error) {
        try {
          const errorData = JSON.parse(xhr.responseText);
          $("#response-message").text(errorData.message);

          // Hide the download button on error
          $("#download-button").hide();
        } catch (e) {
          console.log(xhr.responseText);
          $("#response-message").text(xhr.responseText);
        }
      },
    });
    return false;
  });

  $("#upload-sfc").submit(function (e) {
    e.preventDefault();

    var form = $(this);
    var formData = new FormData(form[0]);

    $.ajax({
      url: "/upload_sfc",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      async: false,
      cache: false,
      success: function (response, status, xhr) {
        console.log(response.message);
        $("#response-message-sfc").text(response.message);

        // Show the download button and set the appropriate download URL
        $("#download-button-sfc").show();
        var downloadUrl = "/download_sfc/" + response.filename; // Construct the download URL
        console.log(downloadUrl);
        $("#download-button-sfc").attr("href", downloadUrl);

        $("#download-button-sfc").html("&nbsp;Download File");
      },
      error: function (xhr, status, error) {
        try {
          const errorData = JSON.parse(xhr.responseText);
          $("#response-message-sfc").text(errorData.message);

          // Hide the download button on error
          $("#download-button-sfc").hide();
        } catch (e) {
          console.log(xhr.responseText);
          $("#response-message-sfc").text(xhr.responseText);
        }
      },
    });
    return false;
  });

  // Attach the change event handler to all three dropdown menus
  $("#comp1").change(handleDropdownChange);
  $("#comp2").change(handleDropdownChange);
  $("#comp3").change(handleDropdownChange);
  $("#polym").change(handleDropdownChange);
});
