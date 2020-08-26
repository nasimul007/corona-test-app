<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Coronadb;
use Illuminate\Support\Facades\DB;

class HomeController extends Controller
{
    public function index()
    {
        return view('home.index');
    }

    public function step1()
    {
        return view('home.step1');
    }

    //function to store all data to database
    public function step1Store(Request $request)
    {
        $data = new Coronadb();
        $data->age = $request->age;
        $data->sex = $request->sex;
        $data->temperature = $request->temp;
        $data->assessment_date = date("Y-m-d");
        $tempOption = $request->tempOption;
        $symptom1 = $request->symptoms1;
        $symptom2 = $request->symptoms2;
        $s1 = 0;
        $s2 = 0;
        $score = 0;

        if ($request->temp > 37.5 && $tempOption == 'c') {
            $score += 2;
        }
        elseif ($request->temp > 99.5 && $tempOption == 'f') {
            $score += 2;
        }

        if ($symptom1) {
            foreach ($symptom1 as $sym) {
                $s1++;
            }
            if ($s1 == 1) {
                $score += 3;
            }
            elseif ($s1 > 1 ) {
                $score += 3;
                $s1--;
                for ($i=0; $i < $s1; $i++) { 
                    $score += 1;
                }
            }
        }
        if ($symptom2) {
            foreach ($symptom2 as $sym) {
                $s2++;
            }
            if ($s2 > 0) {
                for ($i=0; $i < $s2; $i++) { 
                    $score += 2;
                }
            }   
        }
        $data->assessment_score = $score;

        if ($score < 5) {
            $data->result = "Negative";
        }
        elseif ($score >= 5) {
            $data->result = "Positive";    
        }

        //saving ti database
        if ($data->save()) {
            if($score < 5){
                return view('home.suggestion')->with('score', $score);
            }
            elseif($score == 5){
                return view('home.suggestion')->with('score', $score);
            }
            elseif($score > 5 && $score <= 7){
                return view('home.suggestion')->with('score', $score);
            }
            if($score > 7){
                return view('home.suggestion')->with('score', $score);
            }
        }

    }

    public function record()
    {
        $records = DB::table('coronadbs')->get();
        return view('home.recordList')->with('records', $records);
    }
}
