<!doctype html>
<html ng-app="MainApp">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="cache-control" content="max-age=0" />
    <meta http-equiv="cache-control" content="no-cache" />
    <meta http-equiv="expires" content="0" />
    <meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
    <meta http-equiv="pragma" content="no-cache" />
	
    <title>Python Bottle Web App</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="/static/css/style.css">
	<link rel="stylesheet" href="/static/css/baseStyling2.css">
  </head>
  <body>
      <nav class="navbar navbar-default">
        <div class="container-fluid">
          <div class="navbar-header">
            <a class="navbar-brand" href="/searchSite">Analitics engine</a>
          </div>
          <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li class = "site"><a href="/statistics">Statistics</a></li>
              <li class = "site"><a href="/rules">Rules</a></li>
            </ul>
			<a class = "logOut" href="/loggingOut">Log out, {{ login }}</a>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
		
      </nav>
	  
    <div class="container">

      {{!base}}
    </div>

  </body>
</html>
