//$(document).ready(function() {
$('a[id="newcase-tab"]').click(function () {
  var case_id_list="";
  var newcase_table="";
  //$.get({
  //$.getJSON({
  //  url: "/get_case_id_list",
  //  success:function(ret_data){
  //      case_id_list = ret_data.case_id_list;
  //      console.log(case_id_list)
  //    }
  //  });

  function runAsync(){
    var p = new Promise(function(resolve, reject){
      $.ajax({
        "type": "GET",
        "url": "/get_case_id_list",
        success: function(ret_data){
          case_id_list = ret_data.case_id_list;
          resolve(case_id_list);
        }
      });
    });
    return p;
  };
  runAsync().then(function(async_data){
      //alert(async_data);
      newcase_table = $('#case_new_table').DataTable({
          "bSort" : false,
          "bFilter" : false,
          "processing" : true,
          "bServerSide" : true,
          "aLengthMenu" : [ 10, 20 ,50 ],
          "sAjaxSource" : '/show_newcase_table',
          "fnServerParams": function ( aoData ) {
            aoData.push( { "name": "case_id_list", "value": JSON.stringify(async_data) } );
          },
//          "ajax": {//Don't Work
//              "url": "/show_newcase_table",
//              "data": {
//                "case_id_list": JSON.stringify(async_data),
//              }
////              "data": function ( d ) {
////                d.case_id_list = JSON.stringify(async_data);
////              }
//            },

//          "oLanguage": {
//            "sLengthMenu": "每页显示 _MENU_ 条记录",
//            "sZeroRecords": "对不起，查询不到任何相关数据",
//            "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
//            "sInfoEmtpy": "找不到相关数据",
//            //"sInfoFiltered": "数据表中共为 _MAX_ 条记录",  
//            "sProcessing": "正在加载中...",
//            "sSearch": "搜索",
//            "sInfoEmpty": "显示 0 至 0 共 0 项",
//            "oPaginate": { "sFirst": "第一页", "sPrevious": "上一页 ", "sNext": "下一页 ", "sLast": "末页 " }
//          },
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
              "defaultContent": "-",
              "sortable": false
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
                return '<a href="#" class="badge badge-primary" data-toggle="modal" data-target="#save_case_modal" data-case-id="'+row.case_id+'" data-predict="'+row.predict+'" data-case-date="'+row.case_date+'" data-status="'+row.status+'">save</a>';
              }
            },
          ],
      });
  });

var modal_trigger="";

  $('#save_case_modal').on('show.bs.modal', function (event) {
    modal_trigger = $(event.relatedTarget); // Button that triggered the modal
    var case_id = modal_trigger.data('case-id'); // Extract info from data-* attributes
    var predict = modal_trigger.data('predict');
    var case_date = modal_trigger.data('case-date');
    var status = modal_trigger.data('status');
    var modal = $(this);
    modal.find('.modal-title').text('Save Case: '+case_id);
    modal.find('.modal-body #case-id').val(case_id);
    modal.find('.modal-body #predict').val(predict);
    modal.find('.modal-body #case-date').val(case_date);
    modal.find('.modal-body #status').val(status);
  });

  $('#save-case-button').click(function(e){
    //e.preventDefault();
    $('#save-case-form').submit();
    $('#save_case_modal').modal('hide');
    //refresh datatables
    newcase_table.row(modal_trigger.closest("tr")).remove().draw( false );
  });
});