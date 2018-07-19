% rebase('base.tpl', title='Search for products')
	<link rel="stylesheet" href="static/css/rules2.css">
	<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
	<script type="text/javascript">
	$(document).ready(function() {
		console.log({{ !rules }});
		var rules = {{ !rules }};
		var dictKeys = Object.keys(rules);
		var url = document.location.pathname.toLocaleLowerCase();
		for(i = 0; i < $('.navbar-nav li').length; i++){
			if(url.indexOf($('.navbar-nav li').eq(i).text().toLocaleLowerCase()) >= 0){
				$('.navbar-nav li').eq(i).addClass('current');
				break;
			}
		}
		if(dictKeys.length === 0)
			$('body').append('<div class = "message">There was not enought transaction with this product to make any rules.</div>');
		console.log(dictKeys);
		for(i = 0; i < dictKeys.length; i++){
			$('.mainCont').append("<div class = '" + "rulesContainer rulesContainer" + i + "'><div class = 'header'></div><div class = 'support'></div><div class = 'confidence'></div><div class = 'lift'></div></div>");
			$('.rulesContainer' + i + ' .header').append('(' + rules[i]['antecedants'].join().split(',').join(', ') + ') => (' + rules[i]['consequents'].join().split(',').join(', ') + ')');
			if(rules[i]['antecedants'].join().split(',').length > 1){
				$('.rulesContainer' + i + ' .support').append('Products (<b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b>) was purchased together in <span class = "num"><b>' + Math.round(rules[i]['support'] * 10000) / 100 + '% </b></span> of all transactions');
				$('.rulesContainer' + i + ' .confidence').append('People, who bought (<b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b>), with <span class = "num"><b>' + Math.round(rules[i]['confidence'] * 10000) / 100 +  '%</b></span> confidence will buy also ' + (rules[i]['consequents'].join().split(',').length > 1 ? ('<b>products (' + rules[i]['consequents'].join().split(',').join(', ') + '</b>)') : ('product <b>' + rules[i]['consequents'].join().split(',').join(', ') + '</b>')));
				$('.rulesContainer' + i + ' .lift').append('Person, who got products (<b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b>) already in basket is <span class = "num"><b>' + rules[i]['lift'] + '</b></span> times more likely to buy also ' + (rules[i]['consequents'].join().split(',').length > 1 ? ('products <b>(' + rules[i]['consequents'].join().split(',').join(', ') + '</b>)') : ('product <b>' + rules[i]['consequents'].join().split(',').join(', ') + '</b>')) + ' than a person, who plans to buy only second one');
			}
				
			else{
				$('.rulesContainer' + i + ' .support').append('Product <b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b> was bought in <span class = "num"><b>' + Math.round(rules[i]['support'] * 10000) / 100 + '% </b></span> of all transactions');
				$('.rulesContainer' + i + ' .confidence').append('People, who bought <b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b>, with <span class = "num"><b>' + Math.round(rules[i]['confidence'] * 10000) / 100 +  '%</b></span> confidence will buy also ' + (rules[i]['consequents'].join().split(',').length > 1 ? ('<b>products (' + rules[i]['consequents'].join().split(',').join(', ') + '</b>)') : ('product <b>' + rules[i]['consequents'].join().split(',').join(', ') + '</b>')));
				$('.rulesContainer' + i + ' .lift').append('Person, who got product <b>' + rules[i]['antecedants'].join().split(',').join(', ') + '</b> already in basket is <span class = "num"><b>' + rules[i]['lift'] + '</b></span> times more likely to buy also ' + (rules[i]['consequents'].join().split(',').length > 1 ? ('products <b>(' + rules[i]['consequents'].join().split(',').join(', ') + '</b>)') : ('product <b>' + rules[i]['consequents'].join().split(',').join(', ') + '</b>')) + ' than a person, who plans to buy only second one');
			}
		}
	});
	</script>
	<div class = "mainCont"></div>