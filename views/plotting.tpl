% rebase('base.tpl', title='Search')
<link rel="stylesheet" href="/static/css/plotsStyle2.css">
<link rel="stylesheet" href="/static/css/styles2.min.css">
<link rel="stylesheet" href="static/css/jquery-jvectormap-2.0.3.css">
<link rel="stylesheet" href="static/css/tooltipster.bundle.min.css">
<link rel="stylesheet" href="static/css/tooltipster-sideTip-punk.min.css">
<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
<script src="/static/js/tooltipster.bundle.min.js" type="text/javascript"></script>
<script src="/static/js/jquery-jvectormap-2.0.3.min.js" type="text/javascript"></script>
<script src="/static/js/jquery-jvectormap-world-mill.js" type="text/javascript"></script>
<script src="/static/js/jsPlot.js" type="text/javascript"></script>
<script type="text/javascript">
	$(document).ready(function() {
		var url = document.location.pathname.toLocaleLowerCase();
		for(i = 0; i < $('.navbar-nav li').length; i++){
			if(url.indexOf($('.navbar-nav li').eq(i).text().toLocaleLowerCase()) >= 0){
				$('.navbar-nav li').eq(i).addClass('current');
				break;
			}
		}
	});
</script>

<div class = "header"> {{ selectedVal }} 
</div>
<div class = "rightSideCont">
	<div class = "stats">
		<div class = 'pytCode'> {{ stats }} 
		</div>
	</div>
	<div class= "map">
	</div>
</div>
<div class = "allPlots">
	<div class = "plotsContainer1">
		<iframe class = "line1" frameborder="0" scrolling="no" src="//plot.ly/~SSMYL/5.embed?showlink=false"></iframe>
	</div>
	<div class = "plotsContainer2">
		<iframe class = "bar1" frameborder="0" scrolling="yes" src="//plot.ly/~SSMYL/11.embed?showlink=false"></iframe>
	</div>
	<div class = "plotsContainer3">
		<iframe class = "bar1" frameborder="0" scrolling="yes" src="//plot.ly/~SSMYL/15.embed?showlink=false"></iframe>
	</div>
	<div class = "plotsContainer4">
		<iframe class = "bar1" frameborder="0" scrolling="yes" src="//plot.ly/~SSMYL/13.embed?showlink=false"></iframe>
	</div>
</div>