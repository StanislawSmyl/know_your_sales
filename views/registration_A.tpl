<link rel="stylesheet" href="/static/css/registration.css">
<script src="/static/js/jquery-2.1.1.min.js" type="text/javascript"></script>
<script type="text/javascript">
	$(document).ready(function() {
		var message = {{ ! message }};
		message = message['content'];
		if(message)
			$('form').append('<div style = "color: red">' + message + ':) </div>');
	});
</script>
<div class="regContainer">
	<div class="regForm">
<form action="/registration" method="post">
	Login:    <input type="text" name="login_name"><br>
	Email: <input type="text" name="email"><br>
	Password: <input type="password" name="password"><br>
	Confirm password<input type="password" name="password2"><br>
	<input type="submit" value="Register">
</form>

	</div>
</div>
