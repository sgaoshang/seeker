$(document).ready(function() {
	//alert("new");
	$('#case_new_table').DataTable({
		"bSort" : false,
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
					return '<a href="#" class="badge badge-primary" data-toggle="modal" data-target="#save_case_modal" data-case-id="'+row.case_id+'" data-predict="'+row.predict+'" data-case-date="'+row.case_date+'" data-status="'+row.status+'">save</a>';
				}
			},
		],
	});
});