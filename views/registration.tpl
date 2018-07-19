<link rel="stylesheet" href="/static/css/bootstrap.min.css">
<link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="/static/css/registration.css">
<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
<script type="text/javascript">
	$(document).ready(function() {
		var message = {{ ! message }};
		message = message['content'];
		if(message)
			$('form.reg').append('<div style = "color: red">' + message + ':) </div>');
	});
</script>
<div class="regContainer">
	<h1>Registration</h1>
	<div class="regForm">
<form action="/registration" method="post" class = "reg">
	<input type="text" name="login_name" placeholder = "Login"><br>
	<input type="text" name="email" placeholder = "Email"><br>
	<input type="password" name="password" placeholder = "Password"><br>
	<input type="password" name="password2" placeholder = "Confirm password"><br>
	<input type="submit" value="Register">
</form>
<form action="/login" method="post">
	<input type="submit" value="Log in">
</form>

	</div>
</div>
