<!DOCTYPE html>
<html>
<head>
	<title>step-1 corona self assesment</title>
	<style>
		.center {
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
		<h2>COVID-19 Self-Assessment System</h2>

		<form method="post">
			<input type="hidden" name="_token" value="{{ csrf_token() }}">
			<fieldset>
				<legend>Step 1</legend>
				<table>
					<tr>
						<td>Age :</td>
						<td><input type="text" name="age" value="{{old('age')}}"></td>
					</tr>
					<tr>
						<td>Sex :</td>
						<td>
							<select name="sex">
								<option value="Male"> Male</option>
								<option value="Female"> Female</option>
								<option value="Other"> Other</option>
							</select>
						</td>
					</tr>
					<tr>
						<td>Body temperature : </td>
						<td><input type="text" name="temp" value="{{old('temp')}}"> 
							<select name="tempOption">
								<option value="c"> °C</option>
								<option value="f"> °F</option>
							</select></td>
					</tr>
					<!-- <tr>
						<td>
							<input type="submit" name="submit" value="Next Step">
							<input type="reset" name="reset" value="Reset">
						</td>
					</tr> -->
			</table>
			</fieldset>

			<fieldset>  
			    <legend>Step 2</legend>
			    Do you have any of below symptoms (You may control-click (Windows) or command-click (Mac) to select more than one) <br>
			    <input type="checkbox" name="symptoms1[]" value="breath" onclick="return Symptoms1Selection();">Breathing problem <br>  
			    <input type="checkbox" name="symptoms1[]" value="cough" onclick="return Symptoms1Selection();">Dry cough<br>  
			    <input type="checkbox" name="symptoms1[]" value="throat" onclick="return Symptoms1Selection();">Sore throat<br>  
			    <input type="checkbox" name="symptoms1[]" value="weak" onclick="return Symptoms1Selection();">Weakness<br>  
			    <input type="checkbox" name="symptoms1[]" value="nose" onclick="return Symptoms1Selection();">Runny nose<br>  
			    <br>  
			    <!-- <input type="submit" value="Submit now">   -->
	    	</fieldset> 

	    	<fieldset>  
			    <legend>Step 3</legend>
			    Do you have any of below symptoms (You may control-click (Windows) or command-click (Mac) to select more than one) <br>
			    <input type="checkbox" name="symptoms2[]" value="abdominal" onclick="return Symptoms2Selection();">Abdominal Pain <br>  
			    <input type="checkbox" name="symptoms2[]" value="diarrhoea" onclick="return Symptoms2Selection();">Diarrhoea<br>  
			    <input type="checkbox" name="symptoms2[]" value="chest" onclick="return Symptoms2Selection();">Chest pain or pressure<br>  
			    <input type="checkbox" name="symptoms2[]" value="muscle" onclick="return Symptoms2Selection();">Muscle pain<br>  
			    <input type="checkbox" name="symptoms2[]" value="taste" onclick="return Symptoms2Selection();">Loss of taste or smell<br>  
			    <input type="checkbox" name="symptoms2[]" value="rash" onclick="return Symptoms2Selection();">Rash on skin, or discoloration of fingers or toes<br>  
			    <input type="checkbox" name="symptoms2[]" value="speech" onclick="return Symptoms2Selection();">Loss of speech or movement<br>  
			    <br>  
	    	</fieldset> 
	    	<input type="submit" name="submit" value="Submit" class="button">
		</form>
		<footer>
		  	<p align="center">This COVID-19 Self Assessment System is only for software development purpose and may not yield actual result.<br> Any information given by users of this system will not be disclosed or store to anywhere.</p>
		</footer>
	</div>
</body>
</html>