<?php
/* This strings are used in the content manager. */

$lang['number'] = "Zahl";

$lang['cm_select_table_title'] = "Tabelle/Liste wählen";
$lang['cm_select_table_desc'] = "Wählen Sie aus dem Menü Tabelle und Aktion aus";

$lang['cm_add'] = "Datensatz hinzufügen";
$lang['cm_change'] = "Datensatz ändern";
$lang['cm_delete'] = "Datensatz löschen";
$lang['cm_create'] = "Tabelle initialisieren";
$lang['cm_recreate'] = "Tabelle leeren/zurücksetzen";

$lang['cm_entry_add'] = "Eintrag hinzufügen";
$lang['cm_entry_change'] = "Eintrag ändern";
$lang['cm_entry_delete'] = "Eintrag löschen";

$lang['cm_create_table'] = "Sind sie sicher, dass sie die Tabelle „%s“ erstellen möchten?";
$lang['cm_recreate_table'] = "Sind sie sicher, dass sie die Tabelle „%s“ zurücksetzen wollen? Dabei gehen alle Inhalte verloren.";

$lang['cm_already_send'] = 'Die Daten dieses Formulars scheinen mehrfach abgesendet worden zu sein. Um Duplikate zu vermeiden müssen Sie mit einem <b>neuen</b> Formular beginnen, um einen weiteren Eintrag zu erstellen. Gespeicherte Datensätze können Sie über den Menüpunkt „'.$lang['cm_change'].'“ bearbeiten.';
$lang['cm_invalid_formular_data'] = "Das Formular konnte nicht verarbeitet werden, weil es unzulässige Angaben enthält.";
$lang['cm_error_db'] = "Bei der Datenbankoperation ist ein Fehler aufgetreten.";
$lang['cm_error_table_creation'] = "Das Anlegen der Tabelle ist fehlgeschlagen.";
$lang['cm_error_params'] = "Beim Update ist ein Fehler aufgetreten: Falsche Eingabeparameter.";
$lang['cm_error_access'] = "Sie haben für diese Operation nicht die erforderlichen Rechte.";
$lang['cm_error_general'] = "Es ist ein Fehler aufgetreten. <a href='index.php'>Eingabe neu starten</a>";

$lang['cm_add_entry'] = "Datensatz für die Tabelle „%s“ erstellen.";
$lang['cm_change_entry'] = "Datensatz in der Tabelle „%s“ ändern.";
$lang['cm_delete_entry'] = "Datensatz aus der Tabelle „%s“ löschen.";

$lang['cm_create_success'] = "Die Tabelle „%s“ wurde angelegt.";
$lang['cm_recreate_success'] = "Die Tabelle „%s“ wurde gelöscht und neu angelegt.";
$lang['cm_add_success'] = "Die Daten wurden in „%s“ gespeichert.";
$lang['cm_change_success'] = "Die Daten wurden in „%s“ aktualisiert.";
$lang['cm_delete_success'] = "Die Daten wurden aus „%s“ gelöscht.";
$lang['cm_add_further_entry'] = "Weiteren Eintrag in „%s“ erstellen.";
$lang['cm_change_further_entry'] = "Weiteren Eintrag in „%s“ ändern.";
$lang['cm_delete_further_entry'] = "Weiteren Eintrag in „%s“ löschen.";
$lang['cm_other_list'] = "Andere Liste auswählen.";

//For news table
$lang['cm_news_title_title'] = "Titel";
$lang['cm_news_short_title'] = "Kurze Einleitung";
$lang['cm_news_short_desc'] = "Kurze Einleitung oder Vorschau auf den gesamten Text. Dieser Text wird als Aufhänger unter dem Titel eingeblendet, falls die Nachricht auf der Startseite angezeigt wird. ";
$lang['cm_news_content_title'] = "Nachrichtentext";
$lang['cm_news_infolink_title'] = "Link auf weitere Informationen";
$lang['cm_news_infolink_desc'] = "Unter der Nachricht kann auf eine andere Webseite verwiesen werden. Absolute Links müssen mit http:// beginnen.";
$lang['cm_news_author_title'] = "Autor";
$lang['cm_news_author_desc'] = "Ihr Name. Aus praktischen Gründen ist das Feld aber frei editierbar.";
$lang['cm_news_date_title'] = "Erstellzeitpunkt";

//For downloads table
$lang['cm_download_to_big'] = "Die Datei „%s“ ist zu groß für einen Upload.";
$lang['cm_download_new_dir_yes'] = "Hinweis: Das neue Verzeichnis „%s“ wurde angelegt.";
$lang['cm_download_new_dir_exists'] = "Hinweis: Das Verzeichnis „%s“ exisstierte bereits.";
$lang['cm_download_category_title'] = "Kategorie";
$lang['cm_download_category_desc'] = "Jedem Download muss eine Kategorie zugeordnet werden. Ist keine passende vorhanden, legen Sie sie in der Tabelle für Download-Kategorien an.";
$lang['cm_download_public_title'] = "Datei(en) öffentlich";
$lang['cm_download_public_desc'] = "Dateien können in einen öffentlichen ([…]/public/[…]) oder privaten ([…]/private/[…]) Bereich abgelegt werden. Standardmäßig ist der private Downloads aber nicht stärker geschützt als öffentliche. Sie werden aber nur registrierten Nutzern angezeigt.";
$lang['cm_download_show_on_startpage_title'] = "Download auf Startseite anzeigen";
$lang['cm_download_show_on_startpage_desc'] =  "Ist die Option aktiviert wird der Downloadlink nicht nur in der Download-Sektion angezeigt sondern auch auf der Startseite.";

global $maxFileSize;
$lang['cm_download_filename_title'] = "Datei(en)";
$lang['cm_download_filename_desc'] =  "Die Dateigröße ist auf ".$maxFileSize." begrenzt. Größere Dateien müssen auf anderem Wege übertragen werden (siehe „externe Dateien“)";
$lang['cm_download_extern_title'] = "Externe Datei(en)";
$lang['cm_download_extern_desc'] =  "Hier können sie auf Dateien verlinken, die sie anderweitig hochgeladen haben oder auf externe Files verweisen.";
//For download categories table

//For games table
$lang['cm_game_name'] = "Titel des Spiels";
$lang['cm_game_url'] = "Url";
$lang['cm_game_port_title'] = "Port";
$lang['cm_game_port_desc'] = "Geben Sie hier den Port ein, welches Sie beim Pitboss-Server in der pbSettings.json beim Feld „webserver->port“ eingetragen haben.";
$lang['cm_game_manage_password_title'] = "Administrations-Passwort";
$lang['cm_game_manage_password_desc'] = "Geben Sie hier das Passwort ein, welches Sie beim Pitboss-Server in der pbSettings.json beim Feld „webserver->password“ eingetragen haben.";
$lang['cm_game_description'] = "Beschreibung des Spiels";
$lang['cm_game_infolink'] = "Link zu weiteren Informationen";// "Link to further information";
$lang['cm_game_date'] = "Erstellzeitpunkt";
$lang['cm_game_show_details'] = "Zeige Details";
$lang['cm_game_human_title'] = "Wer gilt als Erfinder der Civilization-Reihe?";
$lang['cm_game_human_desc'] = "Diese Frage dient zur Vermeidung automatisierter Registrierungen.";
$lang['cm_game_url_update_title'] = "Automatisch Server-IP sychronisieren";
$lang['cm_game_url_update_desc'] = "Falls die Ip Ihres Pitboss-Servers häufig wechselt können Sie die gespeicherte IP in der Datenbank	automatisch aktualisieren lassen. Dies funktioniert nur, wenn die Update-Funktion in pbSettings.json aktiviert ist.";

$lang['cm_username'] = "Benutzername";
$lang['cm_username_desc'] = "Anzahl von Buchstaben: 3-20 ; Erlaubte Zeichen: A-z, 0-9, _-";
//$lang['cm_username_desc'] = "Number of characters: 3-20 ; Allowed chars: A-z, 0-9, _-";
$lang['cm_username_already_used'] = "Der Benutzername wird bereits verwendet oder ist unzulässig.";
$lang['cm_user_email_title'] = "E-Mail-Adresse";
$lang['cm_user_email_desc'] = "Wird derzeit nicht verwendet.";
$lang['cm_user_password'] = "Passwort";
$lang['cm_user_date'] = "Registrierungsdatum";
$lang['cm_user_'] = "";
$lang['cm_user_'] = "";

$lang[''] = "";
?>
