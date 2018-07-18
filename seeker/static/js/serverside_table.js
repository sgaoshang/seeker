$(document).ready(function() {
	$('#show_case_table').DataTable({
		"bSort" : false,
		"bFilter" : false,
		"processing" : true,
		"bServerSide" : true,
		"aLengthMenu" : [ 10, 20 ,50 ],
		"sAjaxSource" : "/show_case_table",
		"columns" : [
			{
				"data" : "case_id",
				"render" : function(data, type, row, meta) {
					return data = '<a href="https://access.redhat.com/support/cases/#/case/'+data+'">'+data+'</a>';
				}
			}, 
			{
				"data" : "details",
				"render" : function(data, type, row, meta) {
					//return data = 'details'+row.case_id;
					//return data = '<button type="button" class="btn btn-outline-secondary btn-sm" data-toggle="modal" data-target="#case_details_modal">details</button>'
					//return data = '<button type="button" class="btn btn-outline-secondary btn-sm" data-toggle="modal" href="#case_details_modal">details</button>'
					//return data = '<a href="show_case_details" class="badge badge-secondary">details</a>';
					//return data = '<a class="badge badge-secondary" data-toggle="modal" data-target="#case_details_modal">details</a>';
					return data = '<a href="" class="badge badge-secondary" data-toggle="modal" data-target="#case_details_modal" data-case-id="'+row.case_id+'">details</a>';
				}
			},
			{
				"data" : "predict"
			},
			{
				"data" : "validate",
				//"render": function (data, type, row, meta) {
				//	return data = '<button class="btn btn-info btn-sm" data-id=' + data + '><i class="fa fa-pencil"></i>Edit</button>';
				//}
			},
			{
				"data" : "case_date"
			},
			{
				"data" : "case_cover"
			},
			{
				"data" : "bug_cover"
			}
		],
	});
});