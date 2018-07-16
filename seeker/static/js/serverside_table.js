//$(document).ready(function() {
//	$('#show_case_table').DataTable({
//		"ordering" : false,
//		"processing" : true,
//		"serverSide" : true,
//		"sPaginationType" : "full_numbers",
//		"lengthMenu" : [ [ 5, 10, 20 ], [ 5, 10, 20 ] ],
//		"bjQueryUI" : true,
//		"sAjaxSource" : "/show_case_table",
//	});
//});

$(document).ready(function() {
	$('#show_case_table').DataTable({
		"bSort" : false,
		"bFilter":false,
		"processing" : true,
		"bServerSide" : true,
		"lengthMenu": [ [ 5, 10, 20 ], [ 5, 10, 20 ] ],
		"sAjaxSource" : "/show_case_table"
	});
});

//"aoColumns" : [{  
//    "mData" : 'id',  
//    "sTitle" : "ID",  
//    "bSortable" : true  
//},{  
//    "mData" : 'name',  
//    "sTitle" : "Name",  
//    "bSortable" : true  
//},{  
//    "mData" : 'age',  
//    "sTitle" : "Age",  
//    "bSortable" : true,  
//    "mRender" : function(data, type, row) {  
//        return data;  
//    }  
//},{  
//    "mData" : 'work',  
//    "sTitle" : "Work",  
//    "bSortable" : true  
//}],

// DataTables has six built-in paging button arrangements:
//
// numbers - Page number buttons only (1.10.8)
// simple - 'Previous' and 'Next' buttons only
// simple_numbers - 'Previous' and 'Next' buttons, plus page numbers
// full - 'First', 'Previous', 'Next' and 'Last' buttons
// full_numbers - 'First', 'Previous', 'Next' and 'Last' buttons, plus page
// numbers
// first_last_numbers - 'First' and 'Last' buttons, plus page numbers
