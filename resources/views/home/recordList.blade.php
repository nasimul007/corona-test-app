<!DOCTYPE html>
<html>
<head>
	<title>corona self assesment records</title>
	<style>
		table {
		  	border-collapse: collapse;
		}
		table, td, th {
		  	border: 1px solid black;
		}
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
		<h1>All COVID-19 Self-Assessment Records</h1>

		<table align="center">
			<tr>
				<th>Sl No.</th>
				<th>Age</th>
				<th>Sex</th>
				<th>Temperature</th>
				<th>Assessment Date</th>
				<th>Assessment Score</th>
				<th>COVID-19 Result</th>
			</tr>
			@foreach($records as $r)
			<tr>
				<td>{{$r->sl_no}}</td>
				<td>{{$r->age}}</td>
				<td>{{$r->sex}}</td>
				<td>{{$r->temperature}}</td>
				<td>{{$r->assessment_date}}</td>
				<td>{{$r->assessment_score}}</td>
				<td>{{$r->result}}</td>
			</tr>
			@endforeach
		</table>

		<a href="{{route('home.index')}}" class="button"> Back To Home </a>
		<footer>
		  	<p>This COVID-19 Self Assessment System is only for software development purpose and may not yield actual result.<br> Any information given by users of this system will not be disclosed or store to anywhere.</p>
		</footer>
	</div>
</body>
</html>