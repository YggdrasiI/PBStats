<?php
/* This strings are used in the content manager. */

$lang['number'] = "Number";

$lang['cm_select_table_title'] = "Select Table";
$lang['cm_select_table_desc'] = "Select table and action from te menu";

$lang['cm_add'] = "Add item";
$lang['cm_change'] = "Change item";
$lang['cm_delete'] = "Delete item";
$lang['cm_create'] = "Initialize table";
$lang['cm_recreate'] = "Setting back table";

$lang['cm_entry_add'] = "Add entry";
$lang['cm_entry_change'] = "Change entry";
$lang['cm_entry_delete'] = "Delete entry";

$lang['cm_create_table'] = "Are you sure to create the table '%s'?";
$lang['cm_recreate_table'] = "Are you sure to set table '%s' back? This deletes all items.";

$lang['cm_already_send'] = "The form was send twiche. To omit duplicates you has to begin with a <b>new form</b>.</p><p>Use the '".$lang['cm_change']."' menü to change existing entrys.";

$lang['cm_invalid_formular_data'] = "Form can not be handled because it contains invalid entries.";
$lang['cm_error_db'] = "During database operation an error occours.";
$lang['cm_error_table_creation'] = "Can not create table.";
$lang['cm_error_params'] = "Update failed. Wrong input arguments.";
$lang['cm_error_access'] = "Operation aborted. Not enought rights.";
$lang['cm_error_general'] = "An error occurs <a href='index.php'>Restart Submission?</a>";

$lang['cm_add_entry'] = "Create entry for table '%s'.";
$lang['cm_change_entry'] = "Change entry in table '%s'.";
$lang['cm_delete_entry'] = "Delete entry from table '%s'.";

$lang['cm_create_success'] = "Table '%s' created.";
$lang['cm_recreate_success'] = "Table '%s' droped and re-initialized.";
$lang['cm_add_success'] = "Save dataset into '%s'.";
$lang['cm_change_success'] = "Change dataset of '%s'.";
$lang['cm_delete_success'] = "Delete dataset from '%s'.";
$lang['cm_add_further_entry'] = "Create further entry in '%s'.";
$lang['cm_change_further_entry'] = "Change further entry in '%s'.";
$lang['cm_delete_further_entry'] = "Delete further entry in '%s'.";
$lang['cm_other_list'] = "Select other table.";

//For news table
$lang['cm_news_title_title'] = "Title";
$lang['cm_news_short_title'] = "Short preamble";
$lang['cm_news_short_desc'] = "Short leading-in. This sentence will be placed under the headline of the news on the start page.";
$lang['cm_news_content_title'] = "Full text";
$lang['cm_news_infolink_title'] = "Link to furthen information";
$lang['cm_news_infolink_desc'] = "Link will be placed under the text of the news. Absolute links have to begin with http://.";
$lang['cm_news_author_title'] = "Author";
$lang['cm_news_author_desc'] = "Your Nickname or Name. Field is editable for practical reason.";
$lang['cm_news_date_title'] = "Time of creation.";

//For downloads table
$lang['cm_download_to_big'] = "The file '%s' is to big to upload.";
$lang['cm_download_new_dir_yes'] = "Note: The directory '%s' was created.";
$lang['cm_download_new_dir_exists'] = "Note: The directory '%s' already exists.";
$lang['cm_download_category_title'] = "Category";
$lang['cm_download_category_desc'] = "Every download has to assined to a category. Create an new entry to the category table if no current field match.";
$lang['cm_download_public_title'] = "File(s) public";
$lang['cm_download_public_desc'] = "Files can be placed in a public (Link contains […]/public/[…]) or private (Link contains […]/private/[…]) subsection. Note that private files are NOT protected at default settings, but will be displayed to registered users, only. Use the .htaccess mechanism to or similar techniques if you want securec the private files.";
$lang['cm_download_show_on_startpage_title'] = "Show download on start page";
$lang['cm_download_show_on_startpage_desc'] =  "Enable this flag to show the file in the list of the newest downloads.";

global $maxFileSize;
$lang['cm_download_filename_title'] = "File(s)";
$lang['cm_download_filename_desc'] =  "The file size is limited on ".$maxFileSize.". Transfer bigger files with other tools and use the 'external files' field to link on them.";
$lang['cm_download_extern_title'] = "External file(s)";
$lang['cm_download_extern_desc'] =  "Use this to link to external files or internal files which wasn't uploaded over this formular.";
//For download categories table

//For games table
$lang['cm_game_name'] = "Game Title";
$lang['cm_game_url'] = "Url";
$lang['cm_game_port_title'] = "Port";
$lang['cm_game_port_desc'] = "Use the port number which was denoted in pbsettings.json (property: webserver.port ). ";
$lang['cm_game_manage_password_title'] = "Web administration password";
$lang['cm_game_manage_password_desc'] = "Use the password which was denoted in pbsettings.json (property: webserver.password ). ";
$lang['cm_game_description'] = "Informal description of the game settings";
$lang['cm_game_infolink'] = "Link to further information";
$lang['cm_game_date'] = "Time of creation";
$lang['cm_game_show_details'] = "Show details";
$lang['cm_game_human_title'] = "Who is the inventor of the Civilization series?";
$lang['cm_game_human_desc'] = "Just a simple barrier for registration robots.";
$lang['cm_game_url_update_title'] = "Automatic url update";
$lang['cm_game_url_update_desc'] = "If the Ip of your pitboss server changes frequently
	enable this option to update the ip of your pitboss server automaticly. This option only works
	if you enable the automatic update in pbSettings.json";

$lang['cm_username'] = "Username";
$lang['cm_username_desc'] = "Number of characters: 3-20 ; Allowed chars: A-z, 0-9, _-";
$lang['cm_username_already_used'] = "The username is already in usage or invalid.";
$lang['cm_user_email_title'] = "Email";
$lang['cm_user_email_desc'] = "Currently absolute unused. Not even a password reset.";
$lang['cm_user_password'] = "Password";
$lang['cm_user_date'] = "Date of registration";

$lang[''] = "";
?>
