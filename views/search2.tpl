    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="/static/css/baseStyling.css">
	<link rel="stylesheet" href="/static/css/search.css">
	<link rel="stylesheet" href="/static/css/font-awesome.min.css">
	<link rel="stylesheet" href="/static/css/select2.min.css" />
	<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
	<script src="/static/js/select2.min.js"></script>
	<script type="text/javascript">
	$(document).ready(function() {
		console.log({{ !products }});
		var prodList, prodDate;
		var prodList = {{ !products }}; //JSON.parse({{ !products }}); 
		console.log(prodList);
		var prodDate = Object.values(prodList);
		prodDate = prodDate.filter( function(x) { return x != null });
		console.log(prodDate);	
		$(".searchForm").select2({
			placeholder: "Select product",
			data: prodDate
		});
});
	</script>
<div class = 'searchContainer'>
	<h1>Select product, {{ login }}</h1>
	<div>
		<form action="/searchSite2" method="post">
			<select class="searchForm" name = "sel">
			<option></option>
			</select>
			<button type="submit"><i class="fa fa-search"></i></button>
			<div class="error" style="color: red; padding-left: 8px; clear:both; "> Please, select product :) </div>
		</form>
	</div>
	
</div>