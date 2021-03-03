let WorkflowApp = Vue.extend({
    delimiters: ["@{", "}"],
});

WorkflowApp.use(VeeValidate);

WorkflowApp.filter('humanReadableDate', function (value) {
    return moment(value).format("DD MMM YYYY");
});

WorkflowApp.filter('humanReadableTime', function (value) {
    return moment(value).format("hh:mm A");
});

WorkflowApp.filter('humanReadableDateTime', function (value) {
    return moment(value).format("DD MMM YYYY hh:mm A");
});

var globalEformImportData;
new WorkflowApp({
    el: '#content',
    components: {
        modal: vueboot.modal
    },
    data: {
        eforms: {},
        eform_title: '',
        eform_description: '',
    },
    methods: {
        EShowModal(modal){
            this.$refs[modal].showModal();
        },

        EHideModal(modal){
            this.$refs[modal].hideModal();
        },

        eFormListModal(modal){
            this.$http.get(api.eform.list).then(response => {
                this.eforms = response.body
            });

            this.EShowModal(modal);
        },

        createEformModal(modal, scope){
            if(modal == 'eform-import-modal') {
                //console.log("here", modal, globalEformImportData)
                $('#add_eform_form').trigger('reset');
                $("#add_eform_form .help-block").empty();
                $('#add_eform_form .form-group').removeClass('has-error');
                $("#eform_to_be_imported option[value]").remove();
                //Users List
                $.ajax({
                    type: "GET",
                    url: api.eform.list + '&import=y',
                    dataType: "json",
                    success: function (data) {
                        //console.log("data here", data)
                        globalEformImportData = data
                        $.each(data, function (i, d) {
                            //console.log("dd", i)
                            $("#eform_to_be_imported").append($('<option>', {
                                value: i,
                                text: d.title+", project name: "+d.process_name,
                            }));

                        });
                        $("#eform_to_be_imported").selectpicker('refresh');
                    },
                    error: function (response) {
                        $.each(JSON.parse(response.responseText), (k, v) => {
                            notify(`<strong>${k.substr(0, 1).toUpperCase() + k.substr(1) }:</strong> `, `<i>${v}</i>`, '', 'danger', 10000);
                        });
                    }
                });
            }
            this.eform_title = '';
            this.eform_description = '';
            //this.errors.clear(scope);
            this.EShowModal(modal);
        },

        createEform(modal, scope){
            if(modal == 'eform-import-modal'){

                var selected_eform = globalEformImportData[parseInt($('#eform_to_be_imported').val())];
                var new_eform_name = $('#eform_name').val();

                let formData = {
                    project: api.project.id,
                    type: selected_eform["type"],
                    content: selected_eform["content"],
                    description: selected_eform["description"],
                    title: new_eform_name,
                    version: selected_eform["version"],
                    variables_id: selected_eform["variables_id"]
                };
                this.$http.post(api.eform.create, formData).then(
                    response => {
                        if (response.body['content'] === null) {
                            response.body['content'] = '';
                        }
                        this.eforms.push(response.body);
                        PMDesigner.dynaformDesigner(response.body);
                        this.errors.clear(scope);
                        this.EHideModal(modal);
                        },
                    response => {
                        for (let r in response.body) {
                            notify('', response.body[r], '', 'danger', 2000);
                        }
                    });
            }
            else{
                let formData = {
                    project: api.project.id,
                    title: this.eform_title,
                    description: this.eform_description,
                };

                this.$validator.validateAll(scope).then(success => {
                    if (success) {
                        this.$http.post(api.eform.create, formData).then(
                            response => {
                                if (response.body['content'] === null) {
                                    response.body['content'] = '';
                                }

                                this.eforms.push(response.body);
                                PMDesigner.dynaformDesigner(response.body);
                                this.errors.clear(scope);
                                this.EHideModal(modal);
                            },
                            response => {
                                for (let r in response.body) {
                                    notify('', response.body[r], '', 'danger', 2000);
                                }
                            });
                        }
                });
            }

        },

        editEform(id) {
            this.$http.get(`${api.eform.edit}${id}/`).then(response => {
                if (response.body['content'] === null) {
                    response.body['content'] = '';
                }

                PMDesigner.dynaformDesigner(response.body);
            });
        },

        deleteEform(index, id){
            this.$http.delete(`${api.eform.delete}${id}/`).then(response => {
                if (response.status == 204) {
                    this.eforms.splice(index, 1);
                    notify('', 'EForm deleted successfully', '', 'success', 2000);
                }
            });
        },

        openVariableModal(){
            let pmvariables = new PMVariables();
            pmvariables.load();
        }
    }
});
