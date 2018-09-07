$(document).ready(function() {
  //alert("his");
  var hiscase_table = $('#case_his_table').DataTable({
    "bSort" : false,
    "bFilter" : false,
    "processing" : true,
    "bServerSide" : true,
    "aLengthMenu" : [ 10, 20 ,50 ],
    "sAjaxSource" : "/show_hiscase_table",
    "columns" : [
      {
        "data" : "case_id",
        "render" : function(data, type, row, meta) {
          return data = '<a target ="_blank" href="https://access.redhat.com/support/cases/#/case/'+data+'">'+data+'</a>';
        }
      }, 
      {
        "data" : "details",
        "render" : function(data, type, row, meta) {
          return data = '<a href="#" class="badge badge-secondary" data-toggle="modal" data-target="#case_details_modal" data-case-id="'+row.case_id+'">details</a>';
        }
      },
      {
        "data" : "predict",
        "defaultContent": "-"
      },
      {
        "data" : "validate",
        "defaultContent": "-"
      },
      {
        "data" : "case_date"
      },
      {
        "data" : "status",
        "defaultContent": "-"
      },
      {
        "data" : "case_cover",
        "defaultContent": "-",
        "render" : function(data, type, row, meta) {
          return data = '<a target ="_blank" href="https://polarion.engineering.redhat.com/polarion/#/project/RedHatEnterpriseLinux7/workitem?id='+data+'">'+data+'</a>';
        }
      },
      {
        "data" : "bug_cover",
        "defaultContent": "-",
        "render" : function(data, type, row, meta) {
          return data = '<a target ="_blank" href="https://bugzilla.redhat.com/show_bug.cgi?id='+data+'">'+data+'</a>';
        }
      },
      {
        "data" : null,
        "render" : function(data, type, row, meta) {
          return data = '<a href="#" class="badge badge-primary" data-toggle="modal" data-target="#update_case_modal" data-case-id="'+row.case_id+'" data-case-cover="'+row.case_cover+'" data-bug-cover="'+row.bug_cover+'">edit</a>';
        }
      }
    ],
  });

  $('#update_case_modal').on('show.bs.modal', function (event) {
    var modal_trigger = $(event.relatedTarget); // Button that triggered the modal
    var case_id = modal_trigger.data('case-id'); // Extract info from data-* attributes
    var case_cover = modal_trigger.data('case-cover');
    var bug_cover = modal_trigger.data('bug-cover');
    var modal = $(this);
    modal.find('.modal-title').text('Update Case: '+case_id);
    modal.find('.modal-body #case-id').val(case_id);
    modal.find('.modal-body #case-cover').val(case_cover);
    modal.find('.modal-body #bug-cover').val(bug_cover);
  });

  $('#update-case-button').click(function(e){
    //e.preventDefault();
    $('#update-case-form').submit();
    $('#update_case_modal').modal('hide');
    //refresh datatables
    hiscase_table.ajax.reload();
    //location.reload();
  });
});