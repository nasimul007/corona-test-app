function RemoveManualInputGroup() {
    $('input[name=statment_mode]').closest('.row').addClass('start_line');
    $('#instruction_setup').closest('.row').addClass('end_line');
    var remove_group = $(".start_line").nextUntil(".end_line");
    remove_group = remove_group.add(remove_group.last().next()).add(remove_group.first().prev());
    remove_group.remove();
}

function UploadDecision() {
    swal({
        title: "Upload Details?",
        text: "If you have already filled up form then click on Upload File. Otherwise click on Manual Input",
        type: "question",
        showCancelButton: true,
        confirmButtonText: "Upload File",
        cancelButtonText: "Manual Input",
        allowOutsideClick: false,
    }).then(function (isConfirm) {
        if (isConfirm) {
            RemoveManualInputGroup();
        }
    }, function (dismiss) {
        $('#upload_detail_file').closest('.row').remove();
    });
}

function CustomForm() {
    let file_length = $('#upload_detail_file').closest('.row').find('.fg-line').find('a').length;
    if (file_length > 0) {
        RemoveManualInputGroup();
    } else {
        $('#upload_detail_file').closest('.row').remove();
    }
}

function DebitSet() {
    $('input[name=loa_file]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
    $('input[name=salary_file]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
    $('input[name=account_number]').attr('data-parsley-required', 'true').closest('.col-md-3').show();
}

function CreditSet() {
    $('input[name=loa_file]').attr('data-parsley-required', 'true').closest('.col-md-3').show();
    $('input[name=salary_file]').attr('data-parsley-required', 'true').closest('.col-md-3').show();
    $('input[name=account_number]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
}

function OtherSet() {
    $('input[name=loa_file]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
    $('input[name=salary_file]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
    $('input[name=account_number]').removeAttr('data-parsley-required').closest('.col-md-3').hide();
}

function CustomWork() {
    // Onload set
    if ($('input[name=card_type]:checked').length > 0) {
        let selected_value = $("[name=card_type]:checked").val();
        if (selected_value === 'DEBIT CARD') {
            DebitSet();
        } else if (selected_value === 'CORPORATE CARD' || selected_value === 'PREPAID CARD') {
            OtherSet();
        } else if (selected_value === 'CREDIT CARD') {
            CreditSet();
        }
    }
    // onselect change
    $("input[name=card_type]").on('change', function () {
        let selected_value = $("[name=card_type]:checked").val();
        if (selected_value === 'DEBIT CARD') {
            DebitSet();
        } else if (selected_value === 'CORPORATE CARD' || selected_value === 'PREPAID CARD') {
            OtherSet();
        } else if (selected_value === 'CREDIT CARD') {
            CreditSet();
        }
    });

}