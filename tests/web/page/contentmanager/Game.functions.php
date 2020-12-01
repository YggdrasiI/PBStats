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


function sign_is_ok($signCaption){
	if( strlen($signCaption) > 18) return false;
	foreach( str_split($signCaption) as $c ){
		if( ord($c)> 127 ){
			return false;
		}
	}
	return true;
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

			if( $action === "color" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_COLOR}</h3>";
				if( $step == 1 ){
					$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
					if( false && operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{
						$playerId = intval($_GET["playerId"]);
						$colorId = intval($_GET["colorId"]);
						$pbAction = array('action'=>'setPlayerColor','password'=>$pw,
							'playerId'=>$playerId,'colorId'=>$colorId);
						$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

						if( $infos->return === "ok" ){
							$dHtml .= "<p>{L_GAME_SET_PLAYER_COLOR|$playerId,$colorId}</p>";
							operation_update_ids( $opid );
						}else{
							$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
						}
					}
				}else{
					$dHtml .= "<p>{L_GAME_NOTES_PLAYER_COLOR}</p>";
					//request to get actual round
					$opid = operation_new_val();

					$action_info = array('action'=>'info');
					$infos = json_decode(handle_pitboss_action($gameData, $action_info));
					//Get list of saves
					$pbAction = array('action'=>'listPlayerColors');
					$colorData = json_decode(handle_pitboss_action($gameData, $pbAction));

					if( ($infos->return === "ok") && ($colorData->return === "ok") ){
						$dHtml .= "<h4>Colorset / Id / Used by player</h4>";

						$colId = 0;
						foreach( $colorData->colors as $color ){

							$dHtml .= "<p>";
							$dHtml .= "<span class='playerColor' style='background-color:rgba(".$color->primary.");'>Primary</span>\n";
							$dHtml .= "<span class='playerColor' style='background-color:rgba(".$color->secondary.");'>Secondary</span>\n";
							$dHtml .= "<span class='playerColor' style='background-color:rgba(".$color->text.");'>Textcolor</span>\n";
				
							$dHtml .= "<span style='padding:0.4em;'> $colId / ";
							foreach( $color->usedBy as $player ){
								$dHtml .= $player->name.", ";
							}
							$dHtml .= "</span></p>\n";

							$colId += 1;
						}

						// Use Hex values and create list in BB CODE
						$colId = 0;
							$dHtml .= "<p>BB-Code: <textarea>Primary Secondary Textcolor ID / {L_GAME_PLAYER}\n";
						foreach( $colorData->colors as $color ){
							$tmp = explode(",", $color->primary);
							$primaryHex = sprintf("%02X%02X%02X", $tmp[0], $tmp[1], $tmp[2]);
							$tmp = explode(",", $color->secondary);
							$secondaryHex = sprintf("%02X%02X%02X", $tmp[0], $tmp[1], $tmp[2]);
							$tmp = explode(",", $color->text);
							$textHex = sprintf("%02X%02X%02X", $tmp[0], $tmp[1], $tmp[2]);

							$dHtml .= "[COLOR=#$primaryHex]██████[/COLOR]";
							$dHtml .= "[COLOR=#$secondaryHex]██████[/COLOR]";
							$dHtml .= "[COLOR=#$textHex]██████[/COLOR]";

							$dHtml .= " $colId / ";
							foreach( $color->usedBy as $player ){
								$dHtml .= $player->name.", ";
							}
						$dHtml .= "\n";

							$colId += 1;
						}
						$dHtml .= "</textarea></p>\n";

						$dHtml .= "<h4>{L_GAME_PLAYER} / {L_GAME_NEW_COLOR}</h4> <form action='$this_page' method='get'>\n";
						$dHtml .= "<input type='hidden' name='opid' value='$opid' />\n";
						$dHtml .= "<select name='playerId'>";

						$colId = 0;
						foreach( $infos->info->players as $player ){
							$playerId = $player->id;
							$playerName = $player->name;
							$dHtml .= "<option class='playerColor' style='text-align:left;' value='$playerId'>$playerId - $playerName</option>";
						}
						$dHtml .= "</select>";
						$dHtml .= "<select name='colorId'>";

						foreach( $colorData->colors as $color ){
							$dHtml .= "<option class='playerColor' style='text-align:right;padding-right:1em;background-color:rgba(".$color->primary.")' value='$colId'>$colId</option>";
							$colId += 1;
						}
						$dHtml .= "</select>";
						$dHtml .= "<p><input type='submit' />\n
							<input type='hidden' name='action' value='color' />\n
							<input type='hidden' name='game' value='$gameId' />\n
							<input type='hidden' name='step' value='1' />\n
							</p></form>\n";
					}else{
						$dHtml .= "<h3>{L_ERROR}</h3><p>{L_GAME_CONNECTION_ERROR0}</p>";
						$dHtml .= "<p>".$infos->return."</p>";
						$dHtml .= "<p>".$colorData->info."</p>";
						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=color'>{L_GAME_PLAYERCOLOR}</a></h3>";
					}
					$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
					$dHtml .= $mainpageLink;

				}
			}

			if( $action === "motd" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_MOTD_MESSAGE}</h3>";
				if( $step == 1 ){
					$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
					if( false && operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{
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
				}else{
					$opid = operation_new_val();

					//Get current MotD
					$pbAction = array('action'=>'getMotD','password'=>$pw);
					$motdData = json_decode(handle_pitboss_action($gameData, $pbAction));

					//$dHtml .= "<h3 class='hr pad'>{L_GAME_MOTD_MESSAGE}</h3>";
					$dHtml .= "<form action='$this_page' method='get'>\n<p>";

					//older version of the mod doesn't support getMotD
					if( ($motdData->return === "ok") ){
							$dHtml .= "{L_MESSAGE}: <input type='text' name='msg' value='".$motdData->msg."' />\n";
					}else{
						//$dHtml .= "<p>{L_GAME_ERROR_MSG}".$motdData->info ."</p>";
						$dHtml .= "{L_MESSAGE}: <input type='text' name='msg' value='' />\n";
					}
					$dHtml .= "<input type='submit' />\n
						<input type='hidden' name='action' value='motd' />\n
						<input type='hidden' name='game' value='$gameId' />\n
						<input type='hidden' name='step' value='1' />\n
						<input type='hidden' name='opid' value='$opid' />\n
						</p></form>\n";

				}
				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;

			}

			if( $action === "kick" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_KICK}</h3>";
				if( $step == 1 ){
					$opid = isset($_GET["opid"])?intval($_GET["opid"]):-1;
					if( false && operation_already_done( $opid ) ){
						$dHtml .= print_operation_error_msg();
					}else{
						// Klick player by id
						$playerId = intval($_GET["playerId"]);
						$pbAction = array('action'=>'kickPlayer','password'=>$pw,'playerId'=>$playerId);
						$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

						if( $infos->return === "ok" ){
							$dHtml .= "<p>{L_GAME_KICK_SUCCESSFUL|$playerId}</p>";
							operation_update_ids( $opid );
						}else{
							$dHtml .= "<p>{L_GAME_ERROR_MSG}".$infos->info ."</p>";
						}
					}
				}else{
					$opid = operation_new_val();

					$action_info = array('action'=>'info');
					$infos = json_decode(handle_pitboss_action($gameData, $action_info));
          if( $infos->return === "ok" ){
            //Gen list of players and their status.
            global $status_strings;
            $players = append_status($infos->info->players);

						$dHtml .= "<p>{L_GAME_KICK_DESC}</p>\n";
            $dHtml .= "<form action='$this_page' method='get'>\n<p>";
            $dHtml .= "<select name='playerId'>";
            foreach( $players as $player ){
              $playerId = $player->id;
              $playerName = $player->name;
              $playerStatus = $status_strings[$player->statusId];
              $dHtml .= "<option style='text-align:left;' value='$playerId'>$playerId - $playerName - $playerStatus</option>";
            }
            $dHtml .= "</select>";	

            $dHtml .= "<input type='submit' />\n
              <input type='hidden' name='action' value='kick' />\n
              <input type='hidden' name='game' value='$gameId' />\n
              <input type='hidden' name='step' value='1' />\n
              <input type='hidden' name='opid' value='$opid' />\n
              </p></form>\n";
          }else{
						$dHtml .= "<h3>{L_ERROR}</h3><p>{L_GAME_CONNECTION_ERROR0}</p>";
						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=setWebserverpassword'>{L_GAME_WEBSERVERPASSWORD}</a></h3>";
					}

				}
				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;

			}

			if( $action === "replay" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_REPLAY}</h3>";
				//Testing parsing of replay messages. Require debug=True in pbSettings.json
				$pbAction = array('action'=>'getReplay','password'=>$pw);
				$replayData = json_decode(handle_pitboss_action($gameData, $pbAction));
				if( ($replayData->return === "ok") ){
					$dHtml .= "<h4>Replay Messages</h4><p>\n";
					foreach( $replayData->replay as $message ){
						$dHtml .= 'Round ' . $message->turn . ", Player ". $message->player .": ". $message->text . "<br>";
					}
					$dHtml .= "</p>\n";
					$dHtml .= "<h4>Graphs</h4>\n";
					if( isset( $replayData->graphs ) ){
						foreach( $replayData->graphs as $id=>$player ){
							$dHtml .= "<h5>Player $id</h5>\n";
							$dHtml .= "</>Score: \n";
							foreach( $player->score as $val ){
								$dHtml .= "$val ";
							}
							$dHtml .= "</p>\n";
							$dHtml .= "</>Economy: \n";
							foreach( $player->economy as $val ){
								$dHtml .= "$val ";
							}
							$dHtml .= "</p>\n";
							$dHtml .= "</>Industry: \n";
							foreach( $player->industry as $val ){
								$dHtml .= "$val ";
							}
							$dHtml .= "</p>\n";
							$dHtml .= "</>Agriculture: \n";
							foreach( $player->agriculture as $val ){
								$dHtml .= "$val ";
							}
							$dHtml .= "</p>\n";
						}
					}
				}else{
					$dHtml .= "<p>{L_GAME_ERROR_MSG}".$replayData->info ."</p>";
				}

				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;
			}

			if( $action === "getWBSave" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_WBSAVE}</h3>";
				$pbAction = array('action'=>'getWBSave','password'=>$pw,'noCache'=>'0','compress'=>'0');
				$wbSaveData = json_decode(handle_pitboss_action($gameData, $pbAction));
				if( ($wbSaveData->return === "ok") ){
					$dHtml .= "<h4>WBSave</h4><p><textarea>\n";
					$dHtml .= $wbSaveData->save;
					$dHtml .= "</textarea></p>\n";
				}else{
					$dHtml .= "<p>{L_GAME_ERROR_MSG}".$wbSaveData->info ."</p>";
				}

				$dHtml .= "<p><a href='$this_page?game=$gameId&action=admin'>{L_GAME_ADMIN_BACK}</a></p>";
				$dHtml .= $mainpageLink;
			}

			if( $action === "fixSigns" ){
				$step = 0;
				if( isset($_GET["step"] ) ){
					$step = $_GET["step"];
				}

				$dHtml .= "<h3>{L_GAME_SIGNS}</h3>";
				if( $step == 1 ){
					$pbAction = array('action'=>'cleanupSigns','password'=>$pw);
					$signsData = json_decode(handle_pitboss_action($gameData, $pbAction));
					if( ($signsData->return === "ok") ){
						$dHtml .= "<h4>Cleanup Signs</h4><p>\n";
						foreach( $signsData->info as $sign ){
							$dHtml .= "<span" . (sign_is_ok($sign->caption)?"":" class='fontColorWarn' ") . ">";
							$dHtml .= "Id: " . $sign->id . ", Caption: " . $sign->caption;
							$dHtml .= "</span><br>\n";
						}
						$dHtml .= "</p>\n";
					}else{
						$dHtml .= "<p>{L_GAME_ERROR_MSG}".$signsData->info ."</p>";
					}
				}else{
					$pbAction = array('action'=>'listSigns','password'=>$pw);
					$signsData = json_decode(handle_pitboss_action($gameData, $pbAction));
					if( ($signsData->return === "ok") ){
						$dHtml .= "<p>{L_GAME_SIGNS_DESCRIPTION}</p>\n";
						$dHtml .= "<p>{L_GAME_SIGNS_QUESTION}  <a href='$this_page?game=$gameId&action=fixSigns&step=1'>{L_YES}</a></p>";
						$dHtml .= "<h4>Current Signs</h4><p>\n";
						foreach( $signsData->info as $sign ){
							$dHtml .= "<span" . (sign_is_ok($sign->caption)?"":" class='fontColorWarn' ") . ">";
							$dHtml .= "Id: " . $sign->id . ", Caption: " . $sign->caption; 
							$dHtml .= "</span><br>\n";
						}
						$dHtml .= "</p>\n";
					}else{
						$dHtml .= "<p>{L_GAME_ERROR_MSG}".$signsData->info ."</p>";
					}


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
							$hours = intval($_GET["hours"]);
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

						if( $step == 10 ){
							// Set timer for current round
							$hours = intval($_GET["hours"]);
							$minutes = intval($_GET["minutes"]);
							$pbAction = array('action'=>'setCurrentTurnTimer','password'=>$pw,'hours'=>$hours,'minutes'=>$minutes,'seconds'=>10);
							$infos = json_decode(handle_pitboss_action($gameData, $pbAction));

							if( $infos->return === "ok" ){
								$dHtml .= "<p>{L_GAME_SET_TIMER_THIS_ROUND_SUCCESSFUL|$hours|$minutes}</p>";
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

						if( isset( $infos->info->turnTimerMax ) ){
							$seconds = intval($infos->info->turnTimerValue)/4;
							$open_hours =  floor($seconds/3600);
							$open_minutes = 	floor(($seconds%3600)/60)+1;
							$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_TIMER_THIS_ROUND}</h3>";
							$dHtml .= "<form action='$this_page' method='get'>\n
								<p>{L_HOURS}: <input type='number' name='hours' value='".$open_hours."' />\n
								<p>{L_MINUTES}: <input type='number' name='minutes' value='".$open_minutes."' />\n
								<input type='submit' />\n
								<input type='hidden' name='action' value='admin' />\n
								<input type='hidden' name='game' value='$gameId' />\n
								<input type='hidden' name='step' value='10' />\n
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

						$dHtml .= "<h3 class='hr pad'><a href='$this_page?game=$gameId&action=motd&opid=$opid'>{L_GAME_MOTD_MESSAGE}</a></h3>";
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

						$dHtml .= "<h3 class=' '><a href='$this_page?game=$gameId&action=kick&opid=$opid'>{L_GAME_KICK}</a></h3>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_AUTOSTART_FLAG}</h3>";
						$dHtml .= "<p>{L_GAME_NOTES_AUTOSTART}</p>";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=5&value=1'>{L_GAME_AUTOSTART_ENABLE}</a> ";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=5&value=0'>{L_GAME_AUTOSTART_DISABLE}</a><br>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_SET_HEADLESS_FLAG}</h3>";
						$dHtml .= "<p>{L_GAME_NOTES_HEADLESS}</p>";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=7&value=1'>{L_GAME_HEADLESS_ENABLE}</a> ";
						$dHtml .= "<a href='$this_page?game=$gameId&action=admin&opid=$opid&step=7&value=0'>{L_GAME_HEADLESS_DISABLE}</a><br>";

						$dHtml .= "<h3 class='hr pad'>{L_GAME_ADVANCED_SETTINGS}</h3><div style='padding-left:2em'>";
						$dHtml .= "<h3 class=''><a href='$this_page?game=$gameId&action=color'>{L_GAME_COLOR}</a></h3>";
						$dHtml .= "<h3 class=''><a href='$this_page?game=$gameId&action=fixSigns'>{L_GAME_SIGNS}</a></h3>";
						$dHtml .= "<h3 class=''><a href='$this_page?game=$gameId&action=replay'>{L_GAME_REPLAY}</a></h3>";
						$dHtml .= "<h3 class=''><a href='$this_page?game=$gameId&action=getWBSave'>{L_GAME_WBSAVE}</a></h3>";
						$dHtml .= "</div>";
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
