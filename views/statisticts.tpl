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
<script type="text/javascript">
	$(document).ready(function() {
		var pytCode, dictKeys, val, countries = {{ !countries }};
		var url = document.location.pathname.toLocaleLowerCase();
		print(countries);
		for(i = 0; i < $('.navbar-nav li').length; i++){
			if(url.indexOf($('.navbar-nav li').eq(i).text().toLocaleLowerCase()) >= 0){
				$('.navbar-nav li').eq(i).addClass('current');
				break;
			}
		}
		pytCode = {{ !stats }};
		dictKeys = Object.keys(pytCode);
		$('div.stats').append('<h3 style = "color: gray"> Statistics</h3>')
		for(i = 0; i < dictKeys.length; i++){
			val = pytCode[dictKeys[i]];
			if(typeof val === 'object'){
				var content = '';
					for(j = 0; j < val.length; j++)
						if(i in ['Total Revenue', 'Min. Price', 'Mean Price', 'Max. Price'])
							content = content + val[j] + '&amp;#163; <br>';
						else
							content = content + val[j] + '<br>';
						toApp = '<p class = arr' + i + ' style = "padding-left: 5%; clear: both; color: grey; white-space: pre-line" title = "' + content + '">' + dictKeys[i] + ' (hover to see)</p>';
						$('body').on('mouseover mouseout', '.arr' + i, function(e) {
							$(e.target).tooltipster({
								position: 'bottom',
								contentAsHTML: 'true',
								theme: 'tooltipster-punk'
							});
						});
			}
			else
				toApp = '<p style = "padding-left: 5%; clear: both; color: grey"> <strong>' + dictKeys[i] + ': </strong><span style = "color: indianred">' + val + '</span></p>';
				$('div.stats').append(toApp);
		}
		$('div.stats p:first()').css('margin-top', '9%');
		$(function(){
			$('.map').vectorMap({map: 'world_mill',
			series: {
				regions: [{
				  values: countries,
				  scale: ['#ffc8c8', '#b22946'],
				  normalizeFunction: 'polynomial'
				}]
			  },
			  onRegionTipShow: function(e, el, code){
				el.html(el.html()+' (Quantity : '+ (countries[code] ? countries[code] : 0) + ')');
			  }
			});
		});
	});
</script>

<div class = "header"> {{ selectedVal }} 
</div>
<div class = "rightSideCont">
	<div class = "stats">
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