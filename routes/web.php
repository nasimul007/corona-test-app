<?php

use Illuminate\Support\Facades\Route;

Route::get('/', 'HomeController@index')->name('home.index');
Route::get('/home', 'HomeController@index')->name('home.index');
Route::get('/home/step1', 'HomeController@step1')->name('home.step1');
Route::post('/home/step1', 'HomeController@step1Store');
Route::get('/home/record', 'HomeController@record')->name('home.record');