{
    var $summary_modal = $('#summary_modal'),
        $summary_button = $('#summary_button'),
        $pre_comment = $('.comment_side').find('.pre_comment'),
        $comment_count_span = $('#comment_count'),
        $query_count_span = $('#query_count');

    if(overall === 'y'){
        monitor_app = monitor_app+'?all='+overall;
    }

    //Data table
    $('#monitor_application').DataTable({
        processing: true,
        serverSide: true,
        ajax: $.fn.dataTable.pipeline({
            url: monitor_app,
            pages: 1 // number of pages to cache
        }),
        scrollY: 300,
        deferRender: true,
        scroller: true,
        columns: [
            {"title": "App ID", "data": "number"},
            {"title": "Project", "data": "project"},
            {"title": "Current User", "data": "current_user"},
            {"title": "Initiator", "data": "init_user"},
            {"title": "Created at", "data": "created_at"},
            // {"title": "Task", "data": "task_name"},
        ],
        order: [[4, 'desc']],
        columnDefs: [
            {
                targets: 0,
                width: '15%'
            },
            {
                targets: 1,
                width: '20%',
            },
            {
                targets: 2,
                width: '20%',
            },
            {
                targets: 3,
                width: '20%',
            },
            {
                targets: 4,
                width: '20%',
                "render": (data) => {
                            let dbDate = moment.utc(data).toDate();
                            return moment(dbDate).local().format('MMMM Do YYYY, h:mm:ss a')
                        }
            }
            // {
            //     targets: 2,
            //     width: '20%',
            // },
        ],
        language: {
            "emptyTable": "No Item for monitoring"
        },
        "fnRowCallback": function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            if (aData.read_status == "false") {
                $(nRow).addClass('unread');
            }
        }
    });

    var table = $('#monitor_application').DataTable();
    $('#monitor_application tbody').on('click', 'tr', function () {
        var data = table.row(this).data(),
            $summary_button = $('#summary_button');

        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            $summary_button.removeData('case-id').removeClass('c-black').removeData("comment_count");
            $summary_button.removeData("query_count");
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            $summary_button.removeData("case-id").data("case-id", data.id).addClass('c-black');
            $summary_button.removeData("comment_count").data("comment_count", data.comment_count).addClass('c-black');
            $summary_button.data("query_count", data.query_count);
        }
    });

    // Summary
    $('#summary_button').off('click').on('click', function () {
        if ($(this).data('case-id')) {
            var id = $(this).data('case-id');
            $('a[data-toggle="tab"]').off('shown.bs.tab').on('shown.bs.tab', function (e) {
                var $target = $(e.target).attr("href");

                if (($target == '#general_info')) {
                    GeneralInfoCall(id);
                }
                else if ($target === '#generated_document') {
                    GeneratedDocumentCall(id)
                }
                else if ($target == '#process_map') {
                    ProcessMapCall(id)
                }
                else if ($target == '#upload_doc') {
                    UploadDocumentCall(id);
                }
                else if ($target == '#comment_tab') {
                    CommentCall(id);
                }
                else if ($target == '#query_tab') {
                    QueryCall(id)
                }
            });
            $('.tab-nav a[href="#general_info"]').tab('show');
            $summary_modal.find('.printing_button').off('click.fang').on('click.fang', function () {
                window.open("/printer/app_view/"+id, "PrintWindow");
            });
            $summary_modal.find($comment_count_span).text($(this).data('comment_count'));
            $summary_modal.find($query_count_span).text($(this).data('query_count'));
            $summary_modal.modal().show();

        } else {
            notify('No case selected!!! ', 'Please select a case first', '', 'danger', 5000);
        }
    });

    //For modal second open bug fix
    $summary_modal.on('show.bs.modal', function () {
        var id = $summary_button.data('case-id');
        GeneralInfoCall(id);
    });


    //Unselect row
    $('#monitor_application_paginate').on('click', function () {
        if ($('#participated_case').find('.selected').length) {

            $('#summary_button').removeData('case-id').removeClass('c-black').removeData("comment_count");
            $('#summary_button').removeData("query_count");

            $('#participated_case tbody tr').removeClass('selected');
        }
    });
}
