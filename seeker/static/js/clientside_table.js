$(document).ready(function() {
	//alert("new");
	var clientside_table = $('#case_new_table').DataTable({
		"bSort" : true,
		"bFilter" : false,
		"processing" : true,
		"bServerSide" : false,
		"aLengthMenu" : [ 10, 20 ,50 ],
		"sAjaxSource" : '/show_new_table',
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
	var modal_trigger=""

		$('#save_case_modal').on('show.bs.modal', function (event) {
		modal_trigger = $(event.relatedTarget) // Button that triggered the modal
		var case_id = modal_trigger.data('case-id') // Extract info from data-* attributes
		var predict = modal_trigger.data('predict')
		var case_date = modal_trigger.data('case-date')
		var status = modal_trigger.data('status')
		var modal = $(this)
		modal.find('.modal-title').text('Save Case: '+case_id)
		modal.find('.modal-body #case-id').val(case_id)
		modal.find('.modal-body #predict').val(predict)
		modal.find('.modal-body #case-date').val(case_date)
		modal.find('.modal-body #status').val(status)
	});

	$('#save-case-button').click(function(e){
		//e.preventDefault();
		$('#save-case-form').submit();
		$('#save_case_modal').modal('hide');
		//Todo: refresh datatables
		clientside_table.row(modal_trigger.closest("tr")).remove().draw( false );
	});
});