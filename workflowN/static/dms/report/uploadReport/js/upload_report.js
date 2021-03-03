/**
 * Created by mrityunjoy on 2/14/17.
 */
{
    let uploadReport;
    $dateRangeField = $('input[name="daterange"]');
    var date_from="";
    var date_to="";

    function load_upload_report(url) {
        uploadReport = $('#upload_report').DataTable({
            processing: true,
            serverSide: true,
            ajax: $.fn.dataTable.pipeline({
                url: url,
                pages: 1 // number of pages to cache
            }),
            scrollY: 300,
            deferRender: true,
            scroller: true,
            columns: [
                {"title": "Uploader", "data": "uploader"},
                {"title": "Document Name", "data": "filename"},
                {"title": "Doctype", "data": "doctype"},
                {"title": "Metadata", "data": "metadata"},
                {"title": "Upload Time", "data": "uploaded_at"},
            ],
            columnDefs: [
                {
                    targets: 0,
                    width: "23%",
                    render: (data, a, b) => {
                        return b.uploader.first_name + " " + b.uploader.last_name;
                    }
                },
                {
                    targets: 1,
                    width: "18%"
                },
                {
                    targets: 2,
                    width: "23%",
                    orderable: false
                },
                {
                    targets: 3,
                    width: "20%",
                    render: (data, a, b) => {
                        let html = '';
                        if (Object.keys(JSON.parse(data)).length > 0) {
                            $.each(JSON.parse(data), function (k, v) {
                                html += '<li style="list-style: none">' + '<span style="font-weight: 800">' + v.displayname + '</span>' + "-> " + v.value + '</li>'
                            });
                        } else {
                            html = "N/A"
                        }

                        return html;
                    }
                },
                {
                    targets: 4,
                    width: "15%",
                    render: (data, a, b) => {
                        if (b.uploaded_at) {
                            return moment(data).format('MMMM Do YYYY, h:mm:ss a')
                        } else {
                            return "--"
                        }
                    }
                },
            ],
            order: [[4, 'desc']],
        });
    }

    load_upload_report(upload_report_url);

    //---------------DateRangePicker Search--------------------

    $dateRangeField.daterangepicker({
        "opens": "left",
        autoUpdateInput: false,
        locale: {
            "cancelLabel": "Clear",
        }
    });
    $dateRangeField.on('apply.daterangepicker', function (ev, picker) {

        let from = moment(picker.startDate, 'YYYY-MM-DD hh:mm A').format();
        let to = moment(picker.endDate, 'YYYY-MM-DD hh:mm A').format();
        // let from = picker.startDate.format('YYYY-MM-DD HH:mm:ss.sss');
        // let to = picker.endDate.format('YYYY-MM-DD HH:mm:ss.sss');
        $(this).val(moment(picker.startDate).format('YYYY-MM-DD') + ' to ' + moment(picker.endDate).format('YYYY-MM-DD'));

        let dateFilter = {};
        dateFilter.from = from;
        dateFilter.to = to;

        uploadReport.iCacheLower = -1;
        uploadReport.clearPipeline();
        uploadReport.columns(1).search(from);
        uploadReport.columns(2).search(to);
        uploadReport.draw(false);
        date_from = from;
        date_to = to;
    });
    $dateRangeField.on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('');
    });
    $('.input-mini').addClass("date_form");
    $('.applyBtn').removeClass('btn-success').addClass('btn-info');
    $('.cancelBtn').removeClass('btn-default').addClass('bgm-bluegray');
    $.ajax({
        url: '/api/v1/dms/categorization/documenttype/',
        method: 'GET',
        success: function (data) {
            $.each(data, function (k, v) {
                let $this = v;
                let ancestors = $this.ancestors;

                //console.log(ancestors);
                let option = {};
                let optionName = "";
                if (ancestors.length > 0) {
                    $.each(ancestors, function (k, v) {
                        optionName += v.name + ' &rarr; ';
                    });
                }
                else {
                    optionName = "";
                }
                optionName = optionName + $this.name;
                option[$this.id] = optionName;

                let html = '<option value="' + $this.id + '">' + optionName + '</option>';

                $('#document_type').append(html).selectpicker('refresh');
            });

        },
        error: function (response, jqXHR, textStatus, errorThrown) {
            console.log(response);
        }
    });
    $(document).on('change', '#document_type', function (e) {
        e.preventDefault();
        console.log($(this).val());
        let doc_type_id = $(this).val();
        $('#upload_report').dataTable().fnDestroy();
        console.log('date_from', date_from);
        console.log('date_to', date_to);
        let url = upload_report_url + "?doc_type_id=" + doc_type_id + "&date_from=" + date_from + "&date_to=" + date_to;
        load_upload_report(url)
    });
    $(document).on('click', '#upload_excel', function (e) {
        e.preventDefault();
        if ($('#document_type').val()) {
            let doc_type_id = $('#document_type').val();
            console.log('date-from', date_from);
            console.log('date-to', date_to);
            let url = upload_report_url + "?doc_type_id=" + doc_type_id + "&option=download" + "&date_from=" + date_from + "&date_to=" + date_to;
            $('#upload_report').dataTable().fnDestroy();
            load_upload_report(url);

            notify('An Excel file will generate and sent it to your email.', '', '', 'success', '6000');
        } else {
            notify('Please select document type first', '', '', 'danger', '6000');
        }
    })
}