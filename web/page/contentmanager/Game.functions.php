<?php

include_once($subdir."php/pbModFunctions.php");

function gamePreview($game){
	if(!array_key_exists("id",$game))$game["id"] = "-1";
	return gameFull($game,0);
}

function gameShort($game){
	global $otherReferer, $subdir;
	$dHtml = '';
	if( isset($otherReferer) ){
	$dHtml .= '<h4>'.$game['id'].' - '.$game['name'].'</h4><p>';
	$dHtml .=	call_user_func($otherReferer,$game);
	$dHtml .= "</p>";
	}else{
		$dHtml .= '<p class="gametitle" ><a href="'.$subdir.'games.php?game='.$game['id'].'">'.$game['name'].'</a></p>';
	}

	//	$dHtml .= '<p><a href="'.$subdir.'games.php?game='.$game['id'].'">{L_CM_GAME_SHOW_DETAILS}</a></p>');
	
	return $dHtml;
}

/* $online=0 reduce the display to
 * values of the games table .*/
function gameFull($game,$online /* False for preview during creation of new game entry */ ){
	global $otherReferer, $subdir;
	$dHtml = '<h2 style="display:inline"><a href="'.(isset($otherReferer)?call_user_func($otherReferer,$game):$subdir.'games.php?game='.$game["id"]).'">'.$game['name'].'</a></h2><p>';

	if( $online ){

		$this_page = $_SERVER['PHP_SELF'];
		$gameId = $game["id"];
		$action = "list";
		if( isset($_GET["action"] ) ){
			$action = $_GET["action"];
		}
		$dHtml .= '<p class ="game_navlinks">
			<a href="games.php?game='.$gameId.'&action=list">{L_GAME_STATUS}</a> 
			<a href="games.php?game='.$gameId.'&action=log">{L_GAME_LOG}</a> 
			<a href="games.php?game='.$gameId.'&action=admin">{L_GAME_ADMIN}</a> 
			</p>';

		//Read game config from db
		$gameData = get_game_data($gameId);


	}


	/*
	if(hasValue('url',$game)){
		$dHtml .= "{L_CM_GAME_URL}: ". $game['url'];
		if(hasValue('port',$game)) $dHtml .= ":" . $game['port']; 
		$dHtml .= "</p><p>";
	}
	if(hasValue('description',$game)){
		//$dHtml .= "{L_CM_GAME_DESCRIPTION}: ". $game['description'] . "</p><p>";
		$dHtml .= $game['description'] ; 
	}
	if(hasValue('infolink',$game)) $dHtml .= '{L_FURTHER_INFO}: <a href="'.(isRelativePath($game['infolink'])?$subdir:"").$game['infolink'].'">Link</a></p>';
*/


	if( $online ){
		
		{

			$mainpageLink = "<p><a href='$this_page?game=$gameId&action=list'>Return to main page</a></p>\n";

			//Check if password for webinterface of this game is stored
			$pw = "";
			if( array_key_exists( "passwordFor".$gameId, $_COOKIE ) ){
				$pw = $_COOKIE["passwordFor".$gameId];
			}else if( array_key_exists( "pw", $_GET) ){
				$pw = $_GET["pw"];
			}

			$operationIds = array(-1=>-1);
			if( array_key_exists( "operationIds", $_COOKIE ) ){
				$operationIds = json_decode( $_COOKIE["operationIds"], true );
			}
			//print_r ( $operationIds );


			if(( $action === "admin"
				|| $action === "save"
				|| $action === "restart"
			) &&  !matchingGamePassword($gameId, $gameData) )
			{
				// Wrong password. Change action to password request.
				$action = "setWebserverpassword";
			}else{
				//Get a list of operationids 
				/* Well, quite similar to 'form ids', but stored in cookie, not in the session vars.
				 * Can be replaced by session based array....
				 */
				global $operationIds;
				$operationIds = array(-1=>-1);
				if( array_key_exists( "operationIds", $_COOKIE ) ){
					$operationIds = json_decode( $_COOKIE["operationIds"], true );
				}

			}


			if( $action === "list" ){
				$dHtml .= display_game_info($gameData);
			}
			if( $action === "log" ){
				$dHtml .= display_game_log($gameData);
			}

			if( $action === "setWebserverpassword" ){
				/* Stores the (game admin) password of in a cookie.
				 * The value will be attached to all operation which requires
				 * a password. 
				 * Attention, everything unencrypted.
				 */

				$step = 0;
				if( isset($_GET["step"]) ){
					$step = $_GET["step"];
				}

				if( $step == 1 ){
					$newpw = $_GET["pw"];
					$expire=time()+60*60*24*30;
					setcookie("passwordFor".$gameId, $newpw, $expire);
					$dHtml .= "<p>Save game password. New value: $newpw</p>";
				}else{
					$dHtml .= "<p>{L_GAME_NOTES_PASSWORD}</p>\n";
					$dHtml .= "<form action='$this_page' method='get'>\n
						<p>Password: <input type='password' name='pw' value='$pw' /></p>\n
						<p><input type='submit' />\n
						<input type='hidden' name='action' value='setWebserverpassword' />\n
						<input type='hidden' name='game' value='$gameId' />\n
						<input type='hidden' name='step' value='1' />\n
						</p></form>\n";
				}
				$dHtml .= $mainpageLink;
			}

			if( $action === "save" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_SAVE}</h3>";
				if( $step == 1 ){
					$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
					if( operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{
						$fn = $_GET["filename"];
						$pbAction = array('action'=>'save','password'=>$pw,'filename'=>$fn);
						$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

						if( $infos->return === "ok" ){
							$dHtml .= "<p>{L_GAME_SAVE_FILE|$fn}</p>";
							operation_update_ids( $opid );
						}else{
							$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
						}
					}
				}else{
					$dHtml .= "<p>{L_GAME_NOTES_SAVE_FILE}</p>";
					//request to get actual round
					$opid = operation_new_val();

					$action_info = array('action'=>'info');
					$infos = json_decode(handle_pitboss_action($gameData, $action_info));
					$fn = "";
					if( $infos->return === "ok" ){
						$fn = $infos->info->gameName . "_R".$infos->info->gameTurn."_".$infos->info->gameDate;
					}

					$dHtml .= "<form action='$this_page' method='get'>\n
						<p>{L_FILE}: <input style='text-align:center;' type='text' name='filename' value='$fn' />.CivBeyondSwordSave</p>\n
						<p><input type='submit' />\n
						<input type='hidden' name='action' value='save' />\n
						<input type='hidden' name='game' value='$gameId' />\n
						<input type='hidden' name='step' value='1' />\n
						<input type='hidden' name='opid' value='$opid' />\n
						</p></form>\n";
				}
				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;
			}


			if( $action === "admin" ){

				//check if game webpassword matching with cookie value

				$step = 0;
				if( isset($_GET["step"]) ){
					$step = $_GET["step"];
				}

				$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
				if( $step > 0 ){

					if( operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{

						if( $step == 1 ){
							// Pause/Unpause
							$pause = intval($_GET["value"]);
							$pbAction = array('action'=>'setPause','password'=>$pw,'value'=>$pause);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_PAUSE_SUCCESSFUL|$pause}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}


						if( $step == 2 ){
							// End turn
							$confirm = false;
							if( isset($_GET["confirm"]) ){
								$confirm = $_GET["confirm"];
							}

							if( $confirm === "yes" ){
								$pbAction = array('action'=>'endTurn','password'=>$pw);
								$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

								if( $infos->return === "ok" ){
									$dHtml .= "<p>{L_GAME_END_TURN_SUCCESSFUL}</p>";
									operation_update_ids( $opid );
								}else{
									$dHtml .= "<p>{L_GAME_END_TURN_ERROR}: ".$infos->info ."</p>";
								}
							}else{
								$dHtml .= "<h3 class='hr pad'>{L_WARNING}</h3><p>{L_GAME_END_TURN_ASK} 
									<a href='$this_page?game=$gameId&action=admin&step=2&opid=$opid&confirm=yes'>{L_CONFIRM}</a></p>";
							}
						}

						if( $step == 3 ){
							// Send chat message
							$msg = $_GET["msg"];
							$pbAction = array('action'=>'chat','password'=>$pw,'msg'=>$msg);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_CHAT_MESSAGE_SUCCESSFUL|$msg}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

						if( $step == 4 ){
							// Set timer for next round
							$hours = $_GET["hours"];
							$pbAction = array('action'=>'setTurnTimer','password'=>$pw,'value'=>$hours);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_SET_TIMER_SUCCESSFUL|$hours}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

						if( $step == 5 ){
							// Set timer for next round
							$value = $_GET["value"];
							$pbAction = array('action'=>'setAutostart','password'=>$pw,'value'=>$value);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_SUCCESS_MSG}".$infos->info ."</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

						if( $step == 6 ){
							// Set password of player
							$playerId = intval($_GET["playerId"]);
							$newCivPW = "" . $_GET["newCivPW"];
							$pbAction = array('action'=>'setPlayerPassword','password'=>$pw,'playerId'=>$playerId,'newCivPW'=>$newCivPW);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_PASSWORD_SUCCESS}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_PASSWORD_ERROR}".$infos->info ."</p>";
							}

						}

						if( $step == 7 ){
							// Set headless mode
							$value = $_GET["value"];
							$pbAction = array('action'=>'setHeadless','password'=>$pw,'value'=>$value);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_SUCCESS_MSG}".$infos->info ."</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

						if( $step == 8 ){
							// Change message of the day (MotD)
							$msg = $_GET["msg"];
							$pbAction = array('action'=>'setMotD','password'=>$pw,'msg'=>$msg);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_MOTD_MESSAGE_SUCCESSFUL|$msg}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

						if( $step == 9 ){
							/* Toggle short names of leadernames and (default) nation names.
							 * This could be ness. to omit connection issues during login
							 * for games with many players.
							 * Use 0 to disable.
							 */
							$iShortNamesLen = intval($_GET["shortNames"]);
							$iShortDescLen = intval($_GET["shortDesc"]);
							if( $iShortNamesLen > 0 ){
								$pbAction = array('action'=>'setShortNames','password'=>$pw,
									'enable'=>True, 'maxLenName'=>$iShortNamesLen, 
									'maxLenDesc'=>$iShortDescLen, 
								);
							}else{
								$pbAction = array('action'=>'setShortNames','password'=>$pw,
									'enable'=>False);
							}
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_SHORT_NAMES_SUCCESSFUL|$iShortNamesLen|$iShortDescLen}</p>";
								operation_update_ids( $opid );
							}else{
								$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
							}
						}

					}//end operation already done check

					$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";

				}else{ //print menu if no step>0 is given


					//Generate new id for the next command and store this in the operation cookie.
					$opid = operation_new_val();

					// List Commands

					$action_info = array('action'=>'info');
					$infos = json_decode(handle_pitboss_action($gameData, $action_info));
					if( $infos->return === "ok" ){

						$dHtml .= "<h3 class=''><a href='$this_page?game=$gameId&action=save&opid=$opid'>{L_GAME_SAVE}</a></h3>";
						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=restart&opid=$opid'>{L_GAME_RESTART}</a></h3>";
						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=setWebserverpassword'>{L_GAME_WEBSERVERPASSWORD}</a></h3>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_PAUSE}</h3>";
						if( $infos->info->bPaused ){
							$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=1&value=0'>{L_GAME_PAUSE_DISABLE}</a><br>";
						}else{
							$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=1&value=1'>{L_GAME_PAUSE_ENABLE}</a><br>";
						}

						$dHtml .= "<h3 class='hr pad'><a href='$this_page?game=$gameId&action=admin&opid=$opid&step=2'>{L_GAME_END_ROUND}</a></h3>";
						$dHtml .= "<p>{L_GAME_NOTES_END_ROUND}</p>";

						if( isset( $infos->info->turnTimerMax ) ){
							$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_TIMER}</h3>";
							$dHtml .= "<p>{L_GAME_NOTES_SET_TIMER}</p>";
							$dHtml .= "<form action='$this_page' method='get'>\n
								<p>{L_HOURS}: <input type='text' name='hours' value='".$infos->info->turnTimerMax."' />\n
								<input type='submit' />\n
								<input type='hidden' name='action' value='admin' />\n
								<input type='hidden' name='game' value='$gameId' />\n
								<input type='hidden' name='step' value='4' />\n
								<input type='hidden' name='opid' value='$opid' />\n
								</p></form>\n";
						}

						$dHtml .= "<h3 class='hr pad'>{L_GAME_CHAT_MESSAGE}</h3>";
						$dHtml .= "<form action='$this_page' method='get'>\n
							<p>{L_MESSAGE}: <input type='text' name='msg' value='' />\n
							<input type='submit' />\n
							<input type='hidden' name='action' value='admin' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='3' />\n
							<input type='hidden' name='opid' value='$opid' />\n
							</p></form>\n";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_MOTD_MESSAGE}</h3>";
						$dHtml .= "<form action='$this_page' method='get'>\n
							<p>{L_MESSAGE}: <input type='text' name='msg' value='' />\n
							<input type='submit' />\n
							<input type='hidden' name='action' value='admin' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='8' />\n
							<input type='hidden' name='opid' value='$opid' />\n
							</p></form>\n";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_SHORT_NAMES}</h3>";
						$dHtml .= "<form action='$this_page' method='get'>\n
							<p>{L_LEADER_NAME}: <input type='number' name='shortNames' value='2' style='width:3em' />\n
						{L_CIV_DESC}: <input type='number' name='shortDesc' value='3' style='width:3em' />
							<input type='submit' />\n
							<input type='hidden' name='action' value='admin' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='9' />\n
							<input type='hidden' name='opid' value='$opid' />\n
							</p></form>
							<p>{L_GAME_SHORT_NAMES_DESC}</p>\n";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_AUTOSTART_FLAG}</h3>";
						$dHtml .= "<p>{L_GAME_NOTES_AUTOSTART}</p>";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=5&value=1'>{L_GAME_AUTOSTART_ENABLE}</a> ";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=5&value=0'>{L_GAME_AUTOSTART_DISABLE}</a><br>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_HEADLESS_FLAG}</h3>";
						$dHtml .= "<p>{L_GAME_NOTES_HEADLESS}</p>";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=7&value=1'>{L_GAME_HEADLESS_ENABLE}</a> ";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=7&value=0'>{L_GAME_HEADLESS_DISABLE}</a><br>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_PLAYER_PASSWORD_CHANGE}</h3>";
						$dHtml .= "<p>{L_GAME_NOTES_PLAYER_PASSWORD}</p>";
						$dHtml .= "<form action='$this_page' method='get'>\n
							<p>{L_GAME_PLAYER}: ";
						$dHtml .= "<select name='playerId'>";
						foreach( $infos->info->players as $player ){
							$playerId = $player->id;
							$playerName = $player->name;
							$dHtml .= "<option style='text-align:left;' value='$playerId'>$playerId - $playerName</option>";
						}
						$dHtml .= "</select><br>";	

						$dHtml .= "{L_GAME_PASSWORD}: <input type='text' name='newCivPW' value='' />\n
							<input type='submit' /><br>\n
							<input type='hidden' name='action' value='admin' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='6' />\n
							<input type='hidden' name='opid' value='$opid' />\n
							</form>\n";
					}else{
						$dHtml .= "<h3>{L_ERROR}</h3><p>{L_GAME_CONNECTION_ERROR0}</p>";
						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=setWebserverpassword'>{L_GAME_WEBSERVERPASSWORD}</a></h3>";
					}
				}

				//$dHtml .= $mainpageLink;
			}


			if( $action === "load" ){
				//das ist in restart enthalten.
			}
			if( $action === "restart" ){

				$step = 0;
				if( isset($_GET["step"]) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_RESTART}</h3>";

				if( $step == 1 ){
					$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
					//echo "OPID: $opid";
					if( operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{
						$fn = $_GET["filename"];

						if( $fn === "" ){
							$pbAction = array('action'=>'restart','password'=>$pw);
							$dHtml .= "<p>{L_GAME_INVOKE_RESTART1}</p>";
						}else{
							//split 'auto' flag from filename
							$tmp = explode(",",$fn);
							$fn = $tmp[0];
							$folderIndex = 0;
							if( count($tmp)>1 ) $folderIndex = intval($tmp[1]);

							$pbAction = array('action'=>'restart','password'=>$pw,'filename'=>$fn,'folderIndex'=>$folderIndex);
							$dHtml .= "<p>{L_GAME_INVOKE_RESTART2|$fn}</p>";
						}

						$infos = json_decode(handle_pitboss_action($gameData, $pbAction));
						if( $infos->return === "ok" ){
							$dHtml .= "<p>{L_GAME_SUCCESS_MSG}".$infos->info ."</p>";
							operation_update_ids( $opid );
						}else{
							$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
						}
					}
				}else{
					$dHtml .= "<p>{L_GAME_NOTES_RESTART}</p>";

					$opid = operation_new_val();
					//Check if player is logged in and print warning
					$pbAction = array('action'=>'info');
					$infos = json_decode(handle_pitboss_action($gameData, $pbAction));
					if( $infos->return === "ok" ){
						$num_online = get_number_of_connected_players($infos->info->players);
						if( $num_online  > 0 ){
							$dHtml .= "<h3 style='color:red'>{L_WARNING}</h3>\n
								<p>{L_GAME_RESTART_WARNING|$num_online}</p>";
						}
					}

					//Get list of saves
					$pbAction = array('action'=>'listSaves','password'=>$pw);
					$infos = json_decode(handle_pitboss_action($gameData, $pbAction));
					if( $infos->return === "ok" ){

						$dHtml .= "{L_FILE}: <form action='$this_page' method='get'>\n";
						$dHtml .= "<input type='hidden' name='opid' value='$opid' />\n";
						$dHtml .= "<select name='filename'><option style='text-align:center;' value=''>{L_GAME_RESTART_RUNNING}</option>";

						//Sort list by date
						function sortByOrder($a, $b) {
							return $b->timestamp - $a->timestamp;
						};

						usort($infos->list, 'sortByOrder');

						foreach( ($infos->list) as $savefile ){
							// Remove file extensions
							$sname = $savefile->name;
							$dot = strrpos($sname, ".");
							if($dot !== false){
								$sname = substr($sname, 0, $dot);
							}
							$dHtml .= "<option style='text-align:right;' value='".$sname.",".$savefile->folderIndex."'>".$sname." | ".$savefile->date."</option>";
						}
						$dHtml .= "</select>";
						$dHtml .= "<p><input type='submit' />\n
							<input type='hidden' name='action' value='restart' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='1' />\n
							</p></form>\n";
					}else{
						$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
					}

				}
				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;
			}

		}
	}

	return translate($dHtml);
}


function gamesListShort($listName, $ab, $maxNbr, $bUseChangeRestriction = false ){
	global $contentTables;

	if(!is_numeric($maxNbr)|| !is_numeric($ab)) return "Fehlerhafte Eingabeparameter.";
	if(! array_key_exists($listName,$contentTables)) return "Fehlerhafte Eingabeparameter.";
	$list = $contentTables[$listName];

	$userId = -1;
	$userLevel = 0;
	if( array_key_exists("loginId",$_SESSION) && array_key_exists("loginLevel",$_SESSION) ){ 
		$userId = $_SESSION["loginId"];
		$userLevel = $_SESSION["loginLevel"];
	}
	$view_operation = 0;
	$change_operation = 2;
	$access = getAccessLevel($listName, $userId, $userLevel, 
		$bUseChangeRestriction ? $change_operation : $view_operation );

	if( $access > 1 ){
		$sql = 'SELECT * FROM '.$list["sqlTable"].' ORDER BY id DESC LIMIT '.$ab.', '.$maxNbr.'; ';
	}elseif( $access > 0 ){
		$sql = 'SELECT * FROM '.$list["sqlTable"].' WHERE creatorUserId='.$userId.' ORDER BY id DESC LIMIT '.$ab.', '.$maxNbr.'; ';
	}

	$dHtml = '<table class="memberlist" style="width:100%">';
	try{
		$db = get_db_handle();

		$result  = $db->query($sql);
		if( $result )
		while($game = $result->fetch(PDO::FETCH_ASSOC))
		{
			$dHtml .= '<tr><td class="pad">'.gameShort($game).'</td></tr>';
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}

	$dHtml .= '</table>';

	return $dHtml;
}


function gameSingle($listName,$id){
	global $contentTables, $subdir;
	if(!is_numeric($id)) return "Fehlerhafte Eingabeparameter.";
	$dHtml = '';

	$list=$contentTables[$listName];
	$sql =  'SELECT * FROM '.$list["sqlTable"].' WHERE id='.$id.' ORDER BY date DESC ';
	//echo $sql;
	try{
		$db = get_db_handle();

		$result  = $db->query($sql);
		if( $result )
		while($game = $result->fetch(PDO::FETCH_ASSOC))
		{
			$dHtml .= '<tr><td class="hr pad">'.gameFull($game,1).'</td></tr>';
		}

	}catch(Exception $e){
		$dHtml .= 'Exception : '.$e->getMessage();
	}

	return $dHtml;
}


function hashGamePassword($str ){
	//$salt = "Well, for a few users we need no salt.";
	//return crypt($str,$salt);
	
	//Now use (unsecure) old hash function which is also available in
	//python 2.4 with the md5 package.
	return hash('md5', $str);	
}

/* It would be faster to call this method only if
 * a new password should be set.
 */
function matchingGamePassword($gameId,$gameData=null){
	$ret = false;

	$pw = "";
	if( array_key_exists( "passwordFor".$gameId, $_COOKIE ) ){
		$pw = $_COOKIE["passwordFor".$gameId];
	}
	$pwHash = hashGamePassword($pw);
	unset($pw);

	//Compare value with value from db.
	if( $gameData == null ){
		try{
			$db = get_db_handle();

			$statement = $db->prepare('SELECT id FROM games WHERE id=? AND managePasswordHash=? ;');
			$statement->bindValue(1, $gameId, PDO::PARAM_INT);
			$statement->bindValue(2, $pwHash, PDO::PARAM_STR);
			$result  = $statement->execute();

			if ( $result && $res = $statement->fetch(PDO::FETCH_ASSOC) )
			{
				if ( $res['id'] == $gameId )
					$ret = true;
			}

		}catch(Exception $e){
			$dHtml .= 'Exception : '.$e->getMessage();
		}
	}else{
		if( $gameData["id"] == $gameId
			&& $gameData["managePasswordHash"] == $pwHash )
		{
			$ret = true;
		}
	}

	return $ret;
}


//================


?>
