<!DOCTYPE html>
<html>
<head>
	<title>corona self suggestion</title>
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
		<h2>Suggetion based on your COVID-19 test assessment</h2>

		@if($score < 5)
			<p>You Merely have chance to get affected by COVID-19. You're adviced for isolation and contact doctor and follow advice.</p>
		@elseif($score === 5)
			<p>Possible suspected case for COVID-19 affected. You're adviced for isolation and contact doctor and follow advice.</p>
		@elseif($score > 5 && $score <= 7)
			<p>Highly chance of COVID-19 affected. You're adviced for isolation and contact doctor immediately and follow advice.</p> 
			<p> Here's a list of emergency phone numbers to contact in case of any emergency.</p>
			<ul>
			  	<li>01401184551</li>
			  	<li>01937000011</li>
			  	<li>01401184559</li>
			  	<li>01401184555</li>
			  	<li>01927711785</li>
			</ul>
		@elseif($score > 7)
			<p>
				Almost confirmed case of COVID-19 positive. You're adviced for isolation and contact doctor immediately and follow advice. You're Highly adviced to be hospitalized.
			</p>
			<p>Here's a list of emergency phone numbers to contact in case of any emergency</p>
			<ul>
			  	<li>01401184551</li>
			  	<li>01937000011</li>
			  	<li>01401184559</li>
			  	<li>01401184555</li>
			  	<li>01927711785</li>
			</ul>
		@endif

		<a href="{{route('home.index')}}" class="button"> Go To Home </a>

		<footer>
		  	<p>This COVID-19 Self Assessment System is only for software development purpose and may not yield actual result.<br> Any information given by users of this system will not be disclosed or store to anywhere.</p>
		</footer>
	</div>

</body>
</html>