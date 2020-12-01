 <?php
$lang['hours'] = "Stunden";
$lang['minutes'] = "Minuten";
$lang['message'] = "Nachricht";

$lang['game_status'] = "Status"; //"Status & Spielerliste";
$lang['game_log'] = "Log";
$lang['game_admin'] = "Administrieren";
$lang['game_save'] = "PB-Spiel speichern";
$lang['game_restart'] = "PB-Server neu starten";
$lang['game_restart_warning'] = "Achtung, es sind %s Spieler auf dem Pitboss-Server eingeloggt.";
$lang['game_restart_running'] = "Laufende Instanz.";
$lang['game_webserverpassword'] = "Ändere Passwort für Webzugriff";

$lang['game_players'] = "Spieler";
$lang['game_name'] = "Name";
$lang['game_turn'] = "Runde";
$lang['game_date'] = "Datum";
$lang['game_timer'] = "Timer";
$lang['game_timer_next_round'] = "Zeit für nächste Runde";
$lang['game_pause'] = "Pause";
$lang['game_paused'] = "Spiel pausiert";
$lang['game_pause_enable'] = "Aktiviere Pause";
$lang['game_pause_disable'] = "Deaktiviere Pause";
$lang['game_comment'] = "Kommentar";
$lang['game_end_turn'] = "Ende";
$lang['game_player'] = "Spieler";
$lang['game_password'] = "Passwort";
$lang['game_leader'] = "Anführer";
$lang['game_civilization'] = "Zivilisation";
$lang['game_score'] = "Punkte";
$lang['game_player_status'] = "Status";
$lang['game_chat_message'] = "Sende Chat-Nachricht an Spieler";
$lang['game_chat_message_successful'] = "Nachricht „%s“ gesendet.";
$lang['game_motd_message'] = "Ändere Begrüßungsnachricht (MotD)";
$lang['game_motd_message_successful'] = "Neue Nachricht des Tages: „%s“.";

$lang['game_short_names'] = "Ändere Buchstabenanzahl im Loginscreen";
$lang['game_short_names_desc'] = "Um die Datenübertragung bei einigen, restriktiv konfigurierten, Internetanschlüssen zu ermöglichen, wird ein bestimmtes Datenpaket verkleinert. Dies wird durch Kürzen von Anführername und Zivilisationsname realisiert, was allerdings zur Folge hat, dass die Namen im Login-Bildschirm abgeschnitten werden.
	Bei 52 Zivs sollte die Summe der beiden Werte 5 nicht überschreiten. Bei weniger Spielern kann man auch mehr Buchstaben zulassen.<br>
	Um die Option zu deaktivieren kann man den vorderen Wert auf Null setzen.<br>
	Beim Wert 1 wird nicht gekürzt, sondern die Spielerliste durchnummeriert (A-z).";
$lang['game_short_names_successful'] = "Änderung erfolgreich.<br>Neue Länge des Anführernames: %s.<br>Neue Länge des Nationennames: %s.";
$lang['leader_name'] = "Anführername";
$lang['civ_desc'] = "Nationenbeschreibung";

$lang['game_set_timer'] = "Setze den Runden-Timer";
$lang['game_set_timer_successful'] = "Runden-Timer auf %s gesetzt.";
$lang['game_set_timer_this_round'] = "Setze Timer der aktuellen Runde";
$lang['game_set_timer_this_round_successful'] = "Timer auf %sh %sm gesetzt.";
$lang['game_end_round'] = "Forciere Rundenende";
$lang['game_end_turn_successful'] = "Die neue Runde wurde eingeleitet.";
$lang['game_end_turn_error'] = "Fehler. Der Server antwortete: ";
$lang['game_end_turn_ask'] = "Sind sie sicher, dass sie eine neue Runde starten möchten?";
$lang['game_set_autostart_flag'] = "Autostart von Spielständen";
$lang['game_autostart_enable'] = "Aktiviere Autostart";
$lang['game_autostart_disable'] = "Deaktiviere Autostart";
$lang['game_set_headless_flag'] = "Deaktiviere Pitboss-Fenster";
$lang['game_headless_enable'] = "Headless-Modus (Kein Fenster)";
$lang['game_headless_disable'] = "Normaler Modus (Mit Fenster)";
$lang['game_player_password_change'] = "Passwort eines Spielers ändern";
$lang['game_operation_already_done'] = "Diese Operation wurde bereits ausgeführt. Klicken Sie auf „".$lang['game_admin']."“, um eine neue Opreation zu starten.";
//$lang['game_operation_already_done'] = "This operation was already done. Go to main page to start a new operation";

$lang['game_error_msg'] = "Es ist ein Fehler aufgetreten. Der Server antwortete:<br>";
$lang['game_success_msg'] = "Operation erfolgreich. Der Server antwortete:<br>";

$lang['game_admin_back'] = "Zurück zum ".$lang['game_admin']."-Menü.";
$lang['game_status_error'] = "Kann Spielstatus nicht lesen. Fehlermeldung:<br>";
$lang['game_connection_error0'] = "Fehler. Kann keine Verbindung zum Pitboss-Server herstellen.";
$lang['game_connection_error1'] = "Verbindungsversuch zum Server war nicht erfolgreich. Zeige letzten bekannte Daten an.";
$lang['game_connection_error2'] = "Verbindungsversuch zum Server war nicht erfolgreich. Es liegen auch keine älteren Daten vor.";
$lang['game_password_success'] = "Das Passwort des Spielers wurde erfolgreich geändert.";
$lang['game_password_error'] = "Fehler. Konnte Passwort nicht ändern. Der Server antwortete:<br>";
$lang['game_save_file'] = "„%s“ gespeichert.";
$lang['game_pause_successful'] = "Pausen-Flag wurde gesetzt auf: %s.";
$lang['game_notes_save_file'] = "Dateinamen ohne Endung eingeben.</p><p>Wurde der Pitboss-Server mit ALTROOT-Argument gestartet, beeinflusst dies auch den Speicherort der Spielstände.";

$lang['game_notes_restart'] = "Spielstände sind meist durch ein Admin-Passwort geschützt, welches beim Laden eines
	Spielstandes erfragt wird. Das Admin-Passwort kann (derzeit) nur über die pbSettings-Datei im ALTROOT-Verzeichnis des PB-Servers definiert werden. D.h. man kann immer nur Spielstände mit identischem Passwort laden.
	</p><p>Während des Neustarts ist die Weboberfläche nicht verfügbar.";
$lang['game_invoke_restart1'] = "Spiel gespeichert und Pitboss-Server neugestartet.";
$lang['game_invoke_restart2'] = "Zu ladende Datei auf „%s“ gesetzt und Pitboss-Server neugestartet.";

$lang['game_notes_password'] = "Um den Pitboss-Server zu steuern, ist das Webpasswort des Spiels erforderlich. (Dieses Passwort gibt es nur in dieser Mod und ist in der pbSettings.json definiert.)
	</p><p>Das Passwort wird als Cookie auf diesem Rechner gespeichert.
	</p><p>Das Webpasswort eines Spiels ist nicht an den Account des PB-Hosts gebunden. Sie könnten es theoretsch auch jedem Mitspieler geben. Diese müssen sich nicht auf dieser Webseite registieren, um den PB-Server zu verwalten.";

$lang['game_notes_autostart'] = "Achtung, solange der PB-Server kein Spielstand geladen hat, kann auch nicht auf diese Weboberfläche zugegriffen werden. D.h. wenn der Autostart von Spielständen deaktiviert ist, muss der Serverbetreiber manuell ein Spiel laden.</p><p>
	Es ist allerdings auch ohne aktivierten Autostart möglich die Restart-Funktion im Webinterface zu nutzen. Der Autostart wird dann für genau einen Start aktiviert.";

$lang['game_notes_headless'] = "Das Zeichnen des Pitboss-Fensters belastet die CPU unnötig stark. Falls alle Aufgaben über die Weboberfläche erledigt werden, kann man mit dieser Option die GUI deaktivieren.";

$lang['game_notes_set_timer'] = "Der neue Wert  gilt ab der nächsten Runde.";
$lang['game_notes_end_round'] = "Achtung, derzeit werden bei dieser Funktion keinerlei KI-Aktionen durchgeführt.";

$lang['game_notes_player_password'] = "Hinweis: Am besten keine Sonderzeichen verwenden. Die könnten falsch interpretiert werden.";
$lang['game_color'] = "Ändere Spieler-Farbtupel";
$lang['game_notes_player_color'] = "Um ungünstige Farbkombination zwischen Nachbarn zu vermeiden, kann man mit dieser Funktion Spielern neue Farbtupel zuordnen.<br>
	Die verfügbaren Tupel sind definiert in Assets/XML/Interface/CIV4PlayerColorInfos.xml.";
$lang['game_player'] = "Spieler";
$lang['game_new_color'] = "Neue Farbe";
$lang['game_signs'] = "Karten-Markierungen";
$lang['game_signs_description'] = "Sometimes, the PB Server do not load save games under Wine (Error message mentioned corrupt save).<br>
	You can use this function to filtering the sign strings (Alt+S). 
	Then, the game should be loadable again.<br> If your savegame is already corrupt, you need to run the PB server on a Windows machine…<br>\n
	The following filtering will be applied:<ul>
	<li>Cut of after 18 characters.</li>
	<li>Limit on first 127 ascii characters.</li>
	</ul>\n";
$lang['game_signs_questions'] = "Are you sure to start the sign fixing?";
$lang['game_signs_description'] = "Manchmal verweigert der PB-Server unter Wine das Laden von Spielständen mit einer Fehlermeldung, die behauptet, dass der Spielstand korrupt ist. Allerdings kann das Spiel trotzdem noch unter Windows geladen werden.<br>
	Diese Funktion kann verwendet werden, um die Markierungs-Texte (Alt+S) zu filtern, die im Verdacht stehen, das Problem zu verursachen. Danach sollte das Spiel unter Wine wieder laufen. Wenn der PB-Server schon nicht mehr läuft, wenn man dieses Problem feststellt, muss man außerdem das Spiel auf einem Windows-Rechner laden, um die Funktion anzuwenden…
	Folgende (wahrscheinlich etwas über das Ziel hinausschießende) Modifikationen werden durchgeführt:<ul>
	<li>Wörter werden auf 18 Zeichen gekürzt.</li>
	<li>Alle Buchstaben mit einer Kodierung außerhalb der ersten 127 ascii Zeichen werden entfernt.</li>
	</ul>\n";
$lang['game_signs_question'] = "Sollen die Schildertexte modifiziert werden?";
$lang['game_wbsave'] = "Weltenbauer-Spielstand erzeugen";
$lang['game_replay'] = "Replay anzeigen";
$lang['game_advanced_settings'] = "Erweiterte Einstellungen";

$lang['game_kick'] = "Kicke Spieler";
$lang['game_kick_desc'] = "Setzt Status des Spieler-Slots auf KI.";
$lang['game_kick_successful'] = "Spieler %d wurde gekickt.";

// Log messages
$lang['log_player_change_name'] = "Spieler umbenannt zu %s.";
$lang['log_player_score_increased'] = "Punkte erhöht auf %s.";
$lang['log_player_score_decreased'] = "Punkte verringert auf %s.";
$lang['log_player_finished_turn'] = "Runde beendet.";
$lang['log_eliminated'] = "Vernichtet.";
$lang['log_switched_to_ai'] = "Kontrolle auf KI gestellt.";
$lang['log_logged_out'] = "Ausgeloggt.";
$lang['log_logged_in'] = "Eingeloggt.";
$lang['log_claimed_by_human'] = "Durch menschlichen Spieler übernommen.";
$lang['log_new_game'] = "Es wurde ein anderes Spiel geladen. Es ist nun %s (Runde %s).";
$lang['log_new_turn'] = "Eine neue Runde hat begonnen. Es ist nun %s (Runde %s).";
$lang['log_old_turn'] = "Eine frühere Runde wurde geladen. Es ist nun %s (Runde %s).";

?> 
