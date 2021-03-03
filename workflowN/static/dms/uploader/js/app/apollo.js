/**
 * Created by rawnak on 12/10/17.
 */
function DocumentNameSet() {
    if(customer == 'z8t5y67') {
        var $add_form = $('#add_meta_data'),
            $ip_no = $add_form.find('input[name=ip_no]'),
            $admission_date = $add_form.find('input[name=admission_date]'),
            $dr_incharge = $add_form.find('input[name=dr_incharge]'),
            $file_name = $add_form.find('input[name=file_name]');
    }else{
        var $add_form = $('#add_meta_data'),
            $client_code = $add_form.find('input[name=client_code]'),
            $documentation_date = $add_form.find('input[name=documentation_date]'),
            $file_name = $add_form.find('input[name=file_name]');
            $client_code.val(client_code)
            $documentation_date.val(recent_date)
            Set();
    }

    function Set() {
        var value = '';
        if(customer == 'z8t5y67') {
            if ($admission_date.val()) {
                value = value + 'DOA: ' + $admission_date.val() + ' '
            }
            if ($ip_no.val()) {
                value = value + 'IP : ' + $ip_no.val() + ' '
            }
            if ($dr_incharge.val()) {
                value = value + 'Dr.: ' + $dr_incharge.val()
            }
        }
        else{
            if ($client_code.val()) {
                value = value + 'Code: ' + $client_code.val() + ' '
            }
            if ($documentation_date.val()) {
                value = value + '_Date: ' + $documentation_date.val()
            }
        }
        // var value = $admission_date.val() + '_' + $ip_no.val() + '_' + $dr_incharge.val();
        $file_name.val(value)
    }
    if(customer == 'z8t5y67') {
        $('input[name=ip_no], input[name=dr_incharge]').on('keyup', function () {
            Set();
        });
        $admission_date.on("dp.change", function () {
            Set();
        });
    }else{
        $('input[name=client_code]').on('keyup', function () {
            Set();
        });
        $documentation_date.on("dp.change", function () {
            Set();
        });
    }
}