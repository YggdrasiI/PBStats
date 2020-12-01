<?php

// set $subdir to ../ if the php file will move to a subdirectory.
//$subdir = "../";
$subdir = "";

include_once("php/header_all_pages.php");

//The database has has no user table. Init database and try again.
init_main_database_tables();
init_game_database_tables();
