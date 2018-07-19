$(document).ready(function() {
	//x = {{ !products }};
	//console.log(x);
	//console.log('xxx', JSON.parse({{ !products }}));
	var prodList = $('p').html(), prodDate;
	prodList = JSON.parse(prodList);
	console.log(prodList);
	var prodDate = Object.values(prodList);
	prodDate = prodDate.filter( function(x) { return x != null });
	console.log(prodDate);	
	$(".searchForm").select2({
		placeholder: "Select product",
		data: prodDate
	});
});