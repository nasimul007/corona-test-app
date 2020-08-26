<!DOCTYPE html>
<html>
<head>
	<title>corona self assesment</title>
	<!-- <meta name="viewport" content="width=device-width, initial-scale=1.0"> -->
	<style>
		.center {
			text-align: center;
			margin: auto;
			width: 60%;
			border: 3px solid #73AD21;
			padding: 10px;
		}
		.button {
	        background-color: #1c87c9;
	        border: none;
	        color: white;
	        padding: 10px 25px;
	        text-align: center;
	        text-decoration: none;
	        display: inline-block;
	        font-size: 20px;
	        margin: 4px 2px;
	        cursor: pointer;
      	}
	</style>
</head>
<body>
	<div class="center">
		<h1>Welcome To COVID-19 Self-Assessment System</h1>
		<h3>it is a wizard-based system to get questionnaires about symptoms and syndromes</h3>
		<h4>On each step, give the confirmation that information are correct and proceed to next step.</h4>

		<a href="{{route('home.step1')}}" class="button"> Take the assessment </a> 
		<br>
		<a href="{{route('home.record')}}" class="button"> View all the previous records </a>

		<footer>
		  	<p>This COVID-19 Self Assessment System is only for software development purpose and may not yield actual result.<br> Any information given by users of this system will not be disclosed or store to anywhere.</p>
		</footer>
	</div>
</body>
</html>