{
    /*------- ajax call loader ------*/
    $(document).bind("ajaxSend", function () {
        $('.loader').show();
    }).bind("ajaxStop", function () {
        $('.loader').hide();
    });

    var $application_list = $('#application_list'),
        $dtTbl = $application_list.find('#inbox_case'),
        $summary_button = $application_list.find('#summary_button'),
        $query_modal = $('#query_modal'),
        $open_button = $application_list.find('#open_button'),
        $bulk_submit_botton = $application_list.find('#bulk_submit_button'),
        $pause_button = $application_list.find('#pause_button'),
        $summary_modal = $application_list.find('#summary_modal'),
        $pause_modal = $application_list.find('#pause_modal'),
        $pause_submit = $application_list.find('#pause_submit'),
        $pause_case_form = $application_list.find('#pause_case_form'),
        $pre_comment = $application_list.find('.comment_side .pre_comment'),
        $unpause_time = $application_list.find('#unpause_time'),
        $comment_count_span = $application_list.find('#comment_count'),
        $query_count_span = $application_list.find('#query_count'),
        $common_case_form = $('#common_case_form');


    //functions
    // function GeneralInfoCall(deleid) {
    //     $.ajax({
    //         url: general_info + deleid,
    //         method: "GET",
    //         dataType: "JSON",
    //         success: function (data) {
    //             var $target = $('#application_list').find('#general_info');
    //             var $case_tab = $($target).find('#case_property'),
    //                 $current_tab = $($target).find('#current_task');
    //             $case_tab.find('.process_name').text(data.process_name);
    //             $case_tab.find('.case_number').text(data.number);
    //             $case_tab.find('.case_status').text(StatusName(data.status, data.delegation[0].additional_status));
    //             $case_tab.find('.creator').text(data.init_user_name);
    //             $case_tab.find('.create_date').text(moment(data.created_at).format('MMMM Do YYYY, h:mm a'));
    //             $case_tab.find('.last_update').text(moment(data.updated_at).format('MMMM Do YYYY, h:mm a'));
    //
    //             $current_tab.find('.task').text(data.delegation[0].task);
    //             $current_tab.find('.current_user').text(data.delegation[0].user);
    //             $current_tab.find('.task_init_date').text(moment(data.delegation[0].delegation_init_date).format('MMMM Do YYYY, h:mm a'));
    //             $current_tab.find('.task_due_date').text(moment(data.delegation[0].delegation_due_date).format('MMMM Do YYYY, h:mm a'));
    //             $current_tab.find('.task_finish_date').text(data.delegation[0].delegation_finish_date);
    //         },
    //         error: function (response) {
    //             $.each(JSON.parse(response.responseText), (k, v) => {
    //                 notify('Sorry!!! ', v.detail, '', 'danger', 5000)
    //             });
    //         }
    //     });
    // }

    // function StatusName(status, additional_status) {
    //     var status_name;
    //     if (status == 1) {
    //         status_name = "Todo"
    //     } else if (status == 2) {
    //         status_name = "Open"
    //     } else if (status == 0) {
    //         status_name = "Complete"
    //     } else if (status == 3) {
    //         status_name = "Non Claimed"
    //     }
    //     if (additional_status != null) {
    //         if (additional_status == 1) {
    //             additional_status = 'Recheck';
    //         } else if (additional_status == 0) {
    //             additional_status = 'Reject'
    //         } else {
    //             additional_status = '';
    //         }
    //         status_name = status_name + " (" + additional_status + ")"
    //     }else if(additional_status == null && status == 0){
    //         status_name = status_name + " (Approved)"
    //     }
    //     return status_name;
    // }

    function QueryInfo(success_data) {
        var html = '';
        return html = `<tr data-query-id="${success_data.id}">
                <td>${success_data.query}</td>
                <td>${success_data.user_from_name}</td>
                <td>${success_data.date}</td>
                <td>${success_data.user_to_name}</td>
                <td>${success_data.query_answer ? success_data.query_answer : `--`}</td>
                <td>${success_data.answer_date ? success_data.answer_date : `--`}</td>
            </tr>`;
    }


    //Data table
    var inboxdt = $dtTbl.DataTable({
        processing: true,
        serverSide: true,
        ajax: $.fn.dataTable.pipeline({
            url: todo_app + "?item_status=todo" + extra_,
            pages: 1 // number of pages to cache
        }),
        scrollY: 300,
        deferRender: true,
        scroller: true,
        order: [[5, 'desc']],
        columns: [
            {"title": "App ID", "data": "app_number"},
            {"title": "Process", "data": "project_name"},
            {"title": "Task", "data": "task_name"},
            {"title": "Sent by", "data": "sent_by"},
            {"title": "Due Date", "data": "due_date"},
            {"title": "Init Date", "data": "init_date"},
            // {"title": "Priority", "data": "priority"},
        ],
        columnDefs: [
            {
                targets: 0,
                width: '20%',
                "render": (data, a, b) => {
                    if (b.is_recheck == true) {
                        data = "<i class='zmdi zmdi-rotate-left c-red f-18' title='Rechecked task'></i> " + " " + data
                    }
                    return data
                },
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
                "render": (data, a, b) => {
                    var due_date = new Date(data);
                    var current_date = new Date();
                    if (current_date < due_date) {
                        return "<span>"
                            + moment(data).format('MMMM Do YYYY, h:mm a')
                            + "</span>"
                    } else {
                        return "<span class='c-lightRed'>"
                            + moment(data).format('MMMM Do YYYY, h:mm a')
                            + "</span>"
                    }
                },
            },
            {
                targets: 5,
                width: '20%',
                visible: false,
                "render": (data, a, b) => {
                    var due_date = new Date(data);
                    var current_date = new Date();
                    return "<span>"
                        + moment(data).format('MMMM Do YYYY, h:mm a')
                        + "</span>"
                },
            },
        ],
        language: {
            "emptyTable": "You have no Application Assigned"
        },
        "fnRowCallback": function (nRow, aData) {
            if (aData.read_status == "false") {
                $(nRow).addClass('unread');
            }
        }
    });
    /*----- change Header for Risk and over due-----*/
    if (extra_ == '&amp;due_status=risk') {
        $('#application_list').find('.action-header .ah-label').text('Risk')
    } else if (extra_ == '&amp;due_status=due') {
        $('#application_list').find('.action-header .ah-label').text('Over Due')
    }


    //Select Row of DataTable
    $dtTbl.find('tbody').on('click', 'tr', function () {
        var table = $dtTbl.DataTable();
        var element = {}, cart = [];
        var current_data = table.row($(this).closest('tr')).data();
        element.task = current_data.task;
        element.application = current_data.application;
        element.app_number = current_data.app_number;

        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            cart = $bulk_submit_botton.data('bulk_submit_data');
            var indexes = $.map(cart, function (obj, index) {
                if (obj.application == element.application) {
                    return index;
                }
            });
            cart.splice(indexes, 1);


            $bulk_submit_botton.removeData("bulk_submit_data").data("bulk_submit_data", cart);
            if (table.$('tr.selected').length === 1) {
                //enable edit and summary & disable bulk submission
                var data = table.row('.selected').data();
                $summary_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black').data("comment_count", data.comment_count);
                $summary_button.data("query_count", data.query_count);
                $open_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black');
                $pause_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black');
                // cart.push({element: element});
                // $bulk_submit_botton.removeData("bulk_submit_data").data("bulk_submit_data", cart).addClass('c-black');
            } else {
                $summary_button.removeData('case-id').removeClass('c-black').removeData('comment_count');
                $summary_button.removeData('case-id').removeClass('c-black').removeData('query_count');
                $open_button.removeData('case-id').removeClass('c-black');
                $pause_button.removeData('case-id').removeClass('c-black');
                if (table.$('tr.selected').length < 1) {
                    $bulk_submit_botton.removeData('bulk_submit_data').removeClass('c-black');
                } else if (table.$('tr.selected').length > 1) {
                    // cart.push({element: element});
                    // console.log("card", element.task);
                    // $bulk_submit_botton.removeData("bulk_submit_data").data("bulk_submit_data", cart).addClass('c-black');
                }
            }
        }
        else {
            $(this).addClass('selected');
            if ($bulk_submit_botton.data('bulk_submit_data') === undefined) {
                cart.push(element)
            } else {
                cart = $bulk_submit_botton.data('bulk_submit_data');
                cart.push(element)
            }
            $bulk_submit_botton.removeData("bulk_submit_data").data("bulk_submit_data", cart).addClass('c-black');
            if (table.$('tr.selected').length > 1) {
                $summary_button.removeData('case-id').removeClass('c-black').removeData('comment_count');
                $summary_button.removeData('case-id').removeClass('c-black').removeData('query_count');
                $open_button.removeData('case-id').removeClass('c-black');
                $pause_button.removeData('case-id').removeClass('c-black');
            } else {
                var data = table.row('.selected').data();
                $summary_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black').data("comment_count", data.comment_count);
                $summary_button.data("query_count", data.query_count);
                $open_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black');
                $pause_button.removeData("case-id").data("case-id", data.app_id).addClass('c-black');
            }

        }
    });


    //From Notification
    if (localStorage.getItem("outer") != null) {
        var outerdata = JSON.parse(localStorage.getItem("outer"));
        setTimeout(
            function () {
                CommonFormSet(outerdata.task, outerdata.application)
            }, 100
        );
        localStorage.removeItem("outer");
    }

    //DoubleClick
    $dtTbl.find('tbody').on('dblclick', 'tr', function () {
        var table = $dtTbl.DataTable();
        $(this).removeClass('unread');
        var data = table.row(this).data();
        var task_id = data.task;
        var application_id = data.application;
        CommonFormSet(task_id, application_id);
        //window.location = '/workflow/case/form/' + task_id + '/' + application_id;
    });


    //Summary
    $summary_button.off('click').on('click', function () {
        if ($(this).data('case-id')) {
            var id = $(this).data('case-id');
            $('a[data-toggle="tab"]').off('shown.bs.tab').on('shown.bs.tab', function (e) {
                var $target = $(e.target).attr("href");
                //alert(target);
                if (($target === '#general_info')) {
                    GeneralInfoCall(id);
                } else if ($target === '#generated_document') {
                    GeneratedDocumentCall(id)
                }
                else if ($target === '#process_map') {
                    ProcessMapCall(id)
                }
                else if ($target === '#upload_doc') {
                    UploadDocumentCall(id);
                }
                else if ($target === '#comment_tab') {
                    CommentCall(id);
                }
                else if ($target === '#query_tab') {
                    QueryCall(id)
                }
            });
            $('.tab-nav a[href="#general_info"]').tab('show');
            $summary_modal.find('.printing_button').off('click.fang').on('click.fang', function () {
                window.open("/printer/app_view/" + id, "PrintWindow");
            });
            $summary_modal.find($comment_count_span).text($(this).data('comment_count'));
            $summary_modal.find($query_count_span).text($(this).data('query_count'));
            $summary_modal.modal().show();

        } else {
            notify('No case selected!!! ', 'Please select a case first', '', 'danger', 5000);
        }
    });

    //open
    $open_button.off('click').on('click', function () {
        if ($(this).data('case-id')) {
            var table = $('#inbox_case').DataTable();
            $('#inbox_case tr.selected').dblclick();
            // var data =  table.row('.selected').data();
            // console.log(data);
            // var task_id = data.task;
            // var application_id = data.application;
            // CommonFormSet(task_id, application_id);

        } else {
            notify('No case selected!!! ', 'Please select a case first', '', 'danger', 5000);
        }
    });

    //Bulk Submission
    $bulk_submit_botton.off('click').on('click', function () {
        var data_set = $(this).data('bulk_submit_data');
        $bulk_submit_botton.removeData('bulk_submit_data').prop('bulk_submit_data', true);
        if (data_set === undefined) {
            notify('No case selected!!! ', 'Please select cases first', '', 'danger', 5000);
        } else {
            $('#bulk_submission_modal').modal().show();
            let bulk_submit_html = '';
            // data_set = data_set.reverse();
            jQuery.each(data_set, function (index, item) {
                // $.each(res, function (k, v) {
                bulk_submit_html += `<tr data-app_id = ${item.application}>
                                    <td>${item.app_number}</td>
                                    <td class="status"><i class="zmdi zmdi-spinner f-20"></i></td>
                                    <td class="comment"></td>
                                </tr>`;

                $('#bulk_submit_table tbody').empty().append(bulk_submit_html);
            });

            setTimeout(function () {
                // data_set = data_set.reverse();
                jQuery.each(data_set, function (index, item) {
                    AutoSubmit(item);
                });
            }, 500)


        }
    });

    function AutoSubmit(item) {
        setTimeout(function () {
            CommonFormSet(item.task, item.application, null, null, auto = true)
        }, 1000)

    }

    //For modal second open bug fix
    $summary_modal.on('show.bs.modal', function () {
        var id = $summary_button.data('case-id');
        GeneralInfoCall(id);
    });


    //Unselect row
    $('#inbox_case_paginate').on('click', function () {
        if ($dtTbl.find('.selected').length) {

            $summary_button.removeData('announcement-id').removeClass('c-black');
            $pause_button.removeData('case-id').removeClass('c-black').removeData('comment_count');

            $dtTbl.find('tbody tr').removeClass('selected');
        }
    });

}
