/**
 * Created by PyCharm.
 * User: dangtranthai
 * Date: 4/17/12
 * Time: 5:38 PM
 * To change this template use File | Settings | File Templates.
 */

function showtime(){
    if (!document.all && !document.getElementById)
    return;
    thelement=document.getElementById? document.getElementById("tick2"): document.all.tick2;
    var Digital=new Date();
    var hours=Digital.getHours();
    var minutes=Digital.getMinutes();
    var seconds=Digital.getSeconds();
    var dn="PM";
    if (hours<12)
    dn="AM";
    if (hours>12)
    hours=hours-12;
    if (hours==0)
    hours=12;
    if (minutes<=9)
    minutes="0"+minutes;
    if (seconds<=9)
    seconds="0"+seconds;
    var ctime=hours+":"+minutes+":"+seconds+" "+dn;
    thelement.innerHTML="<b style='font-size:15;color:blue;'>"+ctime+"</b>";
    setTimeout("showtime()",1000);
    }
window.onload=showtime;

