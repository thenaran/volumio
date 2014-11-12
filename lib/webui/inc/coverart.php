<?php
/*
 *      PlayerUI Copyright (C) 2013 Andrea Coiutti & Simone De Gregori
 *		 Tsunamp Team
 *      http://www.tsunamp.com
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with TsunAMP; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 *
 *	UI-design/JS code by: 	Andrea Coiutti (aka ACX)
 * PHP/JS code by:			Simone De Gregori (aka Orion)
 * 
 * file:							coverart.php
 * version:						1.0
 *
 */
 
require_once('Zend/Media/Flac.php'); // or using autoload
ini_set('display_errors', '1');
include('connection.php');
// read current session parameters
session_start();
session_write_close();
// fetch MPD status
$status = _parseStatusResponse(MpdStatus($mpd));
$curTrack = getTrackInfo($mpd,$status['song']);
if (isset($curTrack[0]['Title'])) {
$status['currentartist'] = $curTrack[0]['Artist'];
$status['currentsong'] = $curTrack[0]['Title'];
$status['currentalbum'] = $curTrack[0]['Album'];
$status['fileext'] = parseFileStr($curTrack[0]['file'],'.');
}
$currentpath = "/mnt/".findPLposPath($status['song'],$mpd);
//echo $currentpath;

$flac = new Zend_Media_Flac($currentpath);

// Extract picture
if ($flac->hasMetadataBlock(Zend_Media_Flac::PICTURE)) {
    header('Content-Type: ' . $flac->getPicture()->getMimeType());
    echo $flac->getPicture()->getData();
} else {

$ch = curl_init(ui_lastFM_coverart($status['currentartist'],$status['currentalbum'],$_SESSION['lastfm_apikey']));
curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$image = curl_exec($ch);
curl_close($ch);

header('Content-Type: ' .mime_content_type($image));
echo $image;

}

?>
