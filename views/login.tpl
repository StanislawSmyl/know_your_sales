<link rel="stylesheet" href="/static/css/bootstrap.min.css">
<link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="/static/css/login.css">
<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
<script type="text/javascript">
	$(document).ready(function() {
		var message = {{ ! message }};
		message = message['content'];
		if(message)
			$('form.log').append('<div style = "color: red">' + message + '</div>');
	});
</script>
<div class="logContainer">
	<h1>Logging in</h1>
	<div class="logForm">
<form action="/login" method="post" class = "log">
	<input type="text" name="login_name" placeholder = "Login"><br>
	<input type="password" name="password" placeholder = "Password"><br>
	<input type="submit" value="Log in">
</form>
<form action="/registration" method="post">
	<input type="submit" value="Go to registration">
</form>
	</div>
</div>
