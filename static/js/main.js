$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#result-path').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide()
        $('#result-path').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // Show loading animation



        $(this).hide();
        $('.loader').show();


        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: true,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                //$('.result-path').attr('src', 'url(static/Segmented-Positive1.png)')
                //$('#result-path').src('url(' + 'static/Segmented-Positive1.png)');
                console.log(data);
                $('#result-path').fadeIn(600);

                //$('#result-path').reload('static/Segmented-Positive1.png')//.attr('src', 'static/Segmented-Positive1.png')
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
        error : function(e,data)
        {   $('.loader').hide();
            $('#result').fadeIn(600);
            $('#result').text(' Result: Some Error is happened while Image Segmentation Please Choose Higher Dimension Image ' + data);
          //SHOW ERROR TO USER HERE THIS SECTION IS CALLED IN CASE OF ERRORS TO SEE THE OBJECT OF the error use console.log(e);
        }
        });
    });

});
