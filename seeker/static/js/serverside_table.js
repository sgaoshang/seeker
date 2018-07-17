$(document).ready(function() {
	$('#show_case_table').DataTable({
		"bSort" : false,
		"bFilter" : false,
		"processing" : true,
		"bServerSide" : true,
		"aLengthMenu" : [ 5, 10, 20 ],
		"sAjaxSource" : "/show_case_table",
		"columns" : [
			{
			"data" : "case_id",
			"render" : function(data, type, row, meta) {
				return data = '<a href="https://access.redhat.com/support/cases/#/case/'+data+'">'+data+'</a>';
			}}, 
			{
			"data" : "details",
			"render" : function(data, type, row, meta) {
				return data = 'details';
			}},
			{
				"data" : "predict"
			},
			{
				"data" : "validate"
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
		]
	});
});